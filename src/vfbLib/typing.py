from __future__ import annotations

# try:
#     # NotRequired is only available in Python 3.11+
#     from typing import NotRequired, TypedDict
# except ImportError:
from typing import Any, Literal

from typing_extensions import NotRequired, TypedDict

Point = tuple[int, int]


class AnchorDict(TypedDict):
    name: NotRequired[str]
    x: int
    x1: NotRequired[int]
    y: int
    y1: NotRequired[int]


KerningClassFlagDict = dict[str, tuple[int, int]]

MetricsClassFlagDict = dict[str, tuple[int, int, int]]


class BitmapDataDict(TypedDict):
    flag: int
    data: list[int]
    preview: NotRequired[list[str]]


class BackgroundImageDict(TypedDict):
    origin: tuple[int, int]
    size_units: tuple[int, int]
    size_pixels: tuple[int, int]
    bitmap: BitmapDataDict


class BBoxDict(TypedDict):
    xMin: int
    yMin: int
    xMax: int
    yMax: int


class Component(TypedDict):
    gid: int
    offsetX: list[int]
    offsetY: list[int]
    scaleX: list[float]
    scaleY: list[float]


class CustomCmap(TypedDict):
    language_id: int
    platform_id: int
    encoding_id: int
    format: int
    option: int
    records: list[int]


EntryDecompiled = dict[str, Any] | int | list[Any] | str | tuple[int, str] | None


class EntryDict(TypedDict):
    key: str
    size: NotRequired[int]
    data: bytes | EntryDecompiled
    parser: NotRequired[str]
    compiler: NotRequired[str]


class FeatureDict(TypedDict):
    tag: str
    code: list[str]


class FeaturesDict(TypedDict):
    prefix: list[str]
    features: list[FeatureDict]


class FlagsOptionsDict(TypedDict):
    flags: list[int]
    options: list[str]


class GaspRangeDict(TypedDict):
    maxPpem: int
    flags: int


GaspList = list[GaspRangeDict]


class GdefDict(TypedDict):
    anchors: NotRequired[list[AnchorDict]]
    carets: NotRequired[list[tuple[int, int]]]
    glyph_class: NotRequired[str]
    unknown: NotRequired[list[int]]


class GlyphBitmapDict(TypedDict):
    ppm: int
    origin: tuple[int, int]
    adv: tuple[int, int]
    size_pixels: tuple[int, int]
    bitmap: BitmapDataDict


class GuideDict(TypedDict):
    angle: float | int
    pos: int


GuideList = list[GuideDict]


class MMGuidesDict(TypedDict):
    h: list[GuideList]
    v: list[GuideList]


class GuidePropertyDict(TypedDict):
    color: NotRequired[str]
    index: int
    name: NotRequired[str]


class GuidePropertiesDict(TypedDict):
    h: list[GuidePropertyDict]
    v: list[GuidePropertyDict]


class HintDict(TypedDict):
    pos: int
    width: int


HintTuple = tuple[str, int, int]


class Instruction(TypedDict):
    cmd: str
    params: dict[str, int]


class LinkDict(TypedDict):
    x: list[tuple[int, int]]
    y: list[tuple[int, int]]


class MMAnchorDict(TypedDict):
    x: list[int]
    y: list[int]


class MMHintsDict(TypedDict):
    h: list[list[HintDict]]
    v: list[list[HintDict]]
    hintmasks: NotRequired[list[tuple[str, int]]]


class MMNode(TypedDict):
    flags: int
    points: list[list[Point]]
    type: Literal["move", "line", "curve", "qcurve"]


class PrimaryInstanceDict(TypedDict):
    name: str
    values: tuple[float, ...]


class PSInfoDict(TypedDict):
    font_matrix: tuple[float, ...]
    force_bold: int
    blue_values: list[int]
    other_blues: list[int]
    family_blues: list[int]
    family_other_blues: list[int]
    blue_scale: float
    blue_shift: int
    blue_fuzz: int
    std_hw: int
    std_vw: int
    stem_snap_h: list[int]
    stem_snap_v: list[int]
    bounding_box: BBoxDict
    adv_width_min: int
    adv_width_max: int
    adv_width_avg: int
    ascender: int
    descender: int
    x_height: int
    cap_height: int


class TTCommandDict(TypedDict):
    name: str
    params: list[str]


class TTStemDict(TypedDict):
    name: NotRequired[str]
    round: dict[int, int]
    stem: NotRequired[int]
    value: NotRequired[int]


class TTStemsDict(TypedDict):
    ttStemsV: list[TTStemDict]
    ttStemsH: list[TTStemDict]


class TTZoneDict(TypedDict):
    deltas: NotRequired[dict[int, int]]
    name: str
    position: int
    top: NotRequired[bool]
    value: int


class TTZonesDict(TypedDict):
    ttZonesT: list[TTZoneDict]
    ttZonesB: list[TTZoneDict]


class GlyphData(TypedDict):
    components: NotRequired[list[Component]]
    # constants: NotRequired[Tuple[Any, ...]]
    guides: NotRequired[MMGuidesDict]
    hints: NotRequired[MMHintsDict]
    imported: NotRequired[Any]  # FIXME
    kerning: NotRequired[dict[int, list[int]]]
    metrics: NotRequired[list[Point]]
    name: NotRequired[str]
    nodes: NotRequired[list[MMNode]]
    num_masters: NotRequired[int]
    # num_node_values: NotRequired[int]
    tth: NotRequired[list[Instruction]]


class MaskData(GlyphData):
    num: int
    reserved0: NotRequired[int]


class VdmxRecDict(TypedDict):
    pelHeight: int
    max: int
    min: int


class VfbDict(TypedDict):
    header: VfbHeaderDict
    entries: list[dict[str, Any]]


class VfbHeaderDict(TypedDict):
    header0: int
    filetype: str
    header1: int
    chunk1: list[int]
    creator: dict[int, int | list[int]]
    end0: int
    end1: int
    end2: int
