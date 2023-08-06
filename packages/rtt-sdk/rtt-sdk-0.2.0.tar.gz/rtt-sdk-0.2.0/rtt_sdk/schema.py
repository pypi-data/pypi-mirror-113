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

import datetime
from typing import TYPE_CHECKING

import fastapi.openapi.models
from pydantic import BaseConfig, BaseModel, validator
from pydantic.main import Extra

RUNTIME = not TYPE_CHECKING
if RUNTIME:

    def dataclass(model):
        return model


else:
    from dataclasses import dataclass


autocomplete = dataclass

# Allow custom field additions in schema objects (x-thing)
fastapi.openapi.models.SchemaBase.__config__.extra = Extra.allow


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class Schema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        alias_generator = convert_field_to_camel_case

    @validator("*", pre=True)
    def not_none(cls, v, field):
        if field.default is not None and v is None:
            return field.default
        else:
            return v
