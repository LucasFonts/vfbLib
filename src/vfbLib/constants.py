from __future__ import annotations

from vfbLib.compilers.base import (
    EncodedValueListCompiler,
    EncodedValueListWithCountCompiler,
    GlyphEncodingCompiler,
    HexStringCompiler,
    MappingModeCompiler,
    OpenTypeKerningClassFlagsCompiler,
    OpenTypeMetricsClassFlagsCompiler,
)
from vfbLib.compilers.binary import BinaryTableCompiler
from vfbLib.compilers.bitmap import BackgroundBitmapCompiler, GlyphBitmapsCompiler
from vfbLib.compilers.cmap import CustomCmapCompiler
from vfbLib.compilers.fl3 import FL3Type1410Compiler
from vfbLib.compilers.glyph import (
    GlobalMaskCompiler,
    GlyphAnchorsCompiler,
    GlyphAnchorsSuppCompiler,
    GlyphCompiler,
    GlyphGDEFCompiler,
    GlyphOriginCompiler,
    GlyphSketchCompiler,
    GlyphUnicodesCompiler,
    GlyphUnicodesSuppCompiler,
    LinksCompiler,
    MaskCompiler,
    MaskMetricsCompiler,
    MaskMetricsMMCompiler,
)
from vfbLib.compilers.guides import GuidePropertiesCompiler, GuidesCompiler
from vfbLib.compilers.mm import (
    AnisotropicInterpolationsCompiler,
    AxisMappingsCompiler,
    AxisMappingsCountCompiler,
    MasterLocationCompiler,
    PrimaryInstancesCompiler,
)
from vfbLib.compilers.numeric import (
    DoubleCompiler,
    DoubleListCompiler,
    Int16Compiler,
    IntListCompiler,
    PanoseCompiler,
    SignedInt16Compiler,
    SignedInt32Compiler,
    UnicodeRangesCompiler,
)
from vfbLib.compilers.options import (
    ExportOptionsCompiler,
    OpenTypeExportOptionsCompiler,
)
from vfbLib.compilers.pclt import PcltCompiler
from vfbLib.compilers.ps import (
    PostScriptGlobalHintingOptionsCompiler,
    PostScriptGlyphHintingOptionsCompiler,
    PostScriptInfoCompiler,
)
from vfbLib.compilers.text import (
    NameRecordsCompiler,
    OpenTypeStringCompiler,
    StringCompiler,
    VendorIdCompiler,
)
from vfbLib.compilers.truetype import (
    GaspCompiler,
    TrueTypeInfoCompiler,
    TrueTypeStemPpems1Compiler,
    TrueTypeStemPpems23Compiler,
    TrueTypeStemPpemsCompiler,
    TrueTypeStemsCompiler,
    TrueTypeZoneDeltasCompiler,
    TrueTypeZonesCompiler,
    VdmxCompiler,
)
from vfbLib.enum import F, G, M, T
from vfbLib.parsers.base import (
    BaseParser,
    EncodedValueListParser,
    EncodedValueListWithCountParser,
    GlyphEncodingParser,
    MappingModeParser,
    OpenTypeKerningClassFlagsParser,
    OpenTypeMetricsClassFlagsParser,
)
from vfbLib.parsers.binary import BinaryTableParser
from vfbLib.parsers.bitmap import BackgroundBitmapParser, GlyphBitmapsParser
from vfbLib.parsers.cmap import CustomCmapParser
from vfbLib.parsers.fl3 import FL3Type1410Parser
from vfbLib.parsers.glyph import (
    GlobalMaskParser,
    GlyphAnchorsParser,
    GlyphAnchorsSuppParser,
    GlyphGDEFParser,
    GlyphOriginParser,
    GlyphParser,
    GlyphSketchParser,
    GlyphUnicodeParser,
    GlyphUnicodeSuppParser,
    LinkParser,
    MaskMetricsMMParser,
    MaskMetricsParser,
    MaskParser,
)
from vfbLib.parsers.guides import GlobalGuidesParser, GuidePropertiesParser
from vfbLib.parsers.mm import (
    AnisotropicInterpolationsParser,
    AxisMappingsCountParser,
    AxisMappingsParser,
    MasterLocationParser,
    PrimaryInstancesParser,
)
from vfbLib.parsers.numeric import (
    DoubleListParser,
    DoubleParser,
    Int16Parser,
    IntListParser,
    PanoseParser,
    SignedInt16Parser,
    SignedInt32Parser,
    UnicodeRangesParser,
)
from vfbLib.parsers.options import ExportOptionsParser, OpenTypeExportOptionsParser
from vfbLib.parsers.pclt import PcltParser
from vfbLib.parsers.ps import (
    PostScriptGlobalHintingOptionsParser,
    PostScriptGlyphHintingOptionsParser,
    PostScriptInfoParser,
)
from vfbLib.parsers.text import NameRecordsParser, OpenTypeStringParser, StringParser
from vfbLib.parsers.truetype import (
    GaspParser,
    TrueTypeInfoParser,
    TrueTypeStemPpems1Parser,
    TrueTypeStemPpems23Parser,
    TrueTypeStemPpemsParser,
    TrueTypeStemsParser,
    TrueTypeZoneDeltasParser,
    TrueTypeZonesParser,
    VdmxParser,
)

