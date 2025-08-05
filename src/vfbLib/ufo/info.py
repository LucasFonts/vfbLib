from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from ufoLib2.objects.info import Info, WidthClass

from vfbLib.enum import F, T
from vfbLib.helpers import binaryToIntList
from vfbLib.ufo.time import convert_timestamp
from vfbLib.ufo.typing import TUfoGaspRecDict

if TYPE_CHECKING:
    from vfbLib.typing import GaspList
    from vfbLib.ufo.typing import UfoGuide


logger = logging.getLogger(__name__)


# maxp_keys = {
#     "max_zones": "maxZones",
#     "max_twilight_points": "maxTwilightPoints",
#     "max_storage": "maxStorage",
#     "max_function_defs": "maxFunctionDefs",
#     "max_instruction_defs": "maxInstructionDefs",
#     "max_stack_elements": "maxStackElements",
# }


class VfbToUfoInfo(Info):
    def __init__(self) -> None:
        super().__init__()
        # Chance to set some defaults that should always be written
        self.familyName = "Untitled"
        self.guidelines: list[UfoGuide] = []
        self.italicAngle: float | int = 0
        self.openTypeGaspRangeRecords: list[TUfoGaspRecDict] = []
        self.openTypeHeadCreated: str | None = None
        self.openTypeHeadFlags: list[int] = []
        self.openTypeHheaLineGap = 0
        self.openTypeHeadLowestRecPPEM = 0
        self.openTypeNameDescription = ""
        self.openTypeNamePreferredFamilyName = ""
        self.openTypeNamePreferredSubfamilyName = ""
        self.openTypeNameRecords: list | None = None
        self.openTypeNameSampleText = ""
        self.openTypeOS2FamilyClass = [0, 0]
        self.openTypeOS2Selection: list[int] = []
        self.openTypeOS2SubscriptXSize = 0
        self.openTypeOS2SubscriptYSize = 0
        self.openTypeOS2SubscriptXOffset = 0
        self.openTypeOS2SubscriptYOffset = 0
        self.openTypeOS2SuperscriptXSize = 0
        self.openTypeOS2SuperscriptYSize = 0
        self.openTypeOS2SuperscriptXOffset = 0
        self.openTypeOS2SuperscriptYOffset = 0
        self.openTypeOS2StrikeoutPosition = 0
        self.openTypeOS2StrikeoutSize = 0
        self.openTypeOS2Type: list[int] = []
        self.openTypeOS2UnicodeRanges: list[int] | None = []
        self.openTypeOS2WeightClass = 400
        self.openTypeOS2WidthClass = WidthClass(5)
        self.postscriptBlueValues: list[float] | None = []
        self.postscriptDefaultWidthX: float | None = None
        self.postscriptFamilyBlues: list[float] | None = []
        self.postscriptFamilyOtherBlues: list[float] | None = []
        self.postscriptFontName = "Untitled-Regular"
        self.postscriptForceBold = False
        self.postscriptFullName = "Untitled Regular"
        self.postscriptIsFixedPitch = False
        self.postscriptNominalWidthX: float | None = None
        self.postscriptOtherBlues: list[float] | None = []
        self.postscriptStemSnapH: list[float] | None = None
        self.postscriptStemSnapV: list[float] | None = None
        self.postscriptUnderlinePosition = 0
        self.postscriptUnderlineThickness = 0
        self.postscriptWeightName = "Regular"
        self.styleMapFamilyName = "Untitled"
        self.styleMapStyleName = "regular"
        self.styleName = "Regular"

        # Add sensible defaults?
        self.openTypeOS2StrikeoutSize = 0
        self.openTypeOS2StrikeoutPosition = 0
        self.openTypeOS2TypoAscender = 0
        self.openTypeOS2TypoDescender = 0
        self.openTypeOS2TypoLineGap = 0
        self.openTypeOS2WinAscent = 0
        self.openTypeOS2WinDescent = 0
        self.openTypeOS2CodePageRanges: list[int] = []

        # Some lib values are gathered here, they are added to the UFO lib in builder
        self.lib = {}

        self.build_mapping()

    @cached_property
    def ds_family_name(self) -> str | None:
        """
        Return the family name for use in the DesignSpaceDocument.
        """
        if self.openTypeNamePreferredFamilyName:
            return self.openTypeNamePreferredFamilyName
        if self.familyName:
            return self.familyName
        return self.styleMapFamilyName

    @cached_property
    def ds_style_name(self) -> str | None:
        """
        Return the style name for use in the DesignSpaceDocument.
        """
        if self.openTypeNamePreferredSubfamilyName:
            return self.openTypeNamePreferredSubfamilyName
        if self.styleName:
            return self.styleName
        return self.styleMapStyleName

    @cached_property
    def ui_name(self) -> str:
        name = ""
        if hasattr(self, "familyName"):
            name = self.familyName

        elif hasattr(self, "postscriptFontName"):
            name = self.postscriptFontName
        if name:
            return name
        return "Untitled Regular"

    def build_mapping(self):
        self.mapping = {
            # F.pref_family_name: "openTypeNamePreferredFamilyName",  # below
            F.full_name: "postscriptFullName",
            F.font_name: "postscriptFontName",
            F.family_name: "styleMapFamilyName",
            F.weight: "weightName",
            F.italic_angle: "italicAngle",
            F.underline_position: "postscriptUnderlinePosition",
            F.underline_thickness: "postscriptUnderlineThickness",
            # F.is_fixed_pitch: "postscriptIsFixedPitch",  # below
            F.copyright: "copyright",
            F.notice: "openTypeNameDescription",
            F.source: "openTypeNameManufacturer",
            F.unique_id: "postscriptUniqueID",
            # F.weight_code, below
            F.trademark: "trademark",
            F.designer: "openTypeNameDesigner",
            F.designer_url: "openTypeNameDesignerURL",
            F.vendor_url: "openTypeNameManufacturerURL",
            F.width: "widthName",
            F.License: "openTypeNameLicense",
            F.LicenseURL: "openTypeNameLicenseURL",
            F.fond_id: "macintoshFONDFamilyID",
            F.apple_name: "macintoshFONDName",
            F.panose: "openTypeOS2Panose",
            F.vendor: "openTypeOS2VendorID",
            F.tt_u_id: "openTypeNameUniqueID",
            F.tt_version: "openTypeNameVersion",
            F.version_major: "versionMajor",
            F.version_minor: "versionMinor",
            F.year: "year",
            F.upm: "unitsPerEm",
            # F.pref_style_name: "openTypeNamePreferredSubfamilyName",  # below
            T.hhea_ascender: "openTypeHheaAscender",
            T.hhea_descender: "openTypeHheaDescender",
            T.hhea_line_gap: "openTypeHheaLineGap",
            F.note: "note",
            F.default_character: "postscriptDefaultCharacter",
        }
        # Integer values from TTInfo
        self.mapping_int = {
            # "max_zones": ,
            # "max_twilight_points": "",
            # "max_storage": "",
            # "max_function_defs": "",
            # "max_instruction_defs": "",
            # "max_stack_elements": "",
            # "head_flags": "", # below
            # "head_units_per_em": "unitsPerEm",  # duplicate
            # "os2_us_weight_class": "openTypeOS2WeightClass",  # duplicate
            "os2_us_width_class": "openTypeOS2WidthClass",
            "head_lowest_rec_ppem": "openTypeHeadLowestRecPPEM",
            "os2_y_subscript_x_size": "openTypeOS2SubscriptXSize",
            "os2_y_subscript_y_size": "openTypeOS2SubscriptYSize",
            "os2_y_subscript_x_offset": "openTypeOS2SubscriptXOffset",
            "os2_y_subscript_y_offset": "openTypeOS2SubscriptYOffset",
            "os2_y_superscript_x_size": "openTypeOS2SuperscriptXSize",
            "os2_y_superscript_y_size": "openTypeOS2SuperscriptYSize",
            "os2_y_superscript_x_offset": "openTypeOS2SuperscriptXOffset",
            "os2_y_superscript_y_offset": "openTypeOS2SuperscriptYOffset",
            "os2_y_strikeout_size": "openTypeOS2StrikeoutSize",
            "os2_y_strikeout_position": "openTypeOS2StrikeoutPosition",
            "os2_s_typo_ascender": "openTypeOS2TypoAscender",
            "os2_s_typo_descender": "openTypeOS2TypoDescender",
            "os2_s_typo_line_gap": "openTypeOS2TypoLineGap",
            "os2_us_win_ascent": "openTypeOS2WinAscent",
            "os2_us_win_descent": "openTypeOS2WinDescent",
            # "Average Width": "postscriptNominalWidthX",
        }

    def fix_underline_position(self):
        # VFB stores middle of line and thickness, but spec says it must be
        # stored as top of line and thickness.
        if (
            self.postscriptUnderlinePosition is None
            or self.postscriptUnderlineThickness is None
        ):
            logger.error(
                "Can't fix underline position because position or thickness is None"
            )
            return

        self.postscriptUnderlinePosition += int(
            round(0.5 * self.postscriptUnderlineThickness)
        )

    def set_attr(self, attr: str, data):
        setattr(self, attr, data)

    def set_created_timestamp(self, data: int) -> None:
        self.openTypeHeadCreated = convert_timestamp(data).strftime("%Y/%m/%d %H:%M:%S")

    def set_fixed_pitch(self, data: int) -> None:
        self.postscriptIsFixedPitch = bool(data)

    def set_name_records(self, data: list[tuple[int, int, int, int, str]]) -> None:
        # We need to set the attribute once at the end to be able to write JSON, cf.
        # https://github.com/fonttools/ufoLib2/issues/203
        name_records = []
        for rec in data:
            nameID, platformID, encodingID, languageID, s = rec
            name_records.append(
                {
                    "nameID": nameID,
                    "platformID": platformID,
                    "encodingID": encodingID,
                    "languageID": languageID,
                    "string": s,
                }
            )
        self.openTypeNameRecords = name_records

    def set_selection(self, data: int) -> None:
        # Bit 0 = Italic
        # Bit 5 = Bold
        # Bit 6 = Regular

        # Those should not be included in the list.
        # Any others could remain, but FL doesn't set them.
        intlist = binaryToIntList(data)
        self.openTypeOS2Selection = [b for b in intlist if b not in (0, 5, 6)]

        # Construct the style map style name

        name_parts = []
        if 6 in intlist:
            name_parts.append("regular")
        elif 5 in intlist:
            name_parts.append("bold")
        if 0 in intlist:
            name_parts.append("italic")
        if name_parts:
            self.styleMapStyleName = " ".join(name_parts)

    def set_style_name(self, data: str) -> None:
        self.styleName = data
        self.openTypeNamePreferredSubfamilyName = data

    def set_tt_gasp(self, data: GaspList) -> None:
        # FIXME: Different results when hinting is compiled with flufocompile
        gasp: list[TUfoGaspRecDict] = []
        for rec in data:
            gasp.append(
                TUfoGaspRecDict(
                    rangeMaxPPEM=rec["maxPpem"],
                    rangeGaspBehavior=binaryToIntList(rec["flags"]),
                )
            )
        self.openTypeGaspRangeRecords = gasp

    def set_tt_info(self, data: dict[str, int | list[int] | list[str]]) -> None:  # noqa: C901, E501
        instructions = {}
        for k, v in data.items():
            if isinstance(v, int):
                if k in self.mapping_int:
                    setattr(self, self.mapping_int[k], v)
                elif k == "head_creation":
                    self.set_created_timestamp(v)
                elif k == "head_font_direction_hint":
                    # self.info.openTypeOS2Type = binaryToIntList(v)
                    pass
                elif k == "os2_fs_type":
                    self.openTypeOS2Type = binaryToIntList(v)
                elif k == "os2_s_family_class":
                    c = v >> 8
                    s = v & ~(c << 8)
                    self.openTypeOS2FamilyClass = [c, s]
                elif k == "os2_us_weight_class":
                    # Duplicate, we set it from a separate entry (weight_code)
                    # self.openTypeOS2WeightClass = v
                    pass
                elif k == "os2_fs_selection":
                    # Duplicate, set from a separate entry (font_style)
                    # self.openTypeOS2Selection = binaryToIntList(v)
                    pass
                    # We could also set maxp here, but the values are useless on their
                    # own:
                    # elif k in maxp_keys:
                    # instructions[maxp_keys[k]] = v
                elif k == "Average Width":
                    if v != 0:
                        self.postscriptNominalWidthX = abs(v)
                else:
                    logger.info(f"Unhandled integer value in UFO info: {k, v}")
            elif isinstance(v, list):
                if k == "OpenTypeOS2Panose":
                    # Duplicate?
                    # if v != self.info.openTypeOS2Panose:
                    #     print("Contradictory PANOSE values")
                    #     print(self.info.openTypeOS2Panose, "vs.", v)
                    pass
                else:
                    logger.info(f"Unhandled list value in UFO info: {k, v}")
            elif isinstance(v, dict):
                if k == "head_flags":
                    self.openTypeHeadFlags = v.get("flags", [])
                elif k == "Codepages":
                    ranges = binaryToIntList(v.get("os2_ul_code_page_range1", 0))
                    for cp in binaryToIntList(v.get("os2_ul_code_page_range2", 0)):
                        ranges.append(cp + 32)
                    if ranges:
                        self.openTypeOS2CodePageRanges = ranges
                else:
                    logger.info(f"Unhandled dict value in UFO info: {k, v}")
            else:
                raise TypeError
        if instructions:
            if any(instructions.values()):
                # Prepare UFO-level lib entry for TrueType values
                instructions["formatVersion"] = "1"
                self.lib = {"public.truetype.instructions": instructions}

    def set_weight_class(self, data: int) -> None:
        self.openTypeOS2WeightClass = min(max(1, data), 1000)
