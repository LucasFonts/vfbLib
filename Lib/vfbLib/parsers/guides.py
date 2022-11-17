from typing import List
from vfbLib.parsers import BaseParser, read_encoded_value


class GlobalGuidesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        stream = cls.stream
        guides = []
        num_h = read_encoded_value(stream)
        print(num_h, "horizontal")
        for _ in range(num_h):  # FIXME: * num_masters
            x = 0
            y = read_encoded_value(stream)
            angle = read_encoded_value(stream, signed=True)

            guides.append(dict(x=x, y=y, angle=angle))
        
        num_v = read_encoded_value(stream)
        print(num_v, "vertical")
        for _ in range(num_v):
            x = read_encoded_value(stream)
            y = 0
            angle = read_encoded_value(stream, signed=True)

            guides.append(dict(x=x, y=y, angle=angle))

        assert stream.read() == b""
        return guides


class GlobalGuidePropertiesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        stream = cls.stream
        guides = []
        for _ in range(2):
            while True:
                index = read_encoded_value(stream)
                if index == 0:
                    break

                g = dict(index=index)

                color = read_encoded_value(stream)
                if color > -1:
                    g["color"] = "#" + hex(color & ~0xff00000000)[2:]

                name_length = read_encoded_value(stream)
                if name_length > 0:
                    name = cls.stream.read(name_length).decode("cp1252")
                    g["name"] = name

                guides.append(g)

        assert stream.read() == b""
        return guides
