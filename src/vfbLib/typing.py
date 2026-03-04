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
    y: int


class AnchorPropertiesDict(TypedDict):
    hue: NotRequired[int]
    data: NotRequired[int]


KerningClassFlagDict = dict[str, tuple[int, int]]

MetricsClassFlagDict = dict[str, tuple[int, int, int]]


class BitmapDataDict(TypedDict):
    data: list[list[int]]
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
    page_name: str


EntryDecompiled = dict[str, Any] | int | list[Any] | str | tuple[int, str] | None


class EntryDict(TypedDict):
    key: str
    size: NotRequired[int]
    data: bytes | EntryDecompiled
    parser: NotRequired[str]
    compiler: NotRequired[str]


class ExpandKernFlagsDict(TypedDict):
    limit_action: int
    limit_codepage: int
    limit_cmap_10: int
    limit_font_window: int
    limit_count: int
    limit_keep: int
    apply_to_assistance: int


class FeatureDict(TypedDict):
    tag: str
    code: list[str]


class FeaturesDict(TypedDict):
    prefix: list[str]
    features: list[FeatureDict]


class FlagsOptionsDict(TypedDict):
    flags: list[int]
    options: list[str]


class FLVersionDict(TypedDict):
    platform: str
    version: tuple[int, ...]
    owner: int


class TTAutoHintOptionsDict(TypedDict):
    single_link_attachment_precision: int
    generate_triple_hints: int
    generate_delta_instructions: int
    direct_links_to_center_of_the_glyph_where_possible: int
    interpolate_positions_of_cusp_points: int
    interpolate_positions_of_double_links: int
    add_link_to_rsb: int


class FontOptionsDict(TypedDict):
    fit_ascender: NotRequired[int]
    fit_descender: NotRequired[int]
    auto_metrics_left: NotRequired[int]
    auto_metrics_right: NotRequired[int]
    auto_metrics_close: NotRequired[int]
    auto_hinting_min_h_len: NotRequired[int]
    auto_hinting_min_v_len: NotRequired[int]
    auto_hinting_min_h_width: NotRequired[int]
    auto_hinting_min_v_width: NotRequired[int]
    auto_hinting_max_h_width: NotRequired[int]
    auto_hinting_max_v_width: NotRequired[int]
    auto_hinting_h_ratio: NotRequired[float]
    auto_hinting_v_ratio: NotRequired[float]
    duplicate_place_x: NotRequired[int]
    paste_place_x: NotRequired[int]
    duplicate_place_y: NotRequired[int]
    paste_place_y: NotRequired[int]
    opentype_name_records: NotRequired[int]
    codepage_for_cmap_1_0: NotRequired[int]
    dont_ignore_unicode_indexes: NotRequired[int]
    head_bbox_savings: NotRequired[int]
    autohinting_options: NotRequired[int | TTAutoHintOptionsDict]
    export_hinted_truetype_font: NotRequired[int]
    autohint_unhinted_glyphs: NotRequired[int]
    keep_existing_truetype_instructions: NotRequired[int]
    export_visual_truetype_hints: NotRequired[int]
    apply_bbox_savings: NotRequired[int]
    auto_win_asc_desc: NotRequired[int]
    add_characters: NotRequired[int]
    export_embedded_bitmaps: NotRequired[int]
    copy_hdmx_data_from_base_to_composite_glyph: NotRequired[int]
    dont_automatically_reorder_glyphs: NotRequired[int]
    export_ot: NotRequired[int]
    export_volt: NotRequired[int]
    write_kern_feature: NotRequired[int]
    t1_terminal: NotRequired[int]
    t1_pfm: NotRequired[int]
    t1_afm: NotRequired[int]
    t1_autohint: NotRequired[int]
    t1_unicode: NotRequired[int]
    optimize_align: NotRequired[int]
    optimize_reduce: NotRequired[int]
    t1_encoding: NotRequired[int]
    ot_write_gdef: NotRequired[int]
    t1_use_os2: NotRequired[int]
    subrize: NotRequired[int]
    t1_sort: NotRequired[int]
    export_kern_table: NotRequired[int]
    t1_fs_type: NotRequired[int]
    expand_kern_flags: NotRequired[int | ExpandKernFlagsDict]
    expand_kern_codepage: NotRequired[int]
    expand_kern_count: NotRequired[int]
    decompose: NotRequired[int]


class GaspRangeDict(TypedDict):
    maxPpem: int
    flags: int


GaspList = list[GaspRangeDict]


class GdefDict(TypedDict):
    anchors: NotRequired[list[AnchorDict]]
    carets: NotRequired[list[tuple[int, int]]]
    glyph_class: NotRequired[str]
    ot_classes: NotRequired[list[int]]


class GlyphBitmapDict(TypedDict):
    ppm: int
    origin: tuple[int, int]
    adv: tuple[int, int]
    size_pixels: tuple[int, int]
    bitmap: BitmapDataDict


class GlyphHintingOptionsDict(TypedDict):
    hint_replacement: NotRequired[int]
    horizontal_3_stem: NotRequired[int]
    vertical_3_stem: NotRequired[int]
    other: NotRequired[list[int]]


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


class MappingModeDict(TypedDict):
    mapping_mode: str
    m2: int
    m3: int
    mapping_id: int


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
    blue_values: list[int]  # max 14
    other_blues: list[int]  # max 10
    family_blues: list[int]  # max 14
    family_other_blues: list[int]  # max 10
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


class CodepagesDict(TypedDict):
    os2_ul_code_page_range1: int
    os2_ul_code_page_range2: int


class TrueTypeInfoDict(TypedDict):
    max_zones: int
    max_twilight_points: int
    max_storage: int
    max_function_defs: int
    max_instruction_defs: int
    max_stack_elements: int
    head_flags: int | FlagsOptionsDict
    head_units_per_em: int
    head_mac_style: int
    head_lowest_rec_ppem: int
    head_creation: int
    head_creation2: int
    head_font_direction_hint: int
    os2_us_weight_class: int
    os2_us_width_class: int
    os2_fs_type: int
    os2_y_subscript_x_size: int
    os2_y_subscript_y_size: int
    os2_y_subscript_x_offset: int
    os2_y_subscript_y_offset: int
    os2_y_superscript_x_size: int
    os2_y_superscript_y_size: int
    os2_y_superscript_x_offset: int
    os2_y_superscript_y_offset: int
    os2_y_strikeout_size: int
    os2_y_strikeout_position: int
    os2_s_family_class: int
    OpenTypeOS2Panose: list[int]
    os2_s_typo_ascender: int
    os2_s_typo_descender: int
    os2_s_typo_line_gap: int
    os2_fs_selection: int
    os2_us_win_ascent: int
    os2_us_win_descent: int
    AverageWidth: int
    HdmxPPMs1: list[int]
    HdmxPPMs2: list[int]
    Codepages: CodepagesDict
    hhea_line_gap: NotRequired[int]
    hhea_ascender: NotRequired[int]
    hhea_descender: NotRequired[int]


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
    weight_vector: list[float]


class VdmxRecDict(TypedDict):
    pelHeight: int
    max: int
    min: int


class VfbDict(TypedDict):
    header: VfbHeaderDict
    entries: list[dict[str, Any]]


class VfbHeaderDict(TypedDict):
    signature: int
    app_version: int
    file_version: int
    version_major: int
    version_minor: int
