from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import Optional, Tuple
from vfbLib.typing import HintTuple


class TUfoTTZoneDict(TypedDict):
    position: int
    top: bool
    width: int
    # Zone index, shift; index must be str to be saved in lib
    delta: NotRequired[dict[str, int]]


UfoPoint = Tuple[int, int]
UfoComponent = Tuple[str, Tuple[float, float, float, float, int, int]]
UfoGroups = dict[str, list[str]]  # name, glyphs
UfoMasterKerning = dict[Tuple[str, str], int]  # Lstr, Rstr, value
UfoMMKerning = dict[Tuple[str, int], list[int]]  # Lstr, Rid, master values
UfoSegment = Tuple[Optional[str], bool, Optional[str], UfoPoint]
UfoContour = list[UfoSegment]
TUfoTTZonesDict = dict[str, TUfoTTZoneDict]


class TUfoGaspRecDict(TypedDict):
    rangeMaxPPEM: int
    rangeGaspBehavior: list[int]


class TUfoStemsDict(TypedDict):
    ttStemsH: list
    ttStemsV: list


class TUfoStemPPMsDict(TypedDict):
    ttStemsH: list
    ttStemsV: list


class UfoGuide(TypedDict):
    angle: float | int
    color: NotRequired[str]
    name: NotRequired[str]
    x: int
    y: int


class UfoHintingV2(TypedDict):
    flexList: NotRequired[list]
    hintSetList: NotRequired[list[UfoHintSet]]
    id: NotRequired[str]


class UfoHintSet(TypedDict):
    pointTag: str
    stems: list[str | HintTuple]
