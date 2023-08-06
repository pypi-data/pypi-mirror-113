# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NetSPI <rtt.support@netspi.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import json
import os
import pathlib
import sys
import time
import webbrowser
from typing import Any, Dict, List, Optional, Union, cast
from uuid import UUID

from requests import Response, Session
from rtt_sdk import exceptions, logging
from rtt_sdk.__version__ import __compatible_schema_version__, __title__, __version__
from rtt_sdk.helpers import is_task_failed, is_task_finished, recurse_encode_bytes
from rtt_sdk.models import (
    BlobReferenceOrData,
    BlobReferenceOrPayloadOrData,
    ClientScriptArguments,
    InstanceInResponse,
    PayloadSeed,
    TaskContext,
    TaskDetails,
    Tool,
    TransformPeCloneExports,
    TransformPeConvertToShellcode,
)
from rtt_sdk.openapi import OpenAPI, Reference, RequestBody
from rtt_sdk.schema import Schema
from rtt_sdk.stream import WebsocketStream

JSONResponse = Dict[str, Any]
ServerResponse = Union[JSONResponse, bytes]

BLOB_INLINE_DATA_LIMIT = 1024 * 8

#
# TODO List:
#
# - Race condition for setting up the websocket vs first task
# - Raise exceptions for tasks with bad statuses (error_info transforms)
# - Expose the feed subscription with callback registrations
# - Add a generic instance/task query APIs
# - Overload RTTClient init in Slingshot client to remove "tool" arg
# - Parameterize the get/post functions more
# - Add docstrings to everything
# - Dynamic class construction for ssclient.context.user
# - Look at alias function names (getuid, etc.)


