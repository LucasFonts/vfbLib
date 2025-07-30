from __future__ import annotations

from enum import IntEnum


class F(IntEnum):
    EncodingDefault = 1501
    Encoding = 1500
    E1502 = 1502
    E518 = 518
    E257 = 257
    font_name = 1026
    MasterCount = 1503
    weight_vector = 1517
    unique_id = 1044
    version = 1046
    notice = 1038
    full_name = 1025
    family_name = 1027
    pref_family_name = 1024
    menu_name = 1056
    apple_name = 1092
    weight = 1028
    width = 1065
    License = 1069
    LicenseURL = 1070
    copyright = 1037
    trademark = 1061
    designer = 1062
    designer_url = 1063
    vendor_url = 1064
    source = 1039
    is_fixed_pitch = 1034
    weight_code = 1048
    italic_angle = 1029
    slant_angle = 1047
    underline_position = 1030
    underline_thickness = 1031
    ms_charset = 1054
    panose = 1118
    tt_version = 1128
    tt_u_id = 1129
    style_name = 1127
    pref_style_name = 1137
    mac_compatible = 1139
    E1140 = 1140
    vendor = 1121
    xuid = 1133
    xuid_num = 1134
    year = 1132
    version_major = 1130
    version_minor = 1131
    upm = 1135
    fond_id = 1090
    PostScriptHintingOptions = 1093
    E1068 = 1068
    blue_values_num = 1530
    other_blues_num = 1531
    family_blues_num = 1532
    family_other_blues_num = 1533
    stem_snap_h_num = 1534
    stem_snap_v_num = 1535
    font_style = 1267
    pcl_id = 1057
    vp_id = 1058
    ms_id = 1060
    pcl_chars_set = 1059
    ttinfo = 1264
    unicoderanges = 2021
    fontnames = 1138
    CustomCMAPs = 1141
    PCLTTable = 1136
    ExportPCLTTable = 2022
    note = 2025
    E2030 = 2030
    customdata = 2016
    MetricsClassFlags = 2024
    KerningClassFlags = 2026
    TrueTypeTable = 2014  # Font.truetypetables
    features = 1276
    GlyphClass = 1277  # Font.classes
    E513 = 513
    E271 = 271
    AxisCount = 1513
    AxisName = 1514
    AnisotropicInterpolationMappings = 1523
    AxisMappingsCount = 1515
    AxisMappings = 1516
    PrimaryInstanceLocations = 1247
    PrimaryInstances = 1254
    E527 = 527
    GlobalGuides = 1294
    GlobalGuideProperties = 1296
    GlobalMask = 1295
    default_character = 1066
    OpenTypeExportOptions = 1743
    ExportOptions = 1744
    MappingMode = 1742
    E272 = 272
    E1410 = 1410
    E528 = 528
    EOF = 5


class G(IntEnum):
    Glyph = 2001
    Links = 2008  # Glyph.hlinks and Glyph.vlinks
    image = 2007
    Bitmaps = 2013
    E2023 = 2023
    Sketch = 2019
    HintingOptions = 2010
    mask = 2009
    MaskMetrics = 2011  # was: mask.metrics
    MaskMetricsMM = 2028  # was: mask.metrics_mm
    Origin = 2027
    unicodes = 1250
    E2034 = 2034
    UnicodesNonBMP = 1253
    mark = 2012
    customdata = 2015
    note = 2017
    GDEFData = 2018
    AnchorsProperties = 2020
    AnchorsMM = 2029
    GuideProperties = 2031


class M(IntEnum):
    MasterName = 1504
    MasterLocation = 1505
    PostScriptInfo = 1536


class T(IntEnum):
    cvt = 1261
    prep = 1262
    fpgm = 1263
    gasp = 1265
    vdmx = 1271
    hhea_line_gap = 1270
    hhea_ascender = 1278
    hhea_descender = 1279
    # hstem_data and vstem_data:
    TrueTypeStemPPEMs2And3 = 1266
    TrueTypeStemPPEMs = 1268
    TrueTypeStems = 1269
    TrueTypeStemPPEMs1 = 1524
    TrueTypeZones = 1255
    stemsnaplimit = 1272
    zoneppm = 1274
    codeppm = 1275
    E1604 = 1604
    E2032 = 2032
    TrueTypeZoneDeltas = 1273
