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

# type: ignore

import io
import os
import sys
from typing import Union

import colorful as cf


def log(message: Union[bytes, str], sameline=False):
    if isinstance(message, str):
        message = message.encode()

    if not sameline:
        message = b"\r" + message + b"\r\n"

    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(message)
    elif isinstance(sys.stdout, io.BufferedIOBase):
        sys.stdout.write(message)
    else:
        sys.stdout.write(f"\r{cf.red}[!]{cf.reset} stdout write error\r\n")

    try:
        sys.stdout.flush()
    except Exception:
        pass


def shout(message: str):
    log(f"{cf.cyan}[RTT]{cf.reset} {message}")


def warn(message: str):
    log(f"{cf.yellow}[-]{cf.reset} {message}")


def error(message: str):
    log(f"{cf.red}[!]{cf.reset} {message}")


def success(message: str):
    log(f"{cf.green}[+]{cf.reset} {message}")


def newline():
    log("", sameline=False)


def debug(message: str):
    if os.environ.get("DEBUG", False):
        log(f"{cf.blue}[DBG]{cf.reset} {message}")
