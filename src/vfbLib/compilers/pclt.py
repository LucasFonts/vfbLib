from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import PCLTDict


class PcltCompiler(BaseCompiler):
    def _compile(self, data: "PCLTDict") -> None:
        self.write_value(data["font_number"], signed=False)
        for k in (
            "pitch",
            "x_height",
            "style",
            "type_family",
            "cap_height",
            "symbol_set",
        ):
            self.write_value(data[k])
        self.write_str(data["typeface"], 16)
        for value in data["character_complement"]:
            self.write_uint8(value)
        self.write_str(data["file_name"], 6)
        self.write_uint8(data["stroke_weight"])
        self.write_uint8(data["width_type"])
        self.write_uint8(data["serif_style"])
