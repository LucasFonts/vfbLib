from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import Dict, List, Optional, Tuple
from vfbLib.typing import HintTuple


class TUfoTTZoneDict(TypedDict):
    position: int
    top: bool
    width: int
    # Zone index, shift; index must be str to be saved in lib
    delta: NotRequired[Dict[str, int]]


UfoPoint = Tuple[int, int]
UfoComponent = Tuple[str, Tuple[float, float, float, float, int, int]]
UfoGroups = Dict[str, List[str]]  # name, glyphs
UfoMasterKerning = Dict[Tuple[str, str], int]  # Lstr, Rstr, value
UfoMMKerning = Dict[Tuple[str, int], List[int]]  # Lstr, Rid, master values
UfoSegment = Tuple[Optional[str], bool, Optional[str], UfoPoint]
UfoContour = List[UfoSegment]
TUfoTTZonesDict = Dict[str, TUfoTTZoneDict]


class TUfoGaspRecDict(TypedDict):
    rangeMaxPPEM: int
    rangeGaspBehavior: List[int]


class TUfoStemsDict(TypedDict):
    ttStemsH: List
    ttStemsV: List


class TUfoStemPPMsDict(TypedDict):
    ttStemsH: List
    ttStemsV: List


class UfoGuide(TypedDict):
    angle: float | int
    color: NotRequired[str]
    name: NotRequired[str]
    x: int
    y: int


class UfoHintingV2(TypedDict):
    flexList: NotRequired[List]
    hintSetList: NotRequired[List[UfoHintSet]]
    id: NotRequired[str]


class UfoHintSet(TypedDict):
    pointTag: str
    stems: List[str | HintTuple]
