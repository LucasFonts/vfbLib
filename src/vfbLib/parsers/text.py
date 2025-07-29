from __future__ import annotations

import logging
from re import search

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import FeaturesDict

logger = logging.getLogger(__name__)


class NameRecordsParser(BaseParser):
    def _parse(self) -> list[tuple[int, int, int, int, str]]:
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
            result.append((nameID, platID, encID, langID, name))

        return result


class OpenTypeStringParser(BaseParser):
    """
    A parser that reads data as a strings and returns it as a list.
    """

    @staticmethod
    def build_fea_dict(data: list[str]) -> FeaturesDict:
        """
        Parse the OpenType feature code into a structure that is more manageable. This
        is not used in vfbLib, but may be used in code that wants to read OpenType
        features from a VFB.

        Args:
            data (list[str]): The OpenType feature code (AFDKO syntax) as a list of
                lines.

        Returns:
            dict[str, list[dict]]: The feature code split into prefix and actual
                features.
        """
        fea = FeaturesDict(prefix=[], features=[])
        prefix: list[str] = []
        feature: list[str] = []
        tag = ""
        in_prefix = True
        for line in data:
            if "#" in line:
                code, _ = line.split("#", 1)
            else:
                code = line

            if s := search(r"\s*feature\s*([a-z0-9]{4})\s*\{", code):
                # New feature

                if in_prefix:
                    # Flush the prefix code
                    fea["prefix"] = prefix
                    in_prefix = False
                else:
                    # Flush the previous feature
                    fea["features"].append({"tag": tag, "code": feature})

                tag = s.groups()[0]
                feature = [line]
            elif in_prefix:
                prefix.append(line)
            else:
                feature.append(line)

        # Flush the last feature
        fea["features"].append({"tag": tag, "code": feature})

        return fea

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
        return self.read_str_all().strip("\00")
