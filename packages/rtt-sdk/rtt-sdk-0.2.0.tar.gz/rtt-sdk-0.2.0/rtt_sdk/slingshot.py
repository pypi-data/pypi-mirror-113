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
import base64
import os
from os import PathLike
from typing import Any, Dict, List, Optional, Tuple, Union

from requests import Session
from rtt_sdk import models
from rtt_sdk.__version__ import __title__, __version__
from rtt_sdk.client import RTTClient
from rtt_sdk.exceptions import RTTInvalidResults

OptionalInstance = Optional[models.InstanceInResponse]
BlobReference = Union[models.BlobReferenceOrData, models.BlobReferenceOrPayloadOrData]


class SlingshotClient(RTTClient):
    """
    Represents a RTT platform server client connection specifically for Slingshot

    :param url: Server base URL (otherwise `$RTT_PLATFORM_SERVER`)
    :param token: Server authentication token (otherwise `$RTT_PLATFORM_TOKEN`)
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
        instance = instance or os.environ.get("RTT_PLATFORM_INSTANCE", None)

        super().__init__(
            tool=models.Tool.slingshot,
            url=url,
            token=token,
            instance=instance,
            loop=loop,
            debug=debug,
            interactive=interactive,
            session=session,
            ssl_verify=ssl_verify,
            user_agent=user_agent,
        )

    async def camera_capture_raw(
        self,
        camera_id: int,
        quality: Optional[int] = None,
        *,
        instance: OptionalInstance = None,
    ) -> models.CameraCaptureResults:
        arguments = models.CameraCaptureArguments(camera_id=camera_id, quality=quality)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.CameraCaptureResults(**task.results.dict())

    async def camera_capture(
        self,
        camera_id: int,
        quality: Optional[int] = None,
        *,
        instance: OptionalInstance = None,
    ) -> bytes:
        results = await self.camera_capture_raw(camera_id, quality, instance=instance)
        if results.data is None:
            raise RTTInvalidResults
        return self.resolve_blob_reference(results.data)

    async def camera_list(self, instance: OptionalInstance = None) -> List[models.Camera]:
        arguments = models.CameraListArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.CameraListResults(**task.results.dict()).cameras or []

    async def context_idle(self, *, instance: OptionalInstance = None) -> int:
        arguments = models.ContextIdleArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ContextIdleResults(**task.results.dict())
        if results.minutes is None:
            raise RTTInvalidResults
        return results.minutes

    async def context_process(self, *, instance: OptionalInstance = None) -> models.ContextProcessResults:
        arguments = models.ContextProcessArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.ContextProcessResults(**task.results.dict())

    async def context_user(self, verbose: bool, *, instance: OptionalInstance = None) -> models.ContextUserResults:
        arguments = models.ContextUserArguments(verbose=verbose)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.ContextUserResults(**task.results.dict())

    async def context_gather(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> models.InfoResults:
        arguments = models.InfoArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.InfoResults(**task.results.dict())
        return results

    async def exit(self, *, instance: OptionalInstance = None) -> None:
        arguments = models.ExitArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_change_directory(self, directory: Optional[str] = None, *, instance: OptionalInstance = None) -> str:
        arguments = models.FileChangeDirectoryArguments(directory=directory)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.FileChangeDirectoryResults(**task.results.dict())
        if results.directory is None:
            raise RTTInvalidResults
        return results.directory

    async def file_copy(
        self,
        source: str,
        destination: str,
        force: Optional[bool] = None,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.FileCopyArguments(source=source, destination=destination, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_download_raw(self, path: str, *, instance: OptionalInstance = None) -> models.FileDownloadResults:
        arguments = models.FileDownloadArguments(path=path)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.FileDownloadResults(**task.results.dict())

    async def file_download(self, path: str, *, instance: OptionalInstance = None) -> bytes:
        results = await self.file_download_raw(path, instance=instance)
        if results.data is None:
            raise RTTInvalidResults
        return self.resolve_blob_reference(results.data)

    async def file_list(
        self,
        directory: str,
        *,
        time_format: Optional[models.TimeFormat] = None,
        instance: OptionalInstance = None,
    ) -> List[models.FileOrDirectory]:
        arguments = models.FileListArguments(directory=directory, time_format=time_format)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.FileListResults(**task.results.dict()).entries or []

    async def file_make_directory(self, path: str, *, instance: OptionalInstance = None) -> None:
        arguments = models.FileMakeDirectoryArguments(path=path)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_move(
        self,
        source: str,
        destination: str,
        *,
        force: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.FileMoveArguments(source=source, destination=destination, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_remove(
        self,
        path: str,
        *,
        force: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.FileRemoveArguments(path=path, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_remove_directory(
        self,
        path: str,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.FileRemoveDirectoryArguments(path=path)
        await self.create_task_and_wait(arguments, instance=instance)

    async def file_upload(
        self,
        path: str,
        data: Union[bytes, PathLike, str, BlobReference],
        *,
        force: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(data, (models.BlobReferenceOrData, models.BlobReferenceOrPayloadOrData)):
            blob_ref = data
        else:
            blob_ref = self.create_blob_or_payload_reference(data)
        arguments = models.FileUploadArguments(data=blob_ref, path=path, force=force)
        await self.create_task_and_wait(arguments, instance=instance)

    async def host_file(
        self,
        endpoint: str,
        data: Union[bytes, PathLike, str, models.BlobReferenceOrData],
        *,
        base_url: Optional[str] = None,
        encoding: Optional[models.HostingEncoding] = None,
        instance: OptionalInstance = None,
    ) -> str:
        if isinstance(data, models.BlobReferenceOrData):
            blob_ref = data
        else:
            blob_ref = self.create_blob_reference(data)
        arguments = models.HostFileArguments(data=blob_ref, base_url=base_url, endpoint=endpoint, encoding=encoding)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.HostFileResults(**task.results.dict())
        if results.url is None:
            raise RTTInvalidResults
        return results.url

    async def host_powershell(
        self,
        *,
        base_url: Optional[str] = None,
        local: Optional[bool] = None,
        process: Optional[str] = None,
        com_object: Optional[bool] = None,
        endpoint: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.HostPowershellArguments(
            base_url=base_url, local=local, process=process, com_object=com_object, endpoint=endpoint
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.HostPowershellResults(**task.results.dict())
        if results.command is None:
            raise RTTInvalidResults
        return results.command

    async def host_shellcode(
        self,
        endpoint: str,
        payload: Union[bytes, PathLike, str, BlobReference],
        *,
        base_url: Optional[str] = None,
        encoding: Optional[models.HostingEncoding] = None,
        srdi_exported_function: Optional[str] = None,
        srdi_user_data: Optional[bytes] = None,
        srdi_flags: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(payload, (models.BlobReferenceOrData, models.BlobReferenceOrPayloadOrData)):
            blob_ref = payload
        else:
            blob_ref = self.create_blob_or_payload_reference(payload)
        arguments = models.HostShellcodeArguments(
            endpoint=endpoint,
            base_url=base_url,
            encoding=encoding,
            payload=blob_ref,
            srdi_exported_function=srdi_exported_function,
            srdi_user_data=srdi_user_data,
            srdi_flags=srdi_flags,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def host_unload(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.HostUnloadArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def inject(
        self,
        payload: Union[bytes, PathLike, str, BlobReference],
        *,
        process: Optional[Union[str, int]] = None,
        technique: Optional[models.InjectionTechnique] = None,
        skip_conversion: Optional[bool] = None,
        srdi_exported_function: Optional[str] = None,
        srdi_user_data: Optional[bytes] = None,
        srdi_flags: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(payload, (models.BlobReferenceOrData, models.BlobReferenceOrPayloadOrData)):
            blob_ref = payload
        else:
            blob_ref = self.create_blob_or_payload_reference(payload)
        arguments = models.InjectArguments(
            payload=blob_ref,
            process=str(process),
            technique=technique,
            skip_conversion=skip_conversion,
            srdi_exported_function=srdi_exported_function,
            srdi_user_data=srdi_user_data,
            srdi_flags=srdi_flags,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def kerberos_load(
        self,
        ticket: Union[bytes, PathLike, str],
        *,
        instance: OptionalInstance = None,
    ) -> None:
        blob_ref = self.create_blob_reference(ticket)
        arguments = models.KerberosLoadArguments(ticket=blob_ref)
        await self.create_task_and_wait(arguments, instance=instance)

    async def kerberos_purge(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.KerberosPurgeArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def keylog_gather_raw(
        self, *, path: Optional[str] = None, instance: OptionalInstance = None
    ) -> models.KeylogGatherResults:
        arguments = models.KeylogGatherArguments(path=path)
        task = await self.create_task_and_wait(arguments, instance=instance)
        return models.KeylogGatherResults(**task.results.dict())

    async def keylog_gather(self, *, path: Optional[str] = None, instance: OptionalInstance = None) -> bytes:
        results = await self.keylog_gather_raw(path=path, instance=instance)
        if results.keylog is None:
            raise RTTInvalidResults
        return self.resolve_blob_reference(results.keylog)

    async def link(
        self,
        target: str,
        *,
        instance: OptionalInstance = None,
    ) -> List[models.DiscoveredInstance]:
        arguments = models.LinkArguments(target=target)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.LinkResults(**task.results.dict())
        if results.discovered is None:
            raise RTTInvalidResults
        return results.discovered

    async def managed_module_execute(
        self,
        input: str,
        method: str,
        *,
        version: Optional[models.DotNetFrameworkVersion] = None,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.ManagedModuleExecuteArguments(input=input, method=method, version=version)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ManagedModuleExecuteResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def managed_module_load(
        self,
        module: Union[bytes, PathLike, str, models.BlobReferenceOrData],
        *,
        version: Optional[models.DotNetFrameworkVersion] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(module, models.BlobReferenceOrData):
            blob_ref = module
        else:
            blob_ref = self.create_blob_reference(module)
        arguments = models.ManagedModuleLoadArguments(
            module=blob_ref,
            version=version,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def managed_module_unload(
        self,
        *,
        version: Optional[models.DotNetFrameworkVersion] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ManagedModuleUnloadArguments(version=version)
        await self.create_task_and_wait(arguments, instance=instance)

    async def mimikatz_execute(
        self,
        input: str,
        *,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.MimikatzExecuteArguments(target=input)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.MimikatzExecuteResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def mimikatz_load(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.MimikatzLoadArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def minidump(
        self,
        path: str,
        *,
        process: Optional[Union[str, int]] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.MinidumpArguments(path=path, process=str(process))
        await self.create_task_and_wait(arguments, instance=instance)

    async def native_module_execute(
        self,
        input: str,
        export: str,
        *,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.NativeModuleExecuteArguments(input=input, export=export)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.NativeModuleExecuteResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def native_module_load(
        self,
        module: Union[bytes, PathLike, str, models.BlobReferenceOrData],
        *,
        obfuscate: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(module, models.BlobReferenceOrData):
            module_ref = module
        else:
            module_ref = self.create_blob_reference(module)
        arguments = models.NativeModuleLoadArguments(
            module=module_ref,
            obfuscate=obfuscate,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def native_module_unload(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.NativeModuleUnloadArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def network_connect(
        self,
        hosts: str,
        port: int,
        *,
        timeout: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> List[str]:
        arguments = models.NetworkConnectArguments(hosts=hosts, port=port, timeout=timeout)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.NetworkConnectResults(**task.results.dict())
        if results.hosts is None:
            raise RTTInvalidResults
        return results.hosts

    async def network_enumerate_session(
        self,
        host: str,
        *,
        instance: OptionalInstance = None,
    ) -> List[models.SessionDetails]:
        arguments = models.NetworkEnumerateSessionArguments(host=host)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.NetworkEnumerateSessionResults(**task.results.dict())
        if results.sessions is None:
            raise RTTInvalidResults
        return results.sessions

    async def network_ping(
        self,
        host: str,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.NetworkPingArguments(host=host)
        await self.create_task_and_wait(arguments, instance=instance)

    async def network_resolve(
        self,
        host: str,
        *,
        instance: OptionalInstance = None,
    ) -> Tuple[str, str]:
        arguments = models.NetworkResolveArguments(host=host)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.NetworkResolveResults(**task.results.dict())
        if results.nbns_name is None or results.dns_name is None:
            raise RTTInvalidResults
        return results.dns_name, results.nbns_name

    async def powershell_execute(
        self,
        input: str,
        *,
        version: Optional[models.DotNetFrameworkVersion] = None,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.PowershellExecuteArguments(input=input, version=version)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.PowershellExecuteResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def powershell_load(
        self,
        *,
        version: Optional[models.DotNetFrameworkVersion] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.PowershellLoadArguments(version=version)
        await self.create_task_and_wait(arguments, instance=instance)

    async def powershell_stage(
        self,
        script: Optional[Union[bytes, PathLike, str, models.BlobReferenceOrData]] = None,
        *,
        url: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if script is None and url is None:
            raise ValueError("One of script or url must be set")
        script_ref = script
        if script is not None and not isinstance(script, models.BlobReferenceOrData):
            script_ref = self.create_blob_reference(script)
        arguments = models.PowershellStageArguments(
            script=script_ref,
            script_url=url,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def powershell_unstage(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.PowershellUnstageArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def process_list(
        self,
        *,
        verbose: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> List[models.Process]:
        arguments = models.ProcessListArguments(verbose=verbose)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ProcessListResults(**task.results.dict())
        if not results.processes:
            raise RTTInvalidResults
        return results.processes

    async def process_powershell(
        self,
        command: str,
        *,
        parent: Optional[str] = None,
        microsoft_only: Optional[bool] = None,
        additional_args: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.ProcessPowershellArguments(
            command=command, parent=parent, microsoft_only=microsoft_only, additional_args=additional_args
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ProcessPowershellResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def process_shell(
        self,
        command: str,
        *,
        parent: Optional[str] = None,
        microsoft_only: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> str:
        arguments = models.ProcessShellArguments(command=command, parent=parent, microsoft_only=microsoft_only)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ProcessShellResults(**task.results.dict())
        if results.output is None:
            raise RTTInvalidResults
        return results.output

    async def process_start(
        self,
        command: str,
        *,
        parent: Optional[str] = None,
        microsoft_only: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ProcessStartArguments(command=command, parent=parent, microsoft_only=microsoft_only)
        await self.create_task_and_wait(arguments, instance=instance)

    async def registry_create(
        self,
        path: str,
        *,
        machine: Optional[str] = None,
        value: Optional[str] = None,
        value_type: Optional[models.RegistryType] = None,
        value_data: Optional[Union[str, bytes]] = None,
        force: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if value_data is not None and isinstance(value_data, bytes):
            if value_type == models.RegistryType.reg_binary:
                value_data = base64.b64encode(value_data)
            else:
                raise ValueError("value_data as bytes can only be used with REG_BINARY")
        arguments = models.RegistryCreateArguments(
            path=path, machine=machine, value=value, vtype=value_type, data=value_data, force=force
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def registry_delete(
        self,
        path: str,
        *,
        machine: Optional[str] = None,
        value: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.RegistryDeleteArguments(path=path, machine=machine, value=value)
        await self.create_task_and_wait(arguments, instance=instance)

    async def registry_query(
        self,
        path: str,
        *,
        machine: Optional[str] = None,
        value: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> Tuple[List[str], List[models.RegistryValue]]:
        arguments = models.RegistryQueryArguments(path=path, machine=machine, value=value)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.RegistryQueryResults(**task.results.dict())
        if results.keys is None or results.values is None:
            raise RTTInvalidResults
        return results.keys, results.values

    async def schtasks_create(
        self,
        task: str,
        command: str,
        user: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        high_privilege: Optional[bool] = None,
        hidden: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ScheduledTaskCreateArguments(
            task=task,
            command=command,
            user=user,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
            high_privilege=high_privilege,
            hidden=hidden,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def schtasks_create_ex(
        self,
        task: str,
        xml: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        xml_ref = self.create_blob_reference(xml.encode())
        arguments = models.ScheduledTaskCreateExArguments(
            task=task,
            xml=xml_ref,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def schtasks_delete(
        self,
        task: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ScheduledTaskDeleteArguments(
            task=task,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def schtasks_query(
        self,
        task: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> Tuple[List[str], List[models.TaskInfo]]:
        arguments = models.ScheduledTaskQueryArguments(
            task=task,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
        )
        task_ = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ScheduledTaskQueryResults(**task_.results.dict())
        if results.folders is None or results.tasks is None:
            raise RTTInvalidResults
        return results.folders, results.tasks

    async def schtasks_start(
        self,
        task: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ScheduledTaskStartArguments(
            task=task,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def schtasks_stop(
        self,
        task: str,
        *,
        machine: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        folder: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ScheduledTaskStopArguments(
            task=task,
            machine=machine,
            username=username,
            password=password,
            folder=folder,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def screenshot_raw(
        self,
        *,
        quality: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> models.BlobReferenceOrData:
        arguments = models.ScreenshotArguments(
            quality=quality,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ScreenshotResults(**task.results.dict())
        if results.data is None:
            raise RTTInvalidResults
        return results.data

    async def screenshot(
        self,
        *,
        quality: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> bytes:
        data_ref = await self.screenshot_raw(quality=quality, instance=instance)
        return self.resolve_blob_reference(data_ref)

    async def service_create(
        self,
        service: str,
        command: str,
        *,
        machine: Optional[str] = None,
        display_name: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceCreateArguments(
            service=service, command=command, machine=machine, display_name=display_name
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def service_create_ex(
        self,
        config: models.ServiceConfigInCreate,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceCreateExArguments(config=config, machine=machine)
        await self.create_task_and_wait(arguments, instance=instance)

    async def service_modify(
        self,
        service: str,
        config: models.ServiceConfigInResponse,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceModifyArguments(service=service, config=config, machine=machine)
        await self.create_task_and_wait(arguments, instance=instance)

    async def service_delete(
        self,
        service: str,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceDeleteArguments(service=service, machine=machine)
        await self.create_task_and_wait(arguments, instance=instance)

    async def service_query(
        self,
        service: str,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> models.ServiceConfigInResponse:
        arguments = models.ServiceQueryArguments(service=service, machine=machine)
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ServiceQueryResults(**task.results.dict())
        if results.config is None:
            raise RTTInvalidResults
        return results.config

    async def service_start(
        self,
        service: str,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceStartArguments(service=service, machine=machine)
        await self.create_task_and_wait(arguments, instance=instance)

    async def service_stop(
        self,
        service: str,
        *,
        machine: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ServiceStopArguments(service=service, machine=machine)
        await self.create_task_and_wait(arguments, instance=instance)

    async def share_add(
        self,
        path: str,
        *,
        username: Optional[str] = None,
        password: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ShareAddArguments(path=path, username=username, password=password)
        await self.create_task_and_wait(arguments, instance=instance)

    async def share_delete(
        self,
        path: str,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.ShareDeleteArguments(path=path)
        await self.create_task_and_wait(arguments, instance=instance)

    async def share_list(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> List[models.ShareInfo]:
        arguments = models.ShareListArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.ShareListResults(**task.results.dict())
        if results.shares is None:
            raise RTTInvalidResults
        return results.shares

    async def smb_stage(
        self,
        host: str,
        payload: Union[bytes, PathLike, str, BlobReference],
        *,
        migrate: Optional[str] = None,
        pipe: Optional[str] = None,
        convert: Optional[bool] = None,
        timeout: Optional[int] = None,
        srdi_exported_function: Optional[str] = None,
        srdi_user_data: Optional[bytes] = None,
        srdi_flags: Optional[int] = None,
        instance: OptionalInstance = None,
    ) -> None:
        if isinstance(payload, (models.BlobReferenceOrData, models.BlobReferenceOrPayloadOrData)):
            payload_ref = payload
        else:
            payload_ref = self.create_blob_or_payload_reference(payload)
        arguments = models.SmbStageArguments(
            host=host,
            payload=payload_ref,
            migrate=migrate,
            pipe=pipe,
            convert=convert,
            timeout=timeout,
            srdi_exported_function=srdi_exported_function,
            srdi_user_data=srdi_user_data,
            srdi_flags=srdi_flags,
        )
        await self.create_task_and_wait(arguments, instance=instance)

    async def smb_send_to_pipe_raw(
        self,
        host: str,
        pipe: str,
        data: Union[bytes, PathLike, str, models.BlobReferenceOrData],
        *,
        timeout: Optional[int] = None,
        compress: Optional[bool] = None,
        wait: Optional[bool] = None,
        encryption_key: Optional[bytes] = None,
        instance: OptionalInstance = None,
    ) -> Optional[models.BlobReferenceOrData]:
        if isinstance(data, models.BlobReferenceOrData):
            blob_ref = data
        else:
            blob_ref = self.create_blob_reference(data)
        arguments = models.NamedPipeSendArguments(
            host=host,
            pipe=pipe,
            data=blob_ref,
            timeout=timeout,
            compress=compress,
            wait=wait,
            encryption_key=encryption_key,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.NamedPipeSendResults(**task.results.dict())
        if wait and results.response is None:
            raise RTTInvalidResults
        return results.response

    async def smb_send_to_pipe(
        self,
        host: str,
        pipe: str,
        data: Union[bytes, PathLike, str, models.BlobReferenceOrData],
        *,
        timeout: Optional[int] = None,
        compress: Optional[bool] = None,
        wait: Optional[bool] = None,
        encryption_key: Optional[bytes] = None,
        instance: OptionalInstance = None,
    ) -> Optional[bytes]:
        response_ref = await self.smb_send_to_pipe_raw(
            host,
            pipe,
            data,
            timeout=timeout,
            compress=compress,
            wait=wait,
            encryption_key=encryption_key,
            instance=instance,
        )
        if wait:
            if response_ref is not None:
                return self.resolve_blob_reference(response_ref)
            else:
                raise RTTInvalidResults

    async def token_logon(
        self,
        username: str,
        password: str,
        *,
        netonly: Optional[bool] = None,
        store: Optional[bool] = None,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.TokenLogonArguments(username=username, password=password, netonly=netonly, store=store)
        await self.create_task_and_wait(arguments, instance=instance)

    async def token_privileges(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> List[models.SePrivilege]:
        arguments = models.TokenPrivilegesArguments()
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.TokenPrivilegesResults(**task.results.dict())
        if results.privileges is None:
            raise RTTInvalidResults
        return results.privileges

    async def token_revert(
        self,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.TokenRevertArguments()
        await self.create_task_and_wait(arguments, instance=instance)

    async def token_steal(
        self,
        process: Union[str, int] = None,
        *,
        instance: OptionalInstance = None,
    ) -> None:
        arguments = models.TokenStealArguments(process=str(process))
        await self.create_task_and_wait(arguments, instance=instance)

    async def wmi_instance_call(
        self,
        method: str,
        filter: str,
        parameters: Dict[str, Any],
        *,
        machine: Optional[str] = None,
        namespace: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authority: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> Dict[str, Any]:
        arguments = models.WmiInstanceCallArguments(
            method=method,
            filter=filter,
            parameters=parameters,
            machine=machine,
            namespace=namespace,
            username=username,
            password=password,
            authority=authority,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.WmiInstanceCallResults(**task.results.dict())
        if results.results is None:
            raise RTTInvalidResults
        return results.results

    async def wmi_process_create(
        self,
        command: str,
        *,
        machine: Optional[str] = None,
        namespace: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authority: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> Dict[str, Any]:
        arguments = models.WmiProcessCreateArguments(
            command=command,
            machine=machine,
            namespace=namespace,
            username=username,
            password=password,
            authority=authority,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.WmiProcessCreateResults(**task.results.dict())
        if results.results is None:
            raise RTTInvalidResults
        return results.results

    async def wmi_query(
        self,
        filter: str,
        *,
        machine: Optional[str] = None,
        namespace: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authority: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> List[Dict[str, Any]]:
        arguments = models.WmiQueryArguments(
            filter=filter,
            machine=machine,
            namespace=namespace,
            username=username,
            password=password,
            authority=authority,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.WmiQueryResults(**task.results.dict())
        if results.results is None:
            raise RTTInvalidResults
        return results.results

    async def wmi_static_call(
        self,
        method: str,
        class_name: str,
        parameters: Dict[str, Any],
        *,
        machine: Optional[str] = None,
        namespace: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authority: Optional[str] = None,
        instance: OptionalInstance = None,
    ) -> Dict[str, Any]:
        arguments = models.WmiStaticCallArguments(
            method=method,
            parameters=parameters,
            machine=machine,
            namespace=namespace,
            username=username,
            password=password,
            authority=authority,
            class_=class_name,
        )
        task = await self.create_task_and_wait(arguments, instance=instance)
        results = models.WmiStaticCallResults(**task.results.dict())
        if results.results is None:
            raise RTTInvalidResults
        return results.results
