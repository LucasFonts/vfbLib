from __future__ import annotations

import logging

from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from vfbLib.ufo.typing import TUfoGaspRecDict, UfoGuide


logger = logging.getLogger(__name__)


class VfbToUfoInfo:
    def __init__(self) -> None:
        # Chance to set some defaults that should always be written
        self.familyName = "Untitled"
        self.guidelines: List[UfoGuide] = []
        self.italicAngle: float | int = 0
        self.openTypeGaspRangeRecords: List[TUfoGaspRecDict] = []
        self.openTypeHeadCreated: str = ""
        self.openTypeHeadFlags: List[int] = []
        self.openTypeHheaLineGap = 0
        self.openTypeHeadLowestRecPPEM = 0
        self.openTypeNameDescription = ""
        self.openTypeNameSampleText = ""
        self.openTypeNameRecords: List = []
        self.openTypeOS2FamilyClass = [0, 0]
        self.openTypeOS2Selection: List[int] = []
        self.openTypeOS2SubscriptXSize = 0
        self.openTypeOS2SubscriptYSize = 0
        self.openTypeOS2SubscriptXOffset = 0
        self.openTypeOS2SubscriptYOffset = 0
        self.openTypeOS2SuperscriptXSize = 0
        self.openTypeOS2SuperscriptYSize = 0
        self.openTypeOS2SuperscriptXOffset = 0
        self.openTypeOS2SuperscriptYOffset = 0
        self.openTypeOS2Type: List[int] = []
        self.openTypeOS2UnicodeRanges: List[int] = []
        self.openTypeOS2WeightClass = 0
        self.openTypeOS2WidthClass = 5
        self.postscriptIsFixedPitch = False
        self.postscriptFamilyBlues: List[int] = []
        self.postscriptFamilyOtherBlues: List[int] = []
        self.postscriptFontName = "Untitled-Regular"
        self.postscriptForceBold = False
        self.postscriptFullName = "Untitled Regular"
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
        self.openTypeOS2CodePageRanges: List[int] = []

    @property
    def ui_name(self) -> str:
        name = ""
        if hasattr(self, "familyName"):
            name = self.familyName

        elif hasattr(self, "postscriptFontName"):
            name = self.postscriptFontName
        if name:
            return name
        return "Untitled Regular"
