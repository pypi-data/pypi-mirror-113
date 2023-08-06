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

import copy
import re
import struct
from typing import Any, Dict, List, Union

import pefile
from rtt_sdk.models import Architecture, FileOrDirectory, Process, TaskDelivery, TaskStatus

# Read_Only | Initialized_Data
DEFAULT_CHARACTERISTICS = 0x40000040
SECTION_NAME = 8
MACHINE_IA64 = 512
MACHINE_AMD64 = 34404


def _align_up(value: int, align: int = 0x1000) -> int:
    return (value + align - 1) & ~(align - 1)


def _is_64bit_dll(data: bytes) -> bool:
    header_offset = struct.unpack("<L", data[60:64])[0]
    machine = struct.unpack("<H", data[header_offset + 4 : header_offset + 4 + 2])[0]
    if machine == MACHINE_IA64 or machine == MACHINE_AMD64:
        return True
    return False


def _add_section(pe: pefile.PE, name: str, size: int, characteristics: int = DEFAULT_CHARACTERISTICS):

    # Sanity checks

    if len(name) > SECTION_NAME:
        raise ValueError("Section name is too long")

    section_header_size = pefile.Structure(pefile.PE.__IMAGE_SECTION_HEADER_format__).sizeof()
    section_header_off = pe.sections[-1].get_file_offset() + section_header_size
    if section_header_off + section_header_size > pe.OPTIONAL_HEADER.SizeOfHeaders:  # type: ignore
        raise ValueError("Not enough room for another SECTION_HEADER")

    # Calculate/Align sizes
    virtual_size = _align_up(size, pe.OPTIONAL_HEADER.SectionAlignment)  # type: ignore
    virtual_addr = _align_up(
        pe.sections[-1].VirtualAddress + pe.sections[-1].Misc_VirtualSize,
        pe.OPTIONAL_HEADER.SectionAlignment,  # type: ignore
    )

    raw_size = _align_up(size, pe.OPTIONAL_HEADER.FileAlignment)  # type: ignore
    raw_ptr = _align_up(
        pe.sections[-1].PointerToRawData + pe.sections[-1].SizeOfRawData,
        pe.OPTIONAL_HEADER.FileAlignment,  # type: ignore
    )

    # Configure section properties
    section = pefile.SectionStructure(pe.__IMAGE_SECTION_HEADER_format__, pe=pe)
    section.set_file_offset(section_header_off)
    section.Name = name.encode().ljust(SECTION_NAME, b"\x00")
    section.VirtualAddress = virtual_addr
    section.PointerToRawData = raw_ptr
    section.Misc = section.Misc_VirtualSize = virtual_size
    section.SizeOfRawData = raw_size
    section.Characteristics = characteristics

    section.PointerToRelocations = 0
    section.NumberOfRelocations = 0
    section.NumberOfLinenumbers = 0
    section.PointerToLinenumbers = 0

    # Correct headers
    pe.FILE_HEADER.NumberOfSections += 1  # type: ignore
    pe.OPTIONAL_HEADER.SizeOfImage = virtual_addr + virtual_size  # type: ignore

    # Add buffer padding
    pe.__data__ += b"\x00" * raw_size

    # Append to ensure overwrite
    pe.__structures__.append(section)

    # Recreate to save our changes
    pe = pefile.PE(data=pe.write())

    return pe, section


def _clone_exports(tgt: pefile.PE, ref: pefile.PE, ref_path: str, new_section_name: str = ".rdata2"):

    # Forwards typically don't supply the extension
    ref_path = ref_path.replace(".dll", "")

    ref = copy.deepcopy(ref)
    tgt = copy.deepcopy(tgt)

    ref_export_dir = ref.OPTIONAL_HEADER.DATA_DIRECTORY[0]  # type: ignore

    if not ref_export_dir.Size:
        raise ValueError("Reference binary has no exports")

    exp_names = [
        ref_path.encode() + b"." + e.name if e.name else ref_path.encode() + b".#" + str(e.ordinal).encode()
        for e in sorted(ref.DIRECTORY_ENTRY_EXPORT.symbols, key=lambda x: x.ordinal)  # type: ignore
    ]
    exp_names_blob = b"\x00".join(exp_names) + b"\x00"

    new_section_size = ref_export_dir.Size + len(exp_names_blob)

    tgt, section = _add_section(tgt, new_section_name, new_section_size)
    final_rva = section.VirtualAddress  # type: ignore

    # Capture the reference export directory
    export_dir = ref.__unpack_data__(
        pefile.PE.__IMAGE_EXPORT_DIRECTORY_format__,
        ref.get_data(
            ref_export_dir.VirtualAddress, pefile.Structure(pefile.PE.__IMAGE_EXPORT_DIRECTORY_format__).sizeof()
        ),
        file_offset=0,  # we don't need this
    )

    # Calculate our delta
    delta = final_rva - ref_export_dir.VirtualAddress

    # Apply RVA delta to export names
    for i in range(export_dir.NumberOfNames):  # type: ignore
        ref.set_dword_at_rva(
            export_dir.AddressOfNames + 4 * i,  # type: ignore
            ref.get_dword_at_rva(export_dir.AddressOfNames + 4 * i) + delta,  # type: ignore
        )

    # Link function addresses to forward names
    forward_offset = ref_export_dir.VirtualAddress + ref_export_dir.Size + delta
    true_offset = 0

    for i in range(export_dir.NumberOfFunctions):  # type: ignore

        if not ref.get_dword_at_rva(export_dir.AddressOfFunctions + 4 * i):  # type: ignore
            continue  # This function is hollow (never used)

        forward_name = exp_names[true_offset]
        ref.set_dword_at_rva(export_dir.AddressOfFunctions + 4 * i, forward_offset)  # type: ignore
        forward_offset += len(forward_name) + 1  # +1 for null byte
        true_offset += 1

    # Apply RVA delta to directory
    export_dir.AddressOfFunctions += delta  # type: ignore
    export_dir.AddressOfNames += delta  # type: ignore
    export_dir.AddressOfNameOrdinals += delta  # type: ignore

    # Write in our new export directory
    tgt.set_bytes_at_rva(final_rva, ref.get_data(ref_export_dir.VirtualAddress, ref_export_dir.Size) + exp_names_blob)
    tgt.set_bytes_at_rva(final_rva, export_dir.__pack__())

    # Rebuild from bytes to save back
    tgt = pefile.PE(data=tgt.__data__)

    # Update directory specs
    tgt_export_dir = tgt.OPTIONAL_HEADER.DATA_DIRECTORY[0]  # type: ignore
    tgt_export_dir.VirtualAddress = section.VirtualAddress  # type: ignore
    tgt_export_dir.Size = new_section_size
    tgt = pefile.PE(data=tgt.write())

    return tgt


