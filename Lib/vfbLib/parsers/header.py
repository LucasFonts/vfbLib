from __future__ import annotations

import logging

from io import BufferedReader
from typing import Any, Dict
from vfbLib.parsers import read_encoded_value, uint8, uint16


logger = logging.getLogger(__name__)


class VfbHeaderParser:
    stream: BufferedReader | None = None

    @classmethod
    def parse(cls, stream: BufferedReader):
        cls.stream = stream
        header: Dict[str, Any] = {}
        header["header0"] = cls.read_uint8()
        header["filetype"] = cls.stream.read(5).decode("cp1252")
        header["header1"] = cls.read_uint16()
        header["header2"] = cls.read_uint16()
        header["reserved"] = str(cls.stream.read(34))
        header["header3"] = cls.read_uint16()
        header["header4"] = cls.read_uint16()
        header["header5"] = cls.read_uint16()
        header["header6"] = cls.read_uint16()
        header["header7"] = cls.read_uint16()
        header["header8"] = cls.read_uint16()
        for i in range(9, 12):
            key = cls.read_uint8()
            val = read_encoded_value(stream)
            header[f"header{i}"] = {key: val}

        header["header12"] = cls.read_uint16()
        header["header13"] = cls.read_uint16()
        header["header14"] = cls.read_uint8()

        return header

    @classmethod
    def read_uint8(cls) -> int:
        assert cls.stream is not None
        return int.from_bytes(cls.stream.read(uint8), byteorder="little", signed=False)

    @classmethod
    def read_uint16(cls) -> int:
        assert cls.stream is not None
        return int.from_bytes(cls.stream.read(uint16), byteorder="little", signed=False)
