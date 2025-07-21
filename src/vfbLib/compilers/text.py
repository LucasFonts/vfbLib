from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler


class NameRecordsCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        self.write_value(len(data))  # number of records
        for nr in data:
            nameID, platID, encID, langID, name = nr
            self.write_value(nameID)
            self.write_value(platID)
            self.write_value(encID)
            self.write_value(langID)
            self.write_value(len(name))
            for char in name:
                if platID == 1 and encID == 0:
                    try:
                        char = char.encode("macroman")
                    except ValueError:
                        char = "?"
                o = ord(char)
                self.write_value(o)


class OpenTypeStringCompiler(BaseCompiler):
    """
    A compiler that compiles string data that represents OpenType feature code.
    """

    def _compile(self, data: Any) -> None:
        self.write_str("\n".join(data))


class StringCompiler(BaseCompiler):
    """
    A compiler that compiles string data.
    """

    def _compile(self, data: Any) -> None:
        self.write_str(data)


class VendorIdCompiler(BaseCompiler):
    """
    A compiler that compiles string data, padded to 4 bytes.
    """

    def _compile(self, data: Any) -> None:
        self.write_str(data, pad=4)
