import logging

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class NameRecordsParser(BaseParser):
    def _parse(self):
        num = self.read_value()
        result = []
        for _ in range(num):
            nameID = self.read_value()
            platID = self.read_value()
            encID = self.read_value()
            langID = self.read_value()
            name_length = self.read_value()
            name_codes = [self.read_value() for _ in range(name_length)]
            name = ""
            for c in name_codes:
                try:
                    char = chr(c)
                    # Fix platform-specific encodings for Mac
                    if platID == 1 and encID == 0:
                        # TODO: Remove default arguments when Python < 3.11 is dropped
                        char = c.to_bytes(length=1, byteorder="big").decode("macroman")
                except ValueError:
                    char = "\ufeff"
                name += char
            result.append([nameID, platID, encID, langID, name])

        return result


class OpenTypeStringParser(BaseParser):
    """
    A parser that reads data as a strings and returns it as a list.
    """

    def _parse(self) -> list[str]:
        s = self.read_str_all()
        # Filter more than 2 consecutive empty lines
        lines = []
        c = 0
        for line in s.splitlines():
            if line.strip():
                c = 0
                lines.append(line)
            else:
                if c < 2:
                    lines.append(line)
                c += 1

        if len(lines) > 1:
            # Remove empty lines at the end, except one
            while not lines[-1]:
                lines.pop()
        lines.append("")
        return lines


class StringParser(BaseParser):
    """
    A parser that reads data as strings.
    """

    def _parse(self):
        return self.read_str_all()
