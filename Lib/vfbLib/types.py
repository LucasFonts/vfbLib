from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import List, Literal, Tuple


Point = Tuple[int, int]


class Anchor(TypedDict):
    name: NotRequired[str]
    x: int
    x1: int
    y: int
    y1: int


class Guide(TypedDict):
    angle: float | int
    pos: int


GuideList = List[Guide]


class GuideDict(TypedDict):
    h: List[GuideList]
    v: List[GuideList]


class GuideProperty(TypedDict):
    color: NotRequired[str]
    index: int
    name: NotRequired[str]


GuidePropertyList = List[GuideProperty]


class Hint(TypedDict):
    pos: int
    width: int


class MMAnchor(TypedDict):
    x: List[int]
    y: List[int]


class MMHintsDict(TypedDict):
    h: List[List[Hint]]
    v: List[List[Hint]]


class MMNode(TypedDict):
    flags: int
    points: List[List[Point]]
    type: Literal["move", "line", "curve", "qcurve"]
