from vfbLib.compilers.base import (
    EncodedValueListWithCountCompiler,
    GlyphEncodingCompiler,
    HexStringCompiler,
)
from vfbLib.compilers.binary import BinaryTableCompiler
from vfbLib.compilers.glyph import GlyphCompiler
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
from vfbLib.compilers.text import OpenTypeStringCompiler, StringCompiler
from vfbLib.compilers.truetype import TrueTypeZoneDeltasCompiler, TrueTypeZonesCompiler
from vfbLib.parsers.base import (  # EncodedValueParser,; EncodedKeyValuesParser,
    BaseParser,
    EncodedValueListParser,
    EncodedValueListWithCountParser,
    GaspParser,
    GlyphEncodingParser,
    MappingModeParser,
    OpenTypeKerningClassFlagsParser,
    OpenTypeMetricsClassFlagsParser,
)
from vfbLib.parsers.binary import BinaryTableParser
from vfbLib.parsers.bitmap import BackgroundBitmapParser, GlyphBitmapParser
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
    1501: ("Encoding Default", GlyphEncodingParser, GlyphEncodingCompiler),
    1500: ("Encoding", GlyphEncodingParser, GlyphEncodingCompiler),
    1502: ("1502", Int16Parser, Int16Compiler),
    518: ("518", StringParser, StringCompiler),
    257: ("257", StringParser, StringCompiler),
    1026: ("font_name", StringParser, StringCompiler),
    1503: ("Master Count", Int16Parser, Int16Compiler),
    1517: ("weight_vector", DoubleListParser, DoubleListCompiler),
    1044: ("unique_id", SignedInt32Parser, SignedInt32Compiler),
    1046: ("version", StringParser, StringCompiler),
    1038: ("notice", StringParser, StringCompiler),
    1025: ("full_name", StringParser, StringCompiler),
    1027: ("family_name", StringParser, StringCompiler),
    1024: ("pref_family_name", StringParser, StringCompiler),
    1056: ("menu_name", StringParser, StringCompiler),
    1092: ("apple_name", StringParser, StringCompiler),
    1028: ("weight", StringParser, StringCompiler),
    1065: ("width", StringParser, StringCompiler),

    # Is license/url not in Python API?
    1069: ("License", StringParser, StringCompiler),
    1070: ("License URL", StringParser, StringCompiler),

    1037: ("copyright", StringParser, StringCompiler),
    1061: ("trademark", StringParser, StringCompiler),
    1062: ("designer", StringParser, StringCompiler),
    1063: ("designer_url", StringParser, StringCompiler),
    1064: ("vendor_url", StringParser, StringCompiler),
    1039: ("source", StringParser, StringCompiler),  # manufacturer, "created by"
    1034: ("is_fixed_pitch", Int16Parser, Int16Compiler),
    1048: ("weight_code", SignedInt16Parser, SignedInt16Compiler),
    1029: ("italic_angle", DoubleParser, DoubleCompiler),
    1047: ("slant_angle", DoubleParser, DoubleCompiler),
    1030: ("underline_position", SignedInt16Parser, SignedInt16Compiler),
    1031: ("underline_thickness", Int16Parser, Int16Compiler),
    1054: ("ms_charset", Int16Parser, Int16Compiler),
    1118: ("panose", PanoseParser, PanoseCompiler),
    1128: ("tt_version", StringParser, StringCompiler),
    1129: ("tt_u_id", StringParser, StringCompiler),
    1127: ("style_name", StringParser, StringCompiler),
    1137: ("pref_style_name", StringParser, StringCompiler),
    1139: ("mac_compatible", StringParser, StringCompiler),  # OT Mac Name
    1140: ("1140", BaseParser, HexStringCompiler),
    1121: ("vendor", StringParser, StringCompiler),  # vendorID
    1133: ("xuid", IntListParser, IntListCompiler),  # Type 1 XUIDs
    1134: ("xuid_num", Int16Parser, Int16Compiler),  # Type 1 XUIDs Count
    1132: ("year", Int16Parser, Int16Compiler),
    1130: ("version_major", Int16Parser, Int16Compiler),
    1131: ("version_minor", Int16Parser, Int16Compiler),
    1135: ("upm", Int16Parser, Int16Compiler),
    1090: ("fond_id", Int16Parser, Int16Compiler),
    1093: ("PostScript Hinting Options", PostScriptGlobalHintingOptionsParser, None),  # noqa: E501
    1068: ("1068", EncodedValueListWithCountParser, EncodedValueListWithCountCompiler),
    1530: ("blue_values_num", Int16Parser, Int16Compiler),
    1531: ("other_blues_num", Int16Parser, Int16Compiler),
    1532: ("family_blues_num", Int16Parser, Int16Compiler),
    1533: ("family_other_blues_num", Int16Parser, Int16Compiler),
    1534: ("stem_snap_h_num", Int16Parser, Int16Compiler),
    1535: ("stem_snap_v_num", Int16Parser, Int16Compiler),
    1267: ("font_style", Int16Parser, Int16Compiler),  # OS/2.fsSelection
    1057: ("pcl_id", Int16Parser, Int16Compiler),
    1058: ("vp_id", Int16Parser, Int16Compiler),
    1060: ("ms_id", Int16Parser, Int16Compiler),
    1059: ("pcl_chars_set", StringParser, StringCompiler),
    1261: ("Binary cvt Table", BaseParser, HexStringCompiler),
    1262: ("Binary prep Table", BaseParser, HexStringCompiler),
    1263: ("Binary fpgm Table", BaseParser, HexStringCompiler),

    # Goes to font.ttinfo:
    1265: ("gasp", GaspParser, None),  # Gasp Ranges
    1264: ("ttinfo", TrueTypeInfoParser, None),
    # Goes to font.ttinfo:
    1271: ("vdmx", VdmxParser, None),
    # Goes to font.ttinfo:
    1270: ("hhea_line_gap", Int16Parser, Int16Compiler),
    1278: ("hhea_ascender", SignedInt16Parser, SignedInt16Compiler),
    1279: ("hhea_descender", SignedInt16Parser, SignedInt16Compiler),
    # hstem_data and vstem_data:
    1266: ("TrueType Stem PPEMs 2 And 3", TrueTypeStemPpems23Parser, None),
    1268: ("TrueType Stem PPEMs", TrueTypeStemPpemsParser, None),
    # Probably in font.ttinfo, but not accessible through API:
    1269: ("TrueType Stems", TrueTypeStemsParser, None),
    1524: ("TrueType Stem PPEMs 1", TrueTypeStemPpems1Parser, None),
    # Probably in font.ttinfo, but not accessible through API:
    1255: ("TrueType Zones", TrueTypeZonesParser, TrueTypeZonesCompiler),
    # Goes to font:
    2021: ("unicoderanges", UnicodeRangesParser, UnicodeRangesCompiler),
    # Probably in font.ttinfo, but not accessible through API:
    1272: ("stemsnaplimit", Int16Parser, Int16Compiler),  # Pixel Snap
    1274: ("zoneppm", Int16Parser, Int16Compiler),  # Zone Stop PPEM
    1275: ("codeppm", Int16Parser, Int16Compiler),  # Code Stop PPEM
    1604: ("1604", Int16Parser, Int16Compiler),  # Binary import? e.g. 255
    2032: ("2032", Int16Parser, Int16Compiler),  # Binary import? e.g. 300
    1273: ("TrueType Zone Deltas", TrueTypeZoneDeltasParser, TrueTypeZoneDeltasCompiler),
    # Goes to font again:
    1138: ("fontnames", NameRecordsParser, None),
    1141: ("Custom CMAPs", CustomCmapParser, None),
    1136: ("PCLT Table", PcltParser, None),
    2022: ("Export PCLT Table", Int16Parser, Int16Compiler),
    2025: ("note", StringParser, StringCompiler),
    2030: ("2030", BaseParser, HexStringCompiler),
    2016: ("customdata", StringParser, StringCompiler),
    2024: ("OpenType Metrics Class Flags", OpenTypeMetricsClassFlagsParser, None),
    2026: ("OpenType Kerning Class Flags", OpenTypeKerningClassFlagsParser, None),

    # Repeat for each binary table:
    # truetypetables: TrueTypeTable
    2014: ("TrueTypeTable", BinaryTableParser, BinaryTableCompiler),

    1276: ("features", OpenTypeStringParser, OpenTypeStringCompiler),

    # Repeat for each OpenType class:
    1277: ("OpenType Class", StringParser, StringCompiler),  # Font.classes

    513: ("513", BaseParser, None),
    271: ("271", BaseParser, None),
    1513: ("Axis Count", Int16Parser, Int16Compiler),
    1514: ("Axis Name", StringParser, StringCompiler),
    1523: ("Anisotropic Interpolation Mappings", AnisotropicInterpolationsParser, None),
    1515: ("Axis Mappings Count", AxisMappingsCountParser, None),
    1516: ("Axis Mappings", AxisMappingsParser, None),

    # Repeat the next two for each master:
    1504: ("Master Name", StringParser, StringCompiler),
    1505: ("Master Location", MasterLocationParser, None),

    1247: ("Primary Instance Locations", DoubleListParser, DoubleListCompiler),
    1254: ("Primary Instances", PrimaryInstancesParser, None),

    # Repeat PostScript Info for each master:
    1536: ("PostScript Info", PostScriptInfoParser, None),

    527: ("527", BaseParser, None),
    1294: ("Global Guides", GlobalGuidesParser, None),
    1296: ("Global Guide Properties", GuidePropertiesParser, None),
    1295: ("Global Mask", GlobalMaskParser, None),
    1066: ("default_character", StringParser, StringCompiler),

    # Begin: Repeat for each glyph
    2001: ("Glyph", GlyphParser, GlyphCompiler),
    # Glyph.hlinks and Glyph.vlinks:
    2008: ("Links", LinkParser, None),
    2007: ("image", BackgroundBitmapParser, None),  # Background Bitmap
    2013: ("Glyph Bitmaps", GlyphBitmapParser, None),
    2023: ("2023", EncodedValueListParser, None),  # 1 encoded value per master
    2019: ("Glyph Sketch", GlyphSketchParser, None),
    2010: ("Glyph Hinting Options", PostScriptGlyphHintingOptionsParser, None),
    2009: ("mask", MaskParser, None),
    2011: ("mask.metrics", MaskMetricsParser, None),  # Single master mask metrics
    2028: ("mask.metrics_mm", MaskMetricsMMParser, None),  # Mask metrics master 2 to 16
    2027: ("Glyph Origin", GlyphOriginParser, None),
    1250: ("unicodes", GlyphUnicodeParser, None),  # Glyph Unicode
    2034: ("2034", StringParser, StringCompiler),
    1253: ("Glyph Unicode Non-BMP", GlyphUnicodeSuppParser, None),
    2012: ("mark", Int16Parser, Int16Compiler),  # Mark Color
    2015: ("glyph.customdata", StringParser, StringCompiler),
    2017: ("glyph.note", StringParser, StringCompiler),
    2018: ("Glyph GDEF Data", GlyphGDEFParser, None),
    2020: ("Glyph Anchors Supplemental", GlyphAnchorsSuppParser, None),
    2029: ("Glyph Anchors MM", GlyphAnchorsParser, None),  # MM-compatible
    2031: ("Glyph Guide Properties", GuidePropertiesParser, None),
    # End: Repeat for each glyph

    1743: ("OpenType Export Options", OpenTypeExportOptionsParser, None),
    1744: ("Export Options", ExportOptionsParser, None),
    1742: ("Mapping Mode", MappingModeParser, None),

    # Not seen in FontNames.vfb:
    1410: ("1410", FL3Type1410Parser, None),

    # File end
    5: ("EOF", None, None),
}
# fmt: on

# Make sure the human-readable keys are unique
all_classes = [key for key, _, _ in parser_classes.values()]
assert len(set(all_classes)) == len(
    all_classes
), f"Duplicate keys in classes: {sorted(all_classes)}"

entry_ids = {v[0]: k for k, v in parser_classes.items()}

# Those entries are ignored in minimal mode:
ignore_minimal = [
    "Global Guides",
    "Global Mask",
    "Glyph Bitmaps",
    "Glyph Guide Properties",
    "glyph.note",
    "image",
    "mark",
    "mask",
    "note",
]
