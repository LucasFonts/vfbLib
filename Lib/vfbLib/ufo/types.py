from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import Any, Dict, List, Literal, Tuple


UfoPoint = Tuple[int, int]
UfoComponent = Tuple[str, Tuple[float, float, float, float, int, int]]
UfoSegment = Tuple[str | None, bool, str | None, UfoPoint]
UfoContour = List[UfoSegment]


class UfoGuide(TypedDict):
    angle: float | int
    color: NotRequired[str]
    name: NotRequired[str]
    x: int
    y: int
