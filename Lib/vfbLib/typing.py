from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing_extensions import NotRequired, TypedDict

from typing import Any, Dict, List, Literal, Tuple


Point = Tuple[int, int]


class Anchor(TypedDict):
    name: NotRequired[str]
    x: int
    x1: NotRequired[int]
    y: int
    y1: NotRequired[int]


ClassFlagDict = Dict[str, Tuple[int, int]]


class Component(TypedDict):
    gid: int
    offsetX: List[int]
    offsetY: List[int]
    scaleX: List[float]
    scaleY: List[float]


GaspList = List[Dict[str, int]]


class GdefDict(TypedDict):
    anchors: NotRequired[List[Anchor]]
    carets: NotRequired[List[Tuple[int, int]]]
    glyph_class: NotRequired[str]
    unknown: NotRequired[List[int]]


class GlyphData(TypedDict):
    components: NotRequired[List[Component]]
    # constants: NotRequired[Tuple[Any, ...]]
    guides: NotRequired[GuideDict]
    hints: NotRequired[HintDict]
    imported: NotRequired[Any]  # FIXME
    kerning: NotRequired[Dict[int, List[int]]]
    metrics: NotRequired[List[Point]]
    name: NotRequired[str]
    nodes: NotRequired[List[MMNode]]
    num_masters: NotRequired[int]
    # num_node_values: NotRequired[int]
    tth: NotRequired[List[Instruction]]


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


class HintDict(TypedDict):
    h: List[List[Hint]]
    v: List[List[Hint]]
    hintmasks: NotRequired[List[Dict[str, int]]]


HintTuple = Tuple[str, int, int]


class Instruction(TypedDict):
    cmd: str
    params: Dict[str, int]


class LinkDict(TypedDict):
    x: NotRequired[List[Tuple[int, int]]]
    y: NotRequired[List[Tuple[int, int]]]


class MaskData(GlyphData):
    num: int
    reserved0: NotRequired[int]


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


class TTCommandDict(TypedDict):
    name: str
    params: List[str]
