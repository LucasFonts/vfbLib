
from io import BufferedReader
from vfbLib.parsers import BaseParser, read_encoded_value


class VfbHeaderParser(BaseParser):
    @classmethod
    def parse(cls, data: BufferedReader):
        cls.data = data
        header = {}
        header["header0"] = cls.read_uint8()
        header["filetype"] = data.read(5).decode("cp1252")
        header["header1"] = cls.read_uint16()
        header["header2"] = cls.read_uint16()
        header["reserved"] = str(data.read(34))
        header["header3"] = cls.read_uint16()
        header["header4"] = cls.read_uint16()
        header["header5"] = cls.read_uint16()
        header["header6"] = cls.read_uint16()
        header["header7"] = cls.read_uint16()
        header["header8"] = cls.read_uint16()
        for i in range(9, 12):
            key = cls.read_uint8()
            val = read_encoded_value(data)
            header[f"header{i}"] = {key: val}
        header["header13"] = cls.read_uint16()
        header["header14"] = cls.read_uint16()
        header["header15"] = cls.read_uint8()

        return header
