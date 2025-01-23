from vfbLib.compilers.base import GlyphEncodingCompiler
from vfbLib.compilers.binary import BinaryTableCompiler
from vfbLib.compilers.glyph import GlyphCompiler
from vfbLib.compilers.numeric import Int16Compiler
from vfbLib.compilers.text import OpenTypeStringCompiler, StringCompiler
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
    GlyphAnchorsParser,
    GlyphAnchorsSuppParser,
    GlyphGDEFParser,
    GlyphOriginParser,
    GlyphParser,
    GlyphSketchParser,
    GlyphUnicodeParser,
    GlyphUnicodeSuppParser,
    LinkParser,
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
from vfbLib.parsers.ps import PostScriptInfoParser
from vfbLib.parsers.text import NameRecordsParser, OpenTypeStringParser, StringParser
from vfbLib.parsers.truetype import (
    TrueTypeInfoParser,
    TrueTypeStemPpems1Parser,
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
    1026: ("font_name", StringParser, StringCompiler),  # psn
    1503: ("Master Count", Int16Parser, Int16Compiler),
    1517: ("weight_vector", DoubleListParser, None),  # Default Weight Vector, one value per master # noqa: E501
    1044: ("unique_id", SignedInt32Parser, None),  # Type 1 Unique ID
    1046: ("version", StringParser, StringCompiler),  # version full
    1038: ("notice", StringParser, StringCompiler),  # description
    1025: ("full_name", StringParser, StringCompiler),  # ffn
    1027: ("family_name", StringParser, StringCompiler),  # tfn
    1024: ("pref_family_name", StringParser, StringCompiler),  # sgn
    1056: ("menu_name", StringParser, StringCompiler),  # Menu Name
    1092: ("apple_name", StringParser, StringCompiler),  # FOND Name
    1028: ("weight", StringParser, StringCompiler),  # weight_name
    1065: ("width", StringParser, StringCompiler),  # width_name

    # Is license/url not in Python API?
    1069: ("License", StringParser, StringCompiler),
    1070: ("License URL", StringParser, StringCompiler),

    1037: ("copyright", StringParser, StringCompiler),  # OK!
    1061: ("trademark", StringParser, StringCompiler),  # OK!
    1062: ("designer", StringParser, StringCompiler),  # OK!
    1063: ("designer_url", StringParser, StringCompiler),  # designerURL
    1064: ("vendor_url", StringParser, StringCompiler),  # manufacturerURL
    1039: ("source", StringParser, StringCompiler),  # manufacturer, "created by"
    1034: ("is_fixed_pitch", Int16Parser, Int16Compiler),  # Monospaced
    1048: ("weight_code", SignedInt16Parser, None),  # Weight Class, was: weight
    1029: ("italic_angle", DoubleParser, None),  # Italic Angle
    1047: ("slant_angle", DoubleParser, None),  # Slant Angle
    1030: ("underline_position", SignedInt16Parser, None),  # underlinePosition
    1031: ("underline_thickness", Int16Parser, Int16Compiler),  # underlineThickness
    1054: ("ms_charset", Int16Parser, Int16Compiler),  # MS Character Set
    1118: ("panose", PanoseParser, None),  # OK!
    1128: ("tt_version", StringParser, StringCompiler),  # version
    1129: ("tt_u_id", StringParser, StringCompiler),  # UniqueID
    1127: ("style_name", StringParser, StringCompiler),  # Style Name
    1137: ("pref_style_name", StringParser, StringCompiler),  # tsn
    1139: ("mac_compatible", StringParser, StringCompiler),  # OT Mac Name
    1140: ("1140", BaseParser, None),
    1121: ("vendor", StringParser, StringCompiler),  # vendorID
    1133: ("x_u_id", IntListParser, None),  # Type 1 XUIDs
    1134: ("x_u_id_num", Int16Parser, Int16Compiler),  # Type 1 XUIDs Count
    1132: ("year", Int16Parser, Int16Compiler),  # OK!
    1130: ("version_major", Int16Parser, Int16Compiler),  # versionMajor
    1131: ("version_minor", Int16Parser, Int16Compiler),  # versionMinor
    1135: ("upm", Int16Parser, Int16Compiler),  # OK!
    1090: ("fond_id", Int16Parser, Int16Compiler),  # FOND Family ID
    1093: ("1093", BaseParser, None),
    1068: ("1068", EncodedValueListWithCountParser, None),
    1530: ("blue_values_num", Int16Parser, Int16Compiler),  # Blue Values Count
    1531: ("other_blues_num", Int16Parser, Int16Compiler),  # Other Blues Count
    1532: ("family_blues_num", Int16Parser, Int16Compiler),  # Family Blues Count
    1533: ("family_other_blues_num", Int16Parser, Int16Compiler),  # Family Other Blues Count  # noqa: E501
    1534: ("stem_snap_h_num", Int16Parser, Int16Compiler),  # StemSnapH Count
    1535: ("stem_snap_v_num", Int16Parser, Int16Compiler),  # StemSnapV Count
    1267: ("font_style", Int16Parser, Int16Compiler),  # Selection
    1057: ("pcl_id", Int16Parser, Int16Compiler),  # PCL ID
    1058: ("vp_id", Int16Parser, Int16Compiler),  # VP ID
    1060: ("ms_id", Int16Parser, Int16Compiler),  # MS ID
    1059: ("1059", BaseParser, None),
    1261: ("Binary cvt Table", BaseParser, None),
    1262: ("Binary prep Table", BaseParser, None),
    1263: ("Binary fpgm Table", BaseParser, None),

    # Goes to font.ttinfo:
    1265: ("gasp", GaspParser, None),  # Gasp Ranges
    1264: ("ttinfo", TrueTypeInfoParser, None),  # TrueType Info
    # Goes to font.ttinfo:
    1271: ("vdmx", VdmxParser, None),
    # Goes to font.ttinfo:
    1270: ("hhea_line_gap", Int16Parser, Int16Compiler),  # OK!
    1278: ("hhea_ascender", SignedInt16Parser, None),  # OK!
    1279: ("hhea_descender", SignedInt16Parser, None),  # OK!
    # hstem_data and vstem_data:
    1268: ("TrueType Stem PPEMs", TrueTypeStemPpemsParser, None),
    1524: ("TrueType Stem PPEMs 1", TrueTypeStemPpems1Parser, None),
    # Probably in font.ttinfo, but not accessible through API:
    1269: ("TrueType Stems", TrueTypeStemsParser, None),
    1255: ("TrueType Zones", TrueTypeZonesParser, None),
    # Goes to font:
    2021: ("unicoderanges", UnicodeRangesParser, None),  # Unicode Ranges
    # Probably in font.ttinfo, but not accessible through API:
    1272: ("Pixel Snap", Int16Parser, Int16Compiler),
    1274: ("zoneppm", Int16Parser, Int16Compiler),  # Zone Stop PPEM
    1275: ("codeppm", Int16Parser, Int16Compiler),  # Code Stop PPEM
    1604: ("1604", Int16Parser, Int16Compiler),  # Binary import? e.g. 255
    2032: ("2032", Int16Parser, Int16Compiler),  # Binary import? e.g. 300
    1273: ("TrueType Zone Deltas", TrueTypeZoneDeltasParser, None),
    # Goes to font again:
    1138: ("fontnames", NameRecordsParser, None),  # Name Records
    1141: ("Custom CMAPs", CustomCmapParser, None),
    1136: ("PCLT Table", PcltParser, None),
    2022: ("Export PCLT Table", Int16Parser, Int16Compiler),
    2025: ("note", StringParser, StringCompiler),  # fontNote
    2030: ("2030", BaseParser, None),
    2016: ("customdata", StringParser, StringCompiler),  # Font User Data
    2024: ("OpenType Metrics Class Flags", OpenTypeMetricsClassFlagsParser, None),
    2026: ("OpenType Kerning Class Flags", OpenTypeKerningClassFlagsParser, None),

    # Repeat for each binary table:
    # truetypetables: TrueTypeTable
    2014: ("TrueTypeTable", BinaryTableParser, BinaryTableCompiler),  # Binary Table

    1276: ("features", OpenTypeStringParser, OpenTypeStringCompiler),  # openTypeFeatures # noqa: E501

    # Repeat for each OpenType class:
    # font.classes
    1277: ("OpenType Class", StringParser, StringCompiler),  # OpenType Class

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

    1247: ("Primary Instance Locations", DoubleListParser, None),
    1254: ("Primary Instances", PrimaryInstancesParser, None),

    # Repeat PostScript Info for each master:
    1536: ("PostScript Info", PostScriptInfoParser, None),

    527: ("527", BaseParser, None),
    1294: ("Global Guides", GlobalGuidesParser, None),
    1296: ("Global Guide Properties", GuidePropertiesParser, None),
    1066: ("default_character", StringParser, StringCompiler),  # Default Glyph

    # Begin: Repeat for each glyph
    2001: ("Glyph", GlyphParser, GlyphCompiler),
    # Glyph.hlinks and Glyph.vlinks:
    2008: ("Links", LinkParser, None),
    2007: ("image", BackgroundBitmapParser, None),  # Background Bitmap
    2013: ("Glyph Bitmaps", GlyphBitmapParser, None),
    2023: ("2023", EncodedValueListParser, None),  # 1 encoded value per master
    2019: ("Glyph Sketch", GlyphSketchParser, None),
    2010: ("2010", BaseParser, None),
    2009: ("mask", MaskParser, None),  # Mask
    # Mask width master 1?: Two ints or one long int?
    2011: ("2011", BaseParser, None),
    # Mask width master 2?:
    2028: ("2028", EncodedValueListParser, None),  # MM, proportional to num of masters
    2027: ("Glyph Origin", GlyphOriginParser, None),
    1250: ("unicodes", GlyphUnicodeParser, None),  # Glyph Unicode
    1253: ("Glyph Unicode Non-BMP", GlyphUnicodeSuppParser, None),
    2012: ("mark", Int16Parser, Int16Compiler),  # Mark Color
    2015: ("glyph.customdata", StringParser, StringCompiler),  # Glyph User Data
    2017: ("glyph.note", StringParser, StringCompiler),  # Glyph Note
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
}
# fmt: on

# Make sure the human-readable keys are unique
all_classes = [key for key, _, _ in parser_classes.values()]
assert len(set(all_classes)) == len(
    all_classes
), f"Duplicate keys in classes: {sorted(all_classes)}"

entry_ids = {v[0]: k for k, v in parser_classes.items()}

ignore_minimal = [
    "Background Bitmap",
    "note",
    "Global Guides",
    "Glyph Bitmaps",
    "Glyph Guide Properties",
    "mark",
    "mask",
]
