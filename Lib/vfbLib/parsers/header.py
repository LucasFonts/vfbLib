import logging
from io import BufferedReader
from typing import Any

from fontTools.misc.textTools import hexStr

from vfbLib.parsers.base import read_value, uint8, uint16

logger = logging.getLogger(__name__)


class VfbHeaderParser:
    def __init__(self, stream: BufferedReader) -> None:
        self.stream: BufferedReader = stream

    def parse(self) -> dict[str, Any]:
        header: dict[str, Any] = {}
        header["header0"] = self.read_uint8()
        header["filetype"] = self.stream.read(5).decode("cp1252")
        header["header1"] = self.read_uint16()
        header["header2"] = self.read_uint16()
        header["reserved"] = hexStr(self.stream.read(34).decode("ascii"))
        header["header3"] = self.read_uint16()
        header["header4"] = self.read_uint16()
        header["header5"] = self.read_uint16()
        header["header6"] = self.read_uint16()
        header["header7"] = self.read_uint16()
        if header["header7"] == 10:
            # FL5 additions over FL3
            header["header8"] = self.read_uint16()
            for i in range(9, 12):
                key = self.read_uint8()
                val = self.read_value()
                header[f"header{i}"] = {str(key): val}
            header["header12"] = self.read_uint8()
            header["header13"] = self.read_uint16()
        else:
            header["header13"] = header["header7"]
            del header["header7"]
        header["header14"] = self.read_uint16()

        return header

    def read_uint8(self) -> int:
        return int.from_bytes(self.stream.read(uint8), byteorder="little", signed=False)

    def read_uint16(self) -> int:
        return int.from_bytes(
            self.stream.read(uint16), byteorder="little", signed=False
        )

    def read_value(self):
        return read_value(self.stream)