def recurse_encode_bytes(d: Any, encoding: str = "utf-8"):
    if isinstance(d, dict):
        x = {}
        for k, v in d.items():
            if isinstance(v, (dict, list)):
                v = recurse_encode_bytes(v)
            elif isinstance(v, bytes):
                v = v.decode(encoding)
            x[k] = v
        return x
    elif isinstance(d, list):
        x = []
        for v in d:
            if isinstance(v, (dict, list)):
                v = recurse_encode_bytes(v)
            elif isinstance(v, bytes):
                v = v.decode(encoding)
            x.append(v)
        return x
    return d


def clone_exports(tgt_bytes: bytes, ref_bytes: bytes, ref_path: str, new_section_name: str = ".rdata2") -> bytes:
    """
    Clones the export table from one (reference) DLL to another (target) DLL.
    Functionality will be proxied using export fowarding.

    :param byte tgt_bytes: Target PE bytes for cloning
    :param byte ref_bytes: Reference PE bytes to clone from
    :param str ref_path: Path of the reference library during the hijack
    :param str new_section_name: PE section name if a new section is required (Default = '.rdata2')

    :returns: Updated PE bytes
    :rtype: bytes
    """

    cloned_pe = _clone_exports(pefile.PE(data=tgt_bytes), pefile.PE(data=ref_bytes), ref_path, new_section_name)
    return cloned_pe.write() or b""


def convert_path_for_architecture(arch: Architecture, path: str) -> str:
    match = re.findall(r"\\([fF]ramework(?:64)?)\\", path)
    if match:
        if arch == Architecture.x64:
            path = path.replace(match[0], "Framework64")
        elif arch == Architecture.x86:
            path = path.replace(match[0], "Framework")
        else:
            raise ValueError("Could not convert path")
    else:
        path = path.replace("x86", arch.value)
        path = path.replace("x64", arch.value)
    return path


def invert_architecture(arch: Architecture):
    if arch == Architecture.x64:
        return Architecture.x86
    elif arch == Architecture.x86:
        return Architecture.x64
    else:
        raise ValueError("Could not invert architecture")


def architecture_from_directory(directory: Union[str, Dict[str, Any], List[str], List[FileOrDirectory]]):
    """
    Derive architecture from a directory listing (usually C:\\)
    """
    if isinstance(directory, dict):
        directory = list(directory.keys())
    elif all(isinstance(x, FileOrDirectory) for x in directory):
        directory = [f.name for f in directory]  # type: ignore

    if "Program Files (x86)" in directory:
        return Architecture.x64
    elif "Program Files" in directory:
        return Architecture.x86
    raise ValueError("Dir does not look like a root directory listing")


def architecture_from_process_list(ps: Union[str, List[Process]]):
    """
    Derive architecture from a process listing
    """
    if isinstance(ps, str):
        if " x64 " in ps:
            return Architecture.x64
        elif " x86 " in ps:
            return Architecture.x86
    else:
        if [p for p in ps if p.arch == Architecture.x64]:
            return Architecture.x64
        elif [p for p in ps if p.arch == Architecture.x86]:
            return Architecture.x86
    raise ValueError("ps does not look like a process list")


def architecture_from_pe_bytes(pe_bytes: bytes):
    """
    Derive architecture from PE file bytes
    """
    if pe_bytes[:2] != b"MZ":
        raise ValueError("File does not look like a PE")
    return Architecture.x64 if _is_64bit_dll(pe_bytes) else Architecture.x86


def architecture_from_pe_path(pe_path: str):
    """
    Derive architecture from a local PE file
    """
    return architecture_from_pe_bytes(open(pe_path, "rb").read())


def is_task_finished(delivery: TaskDelivery) -> bool:
    return delivery in [TaskDelivery.completed, TaskDelivery.blocked, TaskDelivery.invalid]


def is_task_failed(status: TaskStatus) -> bool:
    return status in [TaskStatus.failure, TaskStatus.warning, TaskStatus.critical]
