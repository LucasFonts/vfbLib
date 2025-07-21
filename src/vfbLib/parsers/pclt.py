from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class PcltParser(BaseParser):
    """
    A parser that reads the PCLT table data
    """

    def _parse(self) -> dict[str, list[int] | int | str]:
        values: dict[str, list[int] | int | str] = {}

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#fontnumber
        values["font_number"] = self.read_value(signed=False)

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#pitch
        values["pitch"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#xheight
        values["x_height"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#style
        values["style"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#typefamily
        values["type_family"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#capheight
        values["cap_height"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#symbolset
        values["symbol_set"] = self.read_value()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#typeface
        values["typeface"] = self.read_str(16)

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#charactercomplement
        values["character_complement"] = [self.read_uint8() for _ in range(8)]

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#filename
        values["file_name"] = self.read_str(6)

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#strokeweight
        values["stroke_weight"] = self.read_int8()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#widthtype
        values["width_type"] = self.read_int8()

        # https://learn.microsoft.com/de-de/typography/opentype/spec/pclt#serifstyle
        values["serif_style"] = self.read_uint8()

        return values
