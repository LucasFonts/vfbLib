from typing import List
from vfbLib.parsers import BaseParser, read_encoded_value


class GlobalGuidesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        stream = cls.stream
        guides = {
            "h": [[] for _ in range(cls.master_count)],
            "v": [[] for _ in range(cls.master_count)],
        }
        for d in "hv":
            num_guides = read_encoded_value(stream)
            for i in range(num_guides):
                for m in range(cls.master_count):
                    pos = read_encoded_value(stream)
                    angle = read_encoded_value(stream)
                    guides[d][m].append(dict(pos=pos, angle=angle))

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
                    g["color"] = "#" + hex(color & ~0xFF00000000)[2:]

                name_length = read_encoded_value(stream)
                if name_length > 0:
                    name = cls.stream.read(name_length).decode("cp1252")
                    g["name"] = name

                guides.append(g)

        assert stream.read() == b""
        return guides
