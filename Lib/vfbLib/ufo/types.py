from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import Any, Dict, List, Literal, Tuple


UfoPoint = Tuple[int, int]
UfoComponent = Tuple[str, Tuple[float, float, float, float, int, int]]
UfoGroups = Dict[str, List[str]]  # name, glyphs
UfoMasterKerning = Dict[Tuple[str, str], int]  # Lstr, Rstr, value
UfoMMKerning = Dict[Tuple[str, int], List[int]]  # Lstr, Rid, master values
UfoSegment = Tuple[str | None, bool, str | None, UfoPoint]
UfoContour = List[UfoSegment]


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
    stems: List[str]
