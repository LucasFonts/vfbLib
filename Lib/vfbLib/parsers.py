from fontTools.misc.textTools import hexStr
from io import BytesIO
from struct import unpack
from typing import List

uint8 = 1
uint16 = 2
uint32 = 4


class BaseParser:
    """
    Base class to read data from a vfb file
    """

    @classmethod
    def parse(cls, data):
        return hexStr(data)

    @classmethod
    def read_uint8(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint8), byteorder="little", signed=False
        )

    @classmethod
    def read_uint16(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint16), byteorder="little", signed=False
        )

    @classmethod
    def read_uint32(cls, stream=None) -> int:
        if stream is None:
            stream = cls.data
        return int.from_bytes(
            stream.read(uint32), byteorder="little", signed=False
        )


class GaspParser(BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    @classmethod
    def parse(cls, data):
        gasp = unpack(f"<{len(data) // 2}H", data)
        it = iter(gasp)
        return [
            {
                "maxPpem": a,
                "flags": b,
            }
            for a, b in zip(it, it)
        ]


class GlyphEncodingParser(BaseParser):
    @classmethod
    def parse(cls, data):
        gid = int.from_bytes(data[:2], byteorder="little")
        nam = data[2:].decode("ascii")
        return gid, nam


class GlyphParser(BaseParser):
    @classmethod
    def parse(cls, data):
        s = BytesIO(data)
        start = unpack("<5B", s.read(5))
        glyph_name_length = int.from_bytes(s.read(1), byteorder="little") - 0x8B
        glyph_name = s.read(glyph_name_length)
        # whatever: List[int | List[int]] = [int.from_bytes(s.read(1), byteorder="little")]  # 0x08
        # arr = []
        # print("Begin")
        # while True:
        #     val = int.from_bytes(s.read(1), byteorder="little")
        #     print("   ", hex(val))
        #     print("   ", whatever)
        #     if val == 0x0F:
        #         break
        #     # num_values = val - 0x8B
        #     # if num_values == 0:
        #     #     arr.append(0)
        #     #     whatever.append(arr)
        #     #     continue

        #     # for i in range(num_values):
        #     #     print(f"        Read value {i}")
        #     #     val_inner = int.from_bytes(s.read(1), byteorder="little")
        #     #     print("       ", hex(val_inner))
        #     #     arr.append(val_inner- 0x8b)
        #     # whatever.append(arr)
        #     # whatever.append([])
        #     # arr = []
        whatever = hexStr(s.read())
        return [start, glyph_name.decode("cp1252"), whatever]

class IntParser(BaseParser):
    """
    A parser that reads data as UInt16.
    """

    @classmethod
    def parse(cls, data):
        return int.from_bytes(data, byteorder="little", signed=False)


class PanoseParser(BaseParser):
    """
    A parser that reads data as an array representing PANOSE values.
    """

    @classmethod
    def parse(cls, data):
        return unpack("<10b", data)


class SignedIntParser(BaseParser):
    """
    A parser that reads data as signed Int16.
    """

    @classmethod
    def parse(cls, data):
        return int.from_bytes(data, byteorder="little", signed=True)


class StringParser(BaseParser):
    """
    A parser that reads data as ASCII-encoded strings.
    """

    @classmethod
    def parse(cls, data):
        return data.decode("cp1252")


class VfbHeaderParser(BaseParser):
    @classmethod
    def parse(cls, data):
        cls.data = data
        header = []
        header.append({"header0": cls.read_uint8()})
        header.append({"filetype": data.read(5).decode("cp1252")})
        header.append({"header1": cls.read_uint16()})
        header.append({"header2": cls.read_uint16()})
        header.append({"reserved": str(data.read(34))})
        header.append({"header3": cls.read_uint32()})
        header.append({"header4": cls.read_uint32()})
        for i in range(5, 12):
            header.append({f"header{i}": cls.read_uint16()})

        return header
