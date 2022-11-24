from __future__ import annotations

from typing import Any, Dict, List, Literal, Tuple, TypedDict


Anchor = Dict[Literal["name", "x", "x1", "y", "y1"], int | str]

Point = Tuple[int, int]
Contour = List[List[None | str | Point]] | None
ContourList = List[Contour]
ComponentList = List[Tuple[str, Tuple[float, float, float, float, int, int]]]
Guide = Dict[Literal["angle", "pos"], float | int]
GuideList = List[Guide]
GuideDict = Dict[str, List[GuideList]]  # str = Literal["h", "v"]
GuidePropertyList = List[Dict[Literal["color", "index", "name"], int | str]]
GuideAllProperty = Dict[
    str,  # Literal["angle", "color", "name", "x", "y"],
    float | int | str,
]
GuideAllPropertyList = List[GuideAllProperty]


class Hint(TypedDict):
    pos: int
    width: int


class MMHintsDict(TypedDict):
    h: List[List[Hint]]
    v: List[List[Hint]]


class MMNode(TypedDict):
    flags: int
    points: List[List[Point]]
    type: Literal["move", "line", "curve", "qcurve"]