class RTTClient:
    """
    Represents a RTT platform server client connection

    :param url: Server base URL (otherwise `$RTT_PLATFORM_SERVER`)
    :param token: Server authentication token (otherwise `$RTT_PLATFORM_TOKEN`)
    :param tool: Specific tool for tasking (otherwise `$RTT_PLATFORM_TOOL`)
    :param instance: Specific instance for tasking (otherwise `$RTT_PLATFORM_INSTANCE`)
    :param loop: Asyncio event loop
    :param debug: Enable verbose debug logging
    :param interactive: Enable prompting for user input
    :param session: Requests base session for HTTP traffic
    :param ssl_verify: Verify SSL when performing HTTP requests
    :param user_agent: User-Agent for HTTP requests
    """

    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
        tool: Optional[Tool] = None,
        instance: Optional[str] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        debug: bool = False,
        interactive: bool = True,
        session: Optional[Session] = None,
        ssl_verify: bool = True,
        user_agent: str = f"{__title__}/{__version__}",
    ):
        url = url or os.environ.get("RTT_PLATFORM_SERVER", None)
        token = token or os.environ.get("RTT_PLATFORM_TOKEN", None)
        tool = cast(Tool, (tool or os.environ.get("RTT_PLATFORM_TOOL", None)))
        instance = instance or os.environ.get("RTT_PLATFORM_INSTANCE", None)

        if not url:
            raise ValueError("url is a required parameter")
        if not tool:
            raise ValueError("tool is a required parameter")

        if not loop:
            loop = asyncio.get_running_loop()

        self._debug: bool = debug
        self._tool: Tool = tool
        self._instance_id: Optional[str] = instance
        self.instance: Optional[InstanceInResponse] = None
        self.instances: List[InstanceInResponse] = []
        self._url: str = url.rstrip("/")
        self._api_url: str = f"{self._url}/api"
        self._session: Session = session or Session()
        self._session.verify = ssl_verify
        self._task_events: Dict[str, asyncio.Event] = {}
        self._task_store: Dict[str, TaskDetails] = {}

        try:
            schema_text = self._session.get(f"{self._url}/openapi.json").text
            self._schema: OpenAPI = OpenAPI(**json.loads(schema_text))
        except Exception as e:
            raise exceptions.RTTServerError from e

        if self._schema.info.version != __compatible_schema_version__:
            logging.warn(
                f"API schema mismatch: {self._schema.info.version} [server]"
                f" != {__compatible_schema_version__} [compatible]"
            )
            # raise exceptions.RTTIncompatibleServer(f"{self._schema.info.version} != {__compatible_schema_version__}")

        self._tasks_schema_map = self._parse_schema()

        if not token:
            if interactive:
                token = self._get_token_interactive()
            else:
                raise ValueError("token is a required parameter")

        self._headers = {"User-Agent": user_agent, "Authorization": f"Bearer {token}"}

        self._task_stream = WebsocketStream(self, f"{self._api_url}/{self._tool.value}/tasks/feed")
        self._task_stream.add_callback(self._task_stream_callback)
        self._task_stream_task = asyncio.create_task(self._task_stream.connect())

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._session.close()

    def _task_stream_callback(self, data: bytes):
        task = TaskDetails(**json.loads(data))
        task_id = str(task.id)

        if task.command == "Script":
            return

        self._task_store[task_id] = task
        if task_id not in self._task_events:
            self._task_events[task_id] = asyncio.Event()
        if is_task_finished(self._task_store[task_id].delivery):
            self._task_events[task_id].set()

    def _parse_schema(self) -> Dict[str, str]:
        schema_map: Dict[str, str] = {}
        for path, info in self._schema.paths.items():
            if "/tasks/" not in path or not info.post:
                continue
            if not isinstance(info.post.requestBody, RequestBody):
                raise exceptions.RTTParsingError("Server schema is invalid")
            try:
                schema_ref = cast(Reference, info.post.requestBody.content["application/json"].schema_).ref
                schema_name = schema_ref.split("/")[-1]
                _ = getattr(sys.modules["rtt_sdk.models"], schema_name)
                schema_map[schema_name] = path
            except Exception as e:
                raise exceptions.RTTParsingError from e
        return schema_map

    def set_instance(self, instance: Union[InstanceInResponse, str]) -> None:
        self._instance_id = str(instance.id) if isinstance(instance, InstanceInResponse) else instance

    def bind_instance(self, instance_id: Optional[str] = None) -> None:
        if instance_id is not None:
            self._instance_id = instance_id

        if not self._instance_id:
            raise exceptions.RTTError("Instance id/tag/name was not provided")

        try:
            UUID(self._instance_id)
            return
        except ValueError:
            pass

        self.instances = self.get_instances()
        matches = [i for i in self.instances if i.tag == self._instance_id or i.name == self._instance_id]
        if len(matches) != 1:
            raise exceptions.RTTError("Instance tag/name was supplied, but could not be resolved")
        self.instance = matches[0]
        self._instance_id = str(self.instance.id)

    def request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict] = None,
        post_data: Optional[Dict] = None,
        multi_part: Optional[Dict] = None,
        **kwargs,
    ) -> Response:
        """
        Make an HTTP request to the platform server

        :param verb: The HTTP method to call (`get`, `post`, `put`, `delete`)
        :param path: Path or full URL to query (`/sub` or `http://server/sub`)
        :param query_data: Data to send as query parameters
        :param post_data: Data to send in the body (as json)
        :param multi_part: Multi-part form data (files)
        :param kwargs: Extra options for the request
        :raises RTTAuthenticationError: When authentication is invalid
        :raises RTTValidationError: When the request structure is invalid
        :raises RTTHttpError: For any other HTTP errors
        :return: A requests result object
        """
        if path.startswith("http://") or path.startswith("https://"):
            url = path
        else:
            url = f"{self._api_url}/{path.lstrip('/')}"
            url = url.replace("/api/api/", "/api/")  # TODO: I know...

        query_data = query_data or {}
        if "context" not in query_data:
            query_data["context"] = TaskContext.script.value

        if "{tool}" in url and self._tool:
            url = url.replace("{tool}", self._tool.value)

        # TODO: Handle retries
        response = self._session.request(
            verb,
            url,
            headers=getattr(self, "_headers", {}),
            params=query_data,
            json=recurse_encode_bytes(post_data),
            files=multi_part,
            **kwargs,
        )
        if self._debug:
            logging.debug(f"[{response.status_code}] {url} : {response.content.decode(errors='replace')}")
        if 200 <= response.status_code < 300:
            return response

        error_message: Union[bytes, str] = response.content
        try:
            error_message = response.json()["detail"]
            if isinstance(error_message, list):
                error_message = error_message[0]["msg"]
        except (KeyError, ValueError, TypeError):
            pass

        error_class = exceptions.RTTHttpError
        if response.status_code == 400:
            error_class = exceptions.RTTValidationError
        elif response.status_code == 401:
            error_class = exceptions.RTTAuthenticationError

        raise error_class(
            response_code=response.status_code,
            message=error_message,
            response_body=response.content,
        )

    def _convert_to_json(self, response: Response) -> JSONResponse:
        """
        Convert response data to formatted JSON

        :param response: The HTTP response object
        :raises RTTParsingError: When parsing cannot occur automatically
        :return: A JSONResponse object
        """
        if response.headers["Content-Type"] == "application/json":
            try:
                return response.json()
            except Exception as e:
                raise exceptions.RTTParsingError(message="Failed to parse the server message") from e
        else:
            raise exceptions.RTTParsingError(
                message=f'Server content type is invalid: {response.headers["Content-Type"]}',
                response_body=response.content,
            )

    def get(self, path: str, *args, **kwargs) -> JSONResponse:
        """
        Wrapper for `request()` as a `get` action

        :param path: Partial or complete URL path
        :param args: Positional arguments redirected to `request()`
        :param kwargs: Named arguments redirected to `request()`
        :return: A JSONResponse object
        """
        return self._convert_to_json(self.request("get", path, *args, **kwargs))

    def post(self, path: str, *args, **kwargs) -> JSONResponse:
        """
        Wrapper for `request()` as a `post` action

        :param path: Partial or complete URL path
        :param args: Positional arguments redirected to `request()`
        :param kwargs: Named arguments redirected to `request()`
        :return: A JSONResponse object
        """
        return self._convert_to_json(self.request("post", path, *args, **kwargs))

    def put(self, path: str, *args, **kwargs) -> JSONResponse:
        """
        Wrapper for `request()` as a `put` action

        :param path: Partial or complete URL path
        :param args: Positional arguments redirected to `request()`
        :param kwargs: Named arguments redirected to `request()`
        :return: A JSONResponse object
        """
        return self._convert_to_json(self.request("put", path, *args, **kwargs))

    def _get_token_interactive(self) -> str:
        """
        Perform round-trip authentication with the platform server to
        collect an access token for scripting. This will trigger a
        browser window to open.

        :raises RTTHttpError: When the server response code is unexpected
        :raisaes RTTAuthenticationTimedOut: When authentication checks exceed attempt thesholds
        :return: str
        """
        auth_start = self.get("/scripts/auth/start")

        logging.shout(f'Script authentication requested: {auth_start["verifyUrl"]}')
        webbrowser.open(auth_start["verifyUrl"])

        script_arguments = ClientScriptArguments(name=f"<external:{sys.argv[0]}>")

        max_attempts = 30
        sleep_delay = 2
        while max_attempts > 0:
            max_attempts -= 1
            try:
                auth_finish = self.post(
                    auth_start["finishUrl"], query_data={"tool": self._tool.value}, post_data=script_arguments.dict()
                )
                return auth_finish["access_token"]
            except exceptions.RTTHttpError as e:
                if e.response_code not in [401, 403]:
                    raise e
                time.sleep(sleep_delay)
        raise exceptions.RTTAuthenticationTimedOut

    def get_instances(self, tool: Optional[Tool] = None) -> List[InstanceInResponse]:
        """
        Get all instances from the server

        :param tool: Filter instances by tool
        :return: List of instances from the server
        """
        tool = tool if tool else self._tool
        return [InstanceInResponse(**i) for i in cast(List[Any], self.get(f"/{tool.value}/instances"))]

    def create_task(self, arguments: Schema, instance: Optional[Union[InstanceInResponse, str]] = None) -> TaskDetails:
        """
        Create a new task for an instance

        :param arguments: Task arguments inherited from a Schema base model
        :param instance: Target instance for tasking
        :raises ValueError: When arguments are missing or invalid
        :return: Created task details
        """
        schema_name = arguments.__class__.__name__
        if schema_name not in self._tasks_schema_map.keys():
            raise ValueError(f"Schema object for create_task is invalid: {arguments}")
        endpoint = self._tasks_schema_map[schema_name]
        if "{instance}" in endpoint:
            if instance:
                instance_id = instance.id if isinstance(instance, InstanceInResponse) else instance
            elif self._instance_id:
                instance_id = self._instance_id
            else:
                raise ValueError("Cannot create tasking without specifying a target instance")
            endpoint = endpoint.replace("{instance}", str(instance_id))
        task = TaskDetails(**self.post(endpoint, post_data=arguments.dict()))
        return task

    async def create_task_and_wait(
        self, arguments: Schema, instance: Optional[Union[InstanceInResponse, str]] = None
    ) -> TaskDetails:
        """
        Create a new task for an instance and wait for results

        :param arguments: Task arguments inherited from a Schema base model
        :param instance: Target instance for tasking
        :raises RTTTaskError: When the task indicates an error has occured
        :raises RTTError: When a task indicates an error but cannot be parsed
        :return: Created task details
        """
        task = self.create_task(arguments, instance=instance)
        task_id = str(task.id)

        if not self._task_stream.cursor:
            self._task_stream.cursor = task_id

        if task_id not in self._task_events:
            self._task_events[task_id] = asyncio.Event()

        await self._task_events[task_id].wait()
        task = self._task_store[task_id]

        if is_task_failed(task.status):
            if task.results.error_info:
                raise exceptions.RTTTaskError(task.results.error_info)
            else:
                raise exceptions.RTTError("A task failed, but no error information was returned")
        return task

    def create_blob(self, data: bytes) -> str:
        return self.request("post", "/blobs", multi_part={"data": data}).text

    def create_blob_reference(self, data: Union[bytes, os.PathLike, str]) -> BlobReferenceOrData:
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, os.PathLike):
            data = open(data, "rb").read()

        if len(data) < BLOB_INLINE_DATA_LIMIT:
            return BlobReferenceOrData(data=data)
        else:
            blob_id = self.create_blob(data)
            return BlobReferenceOrData(id=blob_id)

    def create_blob_or_payload_reference(
        self, data: Union[bytes, os.PathLike, str], profile: Optional[UUID] = None
    ) -> BlobReferenceOrPayloadOrData:
        if isinstance(data, str):
            if pathlib.Path(data).exists():
                data = pathlib.Path(data)
            else:
                payload_seed = PayloadSeed(tool=self._tool, name=data, profile=profile)
                return BlobReferenceOrPayloadOrData(payload=payload_seed)
        if isinstance(data, os.PathLike):
            data = open(data, "rb").read()
        if len(data) < BLOB_INLINE_DATA_LIMIT:
            return BlobReferenceOrPayloadOrData(data=data)
        else:
            blob_id = self.create_blob(data)
            return BlobReferenceOrPayloadOrData(id=blob_id)

    def resolve_blob_reference(self, ref: BlobReferenceOrData) -> bytes:
        if not ref.id and not ref.data:
            raise exceptions.RTTError("Blob reference is invalid")
        if ref.data:
            return ref.data
        return self.request("get", f"/blobs/{ref.id}").content

    def transform_clone_exports(
        self,
        target: Union[bytes, os.PathLike, str, BlobReferenceOrPayloadOrData],
        reference: Union[bytes, os.PathLike, str, BlobReferenceOrData],
        *,
        reference_path: Optional[str] = None,
    ) -> BlobReferenceOrData:
        if isinstance(target, BlobReferenceOrPayloadOrData):
            target_ref = target
        else:
            target_ref = self.create_blob_or_payload_reference(target)
        if isinstance(reference, BlobReferenceOrData):
            reference_ref = reference
        else:
            reference_ref = self.create_blob_reference(reference)
        body = TransformPeCloneExports(target=target_ref, reference=reference_ref, reference_path=reference_path)
        response = self.post("/transforms/pe/clone-exports", post_data=body.dict())
        return BlobReferenceOrData(**response)

    def transform_convert_to_shellcode(
        self,
        pe: Union[bytes, os.PathLike, str, BlobReferenceOrData, BlobReferenceOrPayloadOrData],
        *,
        srdi_exported_function: Optional[str] = None,
        srdi_user_data: Optional[bytes] = None,
        srdi_flags: Optional[int] = None,
    ) -> BlobReferenceOrData:
        if isinstance(pe, (BlobReferenceOrData, BlobReferenceOrPayloadOrData)):
            pe_ref = pe
        else:
            pe_ref = self.create_blob_or_payload_reference(pe)
        body = TransformPeConvertToShellcode(
            target=pe_ref,
            srdi_exported_function=srdi_exported_function,
            srdi_user_data=srdi_user_data,
            srdi_flags=srdi_flags,
        )
        response = self.post("/transforms/pe/convert-to-shellcode", post_data=body.dict())
        return BlobReferenceOrData(**response)
