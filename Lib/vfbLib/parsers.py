from base64 import b64encode, standard_b64encode
uint8 = 1
uint16 = 2
uint32 = 4


class BaseParser:
    """
    Base class to read data from a vfb file
    """

    @classmethod
    def parse(cls, data):
        return str(b64encode(data))

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


class GlyphEncodingParser(BaseParser):
    @classmethod
    def parse(cls, data):
        gid = int.from_bytes(data[:2], byteorder="little")
        nam = data[2:].decode("ascii")
        return gid, nam


class StringParser(BaseParser):
    """
    A parser that reads data as ASCII-encoded strings.
    """

    @classmethod
    def parse(cls, data):
        return data.decode("cp1252")
        return data.decode("Windows-1252")


class VfbHeaderParser(BaseParser):
    @classmethod
    def parse(cls, data):
        cls.data = data
        header = []
        header.append({"filetype": str(data.read(6))})
        header.append({"header1": cls.read_uint16()})
        header.append({"header2": cls.read_uint16()})
        header.append({"reserved": str(data.read(34))})
        header.append({"header3": cls.read_uint32()})
        header.append({"header4": cls.read_uint32()})
        for i in range(5, 12):
            header.append({f"header{i}": cls.read_uint16()})

        return header