# fmt: off
parser_classes = {
    # Sorted by appearance in the VFB
    F.EncodingDefault: ("Encoding Default", GlyphEncodingParser, GlyphEncodingCompiler),
    F.Encoding: ("Encoding", GlyphEncodingParser, GlyphEncodingCompiler),
    F.E1502: ("1502", Int16Parser, Int16Compiler),
    F.E518: ("518", StringParser, StringCompiler),
    F.E257: ("257", StringParser, StringCompiler),
    F.font_name: ("font_name", StringParser, StringCompiler),
    F.MasterCount: ("Master Count", Int16Parser, Int16Compiler),
    F.weight_vector: ("weight_vector", DoubleListParser, DoubleListCompiler),
    F.unique_id: ("unique_id", SignedInt32Parser, SignedInt32Compiler),
    F.version: ("version", StringParser, StringCompiler),
    F.notice: ("notice", StringParser, StringCompiler),
    F.full_name: ("full_name", StringParser, StringCompiler),
    F.family_name: ("family_name", StringParser, StringCompiler),
    F.pref_family_name: ("pref_family_name", StringParser, StringCompiler),
    F.menu_name: ("menu_name", StringParser, StringCompiler),
    F.apple_name: ("apple_name", StringParser, StringCompiler),
    F.weight: ("weight", StringParser, StringCompiler),
    F.width: ("width", StringParser, StringCompiler),
    F.License: ("License", StringParser, StringCompiler),
    F.LicenseURL: ("License URL", StringParser, StringCompiler),
    F.copyright: ("copyright", StringParser, StringCompiler),
    F.trademark: ("trademark", StringParser, StringCompiler),
    F.designer: ("designer", StringParser, StringCompiler),
    F.designer_url: ("designer_url", StringParser, StringCompiler),
    F.vendor_url: ("vendor_url", StringParser, StringCompiler),
    F.source: ("source", StringParser, StringCompiler),  # manufacturer, "created by"
    F.is_fixed_pitch: ("is_fixed_pitch", Int16Parser, Int16Compiler),
    F.weight_code: ("weight_code", SignedInt16Parser, SignedInt16Compiler),
    F.italic_angle: ("italic_angle", DoubleParser, DoubleCompiler),
    F.slant_angle: ("slant_angle", DoubleParser, DoubleCompiler),
    F.underline_position: ("underline_position", SignedInt16Parser, SignedInt16Compiler),  # noqa: E501
    F.underline_thickness: ("underline_thickness", Int16Parser, Int16Compiler),
    F.ms_charset: ("ms_charset", Int16Parser, Int16Compiler),
    F.panose: ("panose", PanoseParser, PanoseCompiler),
    F.tt_version: ("tt_version", StringParser, StringCompiler),
    F.tt_u_id: ("tt_u_id", StringParser, StringCompiler),
    F.style_name: ("style_name", StringParser, StringCompiler),
    F.pref_style_name: ("pref_style_name", StringParser, StringCompiler),
    F.mac_compatible: ("mac_compatible", StringParser, StringCompiler),
    F.E1140: ("1140", BaseParser, HexStringCompiler),
    F.vendor: ("vendor", StringParser, VendorIdCompiler),
    F.xuid: ("xuid", IntListParser, IntListCompiler),
    F.xuid_num: ("xuid_num", Int16Parser, Int16Compiler),
    F.year: ("year", Int16Parser, Int16Compiler),
    F.version_major: ("version_major", Int16Parser, Int16Compiler),
    F.version_minor: ("version_minor", Int16Parser, Int16Compiler),
    F.upm: ("upm", Int16Parser, Int16Compiler),
    F.fond_id: ("fond_id", Int16Parser, Int16Compiler),
    F.PostScriptHintingOptions: ("PostScript Hinting Options", PostScriptGlobalHintingOptionsParser, PostScriptGlobalHintingOptionsCompiler),  # noqa: E501
    F.E1068: ("1068", EncodedValueListWithCountParser, EncodedValueListWithCountCompiler),  # noqa: E501
    F.blue_values_num: ("blue_values_num", Int16Parser, Int16Compiler),
    F.other_blues_num: ("other_blues_num", Int16Parser, Int16Compiler),
    F.family_blues_num: ("family_blues_num", Int16Parser, Int16Compiler),
    F.family_other_blues_num: ("family_other_blues_num", Int16Parser, Int16Compiler),
    F.stem_snap_h_num: ("stem_snap_h_num", Int16Parser, Int16Compiler),
    F.stem_snap_v_num: ("stem_snap_v_num", Int16Parser, Int16Compiler),
    F.font_style: ("font_style", Int16Parser, Int16Compiler),  # OS/2.fsSelection
    F.pcl_id: ("pcl_id", Int16Parser, Int16Compiler),
    F.vp_id: ("vp_id", Int16Parser, Int16Compiler),
    F.ms_id: ("ms_id", Int16Parser, Int16Compiler),
    F.pcl_chars_set: ("pcl_chars_set", StringParser, StringCompiler),

    T.cvt: ("cvt", BaseParser, HexStringCompiler),  # Binary cvt Table
    T.prep: ("prep", BaseParser, HexStringCompiler),  # Binary prep Table
    T.fpgm: ("fpgm", BaseParser, HexStringCompiler),  # Binary fpgm Table
    T.gasp: ("gasp", GaspParser, GaspCompiler),
    F.ttinfo: ("ttinfo", TrueTypeInfoParser, TrueTypeInfoCompiler),
    T.vdmx: ("vdmx", VdmxParser, VdmxCompiler),
    T.hhea_line_gap: ("hhea_line_gap", Int16Parser, Int16Compiler),
    T.hhea_ascender: ("hhea_ascender", SignedInt16Parser, SignedInt16Compiler),
    T.hhea_descender: ("hhea_descender", SignedInt16Parser, SignedInt16Compiler),
    # hstem_data and vstem_data, goes to font.ttinfo:
    T.TrueTypeStemPPEMs2And3: ("TrueType Stem PPEMs 2 And 3", TrueTypeStemPpems23Parser, TrueTypeStemPpems23Compiler),  # noqa: E501
    T.TrueTypeStemPPEMs: ("TrueType Stem PPEMs", TrueTypeStemPpemsParser, TrueTypeStemPpemsCompiler),  # noqa: E501
    # Probably in font.ttinfo, but not accessible through API:
    T.TrueTypeStems: ("TrueType Stems", TrueTypeStemsParser, TrueTypeStemsCompiler),
    T.TrueTypeStemPPEMs1: ("TrueType Stem PPEMs 1", TrueTypeStemPpems1Parser, TrueTypeStemPpems1Compiler),  # noqa: E501
    # Probably in font.ttinfo, but not accessible through API:
    T.TrueTypeZones: ("TrueType Zones", TrueTypeZonesParser, TrueTypeZonesCompiler),

    # Goes to font:
    F.unicoderanges: ("unicoderanges", UnicodeRangesParser, UnicodeRangesCompiler),

    # Probably in font.ttinfo, but not accessible through API:
    T.stemsnaplimit: ("stemsnaplimit", Int16Parser, Int16Compiler),  # Pixel Snap
    T.zoneppm: ("zoneppm", Int16Parser, Int16Compiler),  # Zone Stop PPEM
    T.codeppm: ("codeppm", Int16Parser, Int16Compiler),  # Code Stop PPEM
    T.E1604: ("1604", Int16Parser, Int16Compiler),  # Binary import? e.g. 255
    T.E2032: ("2032", Int16Parser, Int16Compiler),  # Binary import? e.g. 300
    T.TrueTypeZoneDeltas: ("TrueType Zone Deltas", TrueTypeZoneDeltasParser, TrueTypeZoneDeltasCompiler),  # noqa: E501

    # Goes to font again:
    F.fontnames: ("fontnames", NameRecordsParser, NameRecordsCompiler),
    F.CustomCMAPs: ("Custom CMAPs", CustomCmapParser, CustomCmapCompiler),
    F.PCLTTable: ("PCLT Table", PcltParser, PcltCompiler),
    F.ExportPCLTTable: ("Export PCLT Table", Int16Parser, Int16Compiler),
    F.note: ("note", StringParser, StringCompiler),
    F.E2030: ("2030", BaseParser, HexStringCompiler),
    F.customdata: ("customdata", StringParser, StringCompiler),
    F.MetricsClassFlags: ("OpenType Metrics Class Flags", OpenTypeMetricsClassFlagsParser, OpenTypeMetricsClassFlagsCompiler),  # noqa: E501
    F.KerningClassFlags: ("OpenType Kerning Class Flags", OpenTypeKerningClassFlagsParser, OpenTypeKerningClassFlagsCompiler),  # noqa: E501

    # Repeat for each binary table:
    # truetypetables: TrueTypeTable
    F.TrueTypeTable: ("TrueTypeTable", BinaryTableParser, BinaryTableCompiler),

    F.features: ("features", OpenTypeStringParser, OpenTypeStringCompiler),

    # Repeat for each OpenType class:
    F.GlyphClass: ("OpenType Class", StringParser, StringCompiler),  # Font.classes

    F.E513: ("513", BaseParser, HexStringCompiler),
    F.E271: ("271", BaseParser, HexStringCompiler),
    F.AxisCount: ("Axis Count", Int16Parser, Int16Compiler),
    # Repeat for each axis:
    F.AxisName: ("Axis Name", StringParser, StringCompiler),

    F.AnisotropicInterpolationMappings: ("Anisotropic Interpolation Mappings", AnisotropicInterpolationsParser, AnisotropicInterpolationsCompiler),  # noqa: E501
    F.AxisMappingsCount: ("Axis Mappings Count", AxisMappingsCountParser, AxisMappingsCountCompiler),  # noqa: E501
    F.AxisMappings: ("Axis Mappings", AxisMappingsParser, AxisMappingsCompiler),

    # Repeat the next two for each master:
    M.MasterName: ("Master Name", StringParser, StringCompiler),
    M.MasterLocation: ("Master Location", MasterLocationParser, MasterLocationCompiler),

    F.PrimaryInstanceLocations: ("Primary Instance Locations", DoubleListParser, DoubleListCompiler),  # noqa: E501
    F.PrimaryInstances: ("Primary Instances", PrimaryInstancesParser, PrimaryInstancesCompiler),  # noqa: E501

    # Repeat PostScript Info for each master:
    M.PostScriptInfo: ("PostScript Info", PostScriptInfoParser, PostScriptInfoCompiler),

    F.E527: ("527", BaseParser, HexStringCompiler),
    F.GlobalGuides: ("Global Guides", GlobalGuidesParser, GuidesCompiler),
    F.GlobalGuideProperties: ("Global Guide Properties", GuidePropertiesParser, GuidePropertiesCompiler),  # noqa: E501
    F.GlobalMask: ("Global Mask", GlobalMaskParser, GlobalMaskCompiler),
    F.default_character: ("default_character", StringParser, StringCompiler),

    # Begin: Repeat for each glyph
    G.Glyph: ("Glyph", GlyphParser, GlyphCompiler),
    # Glyph.hlinks and Glyph.vlinks:
    G.Links: ("Links", LinkParser, LinksCompiler),
    G.image: ("image", BackgroundBitmapParser, BackgroundBitmapCompiler),
    G.Bitmaps: ("Glyph Bitmaps", GlyphBitmapsParser, GlyphBitmapsCompiler),
    G.E2023: ("2023", EncodedValueListParser, EncodedValueListCompiler),  # 1 encoded value per master  # noqa: E501
    G.Sketch: ("Glyph Sketch", GlyphSketchParser, GlyphSketchCompiler),
    G.HintingOptions: ("Glyph Hinting Options", PostScriptGlyphHintingOptionsParser, PostScriptGlyphHintingOptionsCompiler),  # noqa: E501
    G.mask: ("mask", MaskParser, MaskCompiler),
    G.MaskMetrics: ("mask.metrics", MaskMetricsParser, MaskMetricsCompiler),  # Single master mask metrics  # noqa: E501
    G.MaskMetricsMM: ("mask.metrics_mm", MaskMetricsMMParser, MaskMetricsMMCompiler),  # Mask metrics master 2 to 16  # noqa: E501
    G.Origin: ("Glyph Origin", GlyphOriginParser, GlyphOriginCompiler),
    G.unicodes: ("unicodes", GlyphUnicodeParser, GlyphUnicodesCompiler),  # Glyph Unicode  # noqa: E501
    G.E2034: ("2034", StringParser, StringCompiler),
    G.UnicodesNonBMP: ("Glyph Unicode Non-BMP", GlyphUnicodeSuppParser, GlyphUnicodesSuppCompiler),  # noqa: E501
    G.mark: ("mark", Int16Parser, Int16Compiler),  # Mark Color
    G.customdata: ("glyph.customdata", StringParser, StringCompiler),
    G.note: ("glyph.note", StringParser, StringCompiler),
    G.GDEFData: ("Glyph GDEF Data", GlyphGDEFParser, GlyphGDEFCompiler),
    G.AnchorsProperties: ("Glyph Anchors Supplemental", GlyphAnchorsSuppParser, GlyphAnchorsSuppCompiler),  # noqa: E501
    G.AnchorsMM: ("Glyph Anchors MM", GlyphAnchorsParser, GlyphAnchorsCompiler),  # MM-compatible  # noqa: E501
    G.GuideProperties: ("Glyph Guide Properties", GuidePropertiesParser, GuidePropertiesCompiler),  # noqa: E501
    # End: Repeat for each glyph

    F.OpenTypeExportOptions: ("OpenType Export Options", OpenTypeExportOptionsParser, OpenTypeExportOptionsCompiler),  # noqa: E501
    F.ExportOptions: ("Export Options", ExportOptionsParser, ExportOptionsCompiler),
    F.MappingMode: ("Mapping Mode", MappingModeParser, MappingModeCompiler),

    # Not seen in FontNames.vfb:
    F.E272: ("272", BaseParser, HexStringCompiler),
    F.E1410: ("1410", FL3Type1410Parser, FL3Type1410Compiler),
    F.E528: ("528", BaseParser, HexStringCompiler),

    # File end
    F.EOF: ("EOF", None, None),
}
# fmt: on


# Those entries are ignored in minimal mode:
ignore_minimal = set(
    (
        "Global Guides",
        "Global Mask",
        "Glyph Bitmaps",
        "Glyph Guide Properties",
        "glyph.note",
        "image",
        "mark",
        "mask",
        "note",
    )
)

ignore_minimal_keys = frozenset(
    (
        F.GlobalGuides,
        F.GlobalMask,
        F.note,
        G.Bitmaps,
        G.GuideProperties,
        G.image,
        G.mark,
        G.mask,
        G.note,
    )
)
