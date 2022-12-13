from __future__ import annotations

import logging

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
