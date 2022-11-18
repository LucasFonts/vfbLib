from __future__ import annotations

from typing import List
from vfbLib.parsers import BaseParser, read_encoded_value


def parse_guides(stream, num_masters) -> List:
    # Common parser for glyph and global guides
    guides = {
        "h": [[] for _ in range(num_masters)],
        "v": [[] for _ in range(num_masters)],
    }
    for d in "hv":
        num_guides = read_encoded_value(stream)
        for i in range(num_guides):
            for m in range(num_masters):
                pos = read_encoded_value(stream)
                angle = read_encoded_value(stream)
                guides[d][m].append(dict(pos=pos, angle=angle))

    return guides


class GlobalGuidesParser(BaseParser):
    @classmethod
    def _parse(cls) -> List:
        guides = parse_guides(cls.stream, cls.master_count)
        assert cls.stream.read() == b""
        return guides


class GuidePropertiesParser(BaseParser):
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
