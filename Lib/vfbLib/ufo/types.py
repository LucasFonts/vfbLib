from __future__ import annotations

from typing import Any, Dict, List, Literal, Tuple


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
