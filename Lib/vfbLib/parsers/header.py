import logging
from io import BufferedReader, BytesIO
from typing import Any

from vfbLib.parsers.base import StreamReader

logger = logging.getLogger(__name__)


class VfbHeaderParser(StreamReader):
    def __init__(self, stream: BufferedReader) -> None:
        self.stream: BufferedReader = stream

    def parse(self) -> dict[str, Any]:
        header: dict[str, Any] = {}
        header["header0"] = self.read_uint8()
        header["filetype"] = self.read_str(5)
        header["header1"] = self.read_uint16()
        size = self.read_uint16()
        chunk1 = []
        for _ in range(size):
            chunk1.append(self.read_uint8())
        header["chunk1"] = chunk1
        if chunk1[-2:] == [10, 0]:
            # FL4+ additions over FL3
            size = self.read_uint16()
            fl4_chunk = self.stream.read(size)
            sr = StreamReader()
            sr.stream = BytesIO(fl4_chunk)
            app_info = {}
            while True:
                key = sr.read_uint8()
                if key == 0:
                    break
                value = sr.read_value()
                if key == 2:
                    # app version
                    app_version = []
                    for i in (24, 16, 8, 0):
                        # Extract the bytes from the number again
                        app_version.append(value >> i & 0xFF)
                    app_info[str(key)] = app_version
                else:
                    app_info[str(key)] = value
            header["creator"] = app_info
            # Two bytes follow that are at the end of chunk1 in the older format
            header["end0"] = self.read_uint8()  # 6
            header["end1"] = self.read_uint8()  # 1
        else:
            # TODO: Just upgrade the header to the newer format?
            # chunk1[-2:] = [10, 0]
            # header["creator"] = {
            #     "1": 1,
            #     "2": [5, 2, 2, 128],
            #     "3": 0,
            # }
            # header["end0"] = 6
            # header["end1"] = 1
            pass
        # The common 0 word at the end of the header
        header["end2"] = self.read_uint16()

        return header
