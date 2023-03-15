from __future__ import annotations

import logging

from typing import Dict, List
from vfbLib.parsers import BaseParser, read_encoded_value


logger = logging.getLogger(__name__)


class NameRecordsParser(BaseParser):
    @classmethod
    def _parse(cls):
        stream = cls.stream
        num = read_encoded_value(stream)
        result = []
        for _ in range(num):
            nameID = read_encoded_value(stream)
            platID = read_encoded_value(stream)
            encID = read_encoded_value(stream)
            langID = read_encoded_value(stream)
            name_length = read_encoded_value(stream)
            name_codes = [read_encoded_value(stream) for _ in range(name_length)]
            name = ""
            for c in name_codes:
                try:
                    char = chr(c)
                    # FIXME: Worth fixing the platform-specific encodings?
                    # if platID == 1 and encID == 0:
                    #     char = char.encode("utf-8").decode("macroman")
                except ValueError:
                    char = "\ufeff"
                name += char
            result.append([nameID, platID, encID, langID, name])

        assert stream.read() == b""
        return result


class OpenTypeClassParser(BaseParser):
    """
    A parser that reads data as a Windows-1252-encoded strings and returns it formatted
    to represent an OpenType class
    """

    @classmethod
    def _parse(cls) -> Dict[str, List[str] | str]:
        s = cls.stream.read().decode("cp1252").strip("\u0000 ")
        if ":" not in s:
            logger.warning(f"Malformed OpenType class: {s}")
            return {"str": s, "err": "PARSE_ERROR"}
            # raise ValueError

        name, contents = s.split(":")

        glyphs = []
        for glyph in contents.split(" "):
            glyph = glyph.strip()
            if glyph:
                glyphs.append(glyph)
        return {"name": name, "glyphs": glyphs}


class OpenTypeStringParser(BaseParser):
    """
    A parser that reads data as a Windows-1252-encoded strings and returns it as a list.
    """

    @classmethod
    def _parse(cls) -> List[str]:
        s = cls.stream.read().decode("cp1252").strip("\u0000 ")
        return s.splitlines()


class StringParser(BaseParser):
    """
    A parser that reads data as Windows-1252-encoded strings.
    """

    @classmethod
    def _parse(cls):
        return cls.stream.read().decode("cp1252").strip("\u0000 ")
