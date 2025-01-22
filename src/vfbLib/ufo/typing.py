# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing import Optional

from typing_extensions import NotRequired, TypedDict

from vfbLib.typing import HintTuple


class TUfoTTZoneDict(TypedDict):
    position: int
    top: bool
    width: int
    # Zone index, shift; index must be str to be saved in lib
    delta: NotRequired[dict[str, int]]


UfoPoint = tuple[int, int]
UfoComponent = tuple[str, tuple[float, float, float, float, int, int]]
UfoGroups = dict[str, list[str]]  # name, glyphs
UfoMasterKerning = dict[tuple[str, str], int]  # Lstr, Rstr, value
UfoMMKerning = dict[tuple[str, int], list[int]]  # Lstr, Rid, master values
UfoSegment = tuple[Optional[str], bool, Optional[str], UfoPoint]
UfoContour = list[UfoSegment]
TUfoTTZonesDict = dict[str, TUfoTTZoneDict]


class TUfoRawStemDict(TypedDict):
    name: str
    round: dict[str, int]
    value: int


class TUfoRawStemsDict(TypedDict):
    ttStemsH: list[TUfoRawStemDict]
    ttStemsV: list[TUfoRawStemDict]


class TUfoGaspRecDict(TypedDict):
    rangeMaxPPEM: int
    rangeGaspBehavior: list[int]


class TUfoStemDict(TypedDict):
    horizontal: bool
    name: str
    round: dict[str, int]
    width: int


class TUfoStemsDict(TypedDict):
    ttStemsH: list[TUfoStemDict]
    ttStemsV: list[TUfoStemDict]


class TUfoStemPPMDict(TypedDict):
    stem: int
    round: dict[str, int]


class TUfoStemPPMsDict(TypedDict):
    ttStemsH: list[TUfoStemPPMDict]
    ttStemsV: list[TUfoStemPPMDict]


class UfoGuide(TypedDict):
    angle: float | int
    color: NotRequired[str]
    name: NotRequired[str]
    x: int
    y: int


class UfoHintSet(TypedDict):
    pointTag: str
    stems: list[str | HintTuple]


class UfoHintingV2(TypedDict):
    flexList: NotRequired[list]
    hintSetList: NotRequired[list[UfoHintSet]]
    id: NotRequired[str]
