uint8 = 1
uint16 = 2
uint32 = 4


class BaseParser:
    """
    Base class to read data from a vfb file
    """

    pass


class StringParser(BaseParser):
    """
    A parser that reads data as ASCII-encoded strings.
    """

    pass


class VfbHeaderParser(BaseParser):
    @classmethod
    def parse(cls, data):
        header = []
        header.append({"filetype": data.read(6).encode("utf-8")})
        header.append({"header1": data.read(uint16)})
        header.append({"header2": data.read(uint16)})
        header.append({"reserved": data.read(34)})
        header.append({"header3": data.read(uint32)})
        header.append({"header4": data.read(uint32)})
        for i in range(1, 8):
            header.append({f"header{i}": data.read(uint16)})

        return header
