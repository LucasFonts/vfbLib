set infoEntries [dict create \
    1024 "Family Name" \
    1025 "Full Name" \
    1026 "PostScript Font Name" \
    1027 "OT Family Name?" \
    1028 "Weight?" \
    1029 "1029" \
    1030 "1030" \
    1031 "Underline Thickness?" \
    1034 "1034" \
    1037 "Copyright" \
    1038 "Description" \
    1039 "Created By" \
    1044 "1044" \
    1046 "Complete Version Record" \
    1047 "1047" \
    1048 "Weight Class" \
    1054 "1054" \
    1056 "1056" \
    1060 "1060" \
    1061 "Trademark" \
    1062 "Designer" \
    1063 "Designer URL" \
    1064 "Vendor URL" \
    1065 "Width" \
    1066 "Default Glyph" \
    1068 "1068" \
    1069 "Italic?" \
    1070 "Bold?" \
    1090 "1090" \
    1092 "1092" \
    1093 "1093" \
    1118 "Panose" \
    1121 "Vendor ID" \
    1127 "Style Name" \
    1128 "TrueType Version Record" \
    1129 "TrueType Unique ID Record" \
    1130 "Version Major" \
    1131 "Version Minor" \
    1132 "Year" \
    1133 "1133" \
    1134 "1134" \
    1135 "Units Per Em" \
    1136 "1136" \
    1137 "OT Style Name?" \
    1138 "1138" \
    1139 "Mac Name?" \
    1140 "1140" \
    1141 "1141" \
    1250 "Glyph Unicode" \
    1254 "Primary Instances" \
    1255 "TrueType Zones" \
    1264 "Metrics" \
    1265 "Gasp Ranges" \
    1267 "1267" \
    1269 "TrueType Stems" \
    1270 "hhea Line Gap" \
    1272 "Pixel Snap" \
    1273 "1273" \
    1274 "Zone Stop PPEM" \
    1275 "Code Stop PPEM" \
    1276 "OpenType Features" \
    1277 "OpenType Class" \
    1278 "hhea Ascender" \
    1279 "hhea Descender" \
    1294 "1294" \
    1296 "1296" \
    1500 "Encoding" \
    1502 "1502" \
    1504 "Master Name" \
    1514 "Axis Name" \
    1517 "1517" \
    1524 "1524" \
    1530 "1530" \
    1531 "1531" \
    1532 "1532" \
    1533 "1533" \
    1534 "1534" \
    1535 "1535" \
    1536 "1536" \
    1604 "1604" \
    1742 "1742" \
    1743 "1743" \
    1744 "1744" \
    2001 "Glyph" \
    2007 "Background" \
    2008 "Links" \
    2009 "Mask" \
    2015 "Glyph User Data" \
    2016 "Font User Data" \
    2018 "Glyph GDEF Data" \
    2020 "2020" \
    2023 "2023" \
    2025 "Font Note" \
    2026 "OpenType Class Flags" \
    2031 "2031" \
    2032 "2032" \
]

proc lookupName {id} {
    global infoEntries
    if ([dict exists $infoEntries $id]) {
        return [dict get $infoEntries $id]
    } else {
        return $id
    }
}

proc readInfoEntry {} {
    section "Info Entry" {
        set eid [uint16 "Entry Type"]
        if {$eid & 0x8000} {
            entry "Label" [lookupName [expr $eid - 0x8000]]
            set entryLength [uint32 "Bytes"]
        } else {
            entry "Label" [lookupName $eid]
            set entryLength [uint16 "Bytes"]
        }
        if {$entryLength > 0} {
            str $entryLength "ascii" "Value"
        }
    }
}

section "Header" {
    str 6 "ascii" "Filetype"
    readInfoEntry
    uint16 "Field 3"
    set num 1
    while {$num < 11} {
        uint8 "Value"
        incr num
    }
    readInfoEntry
    # uint16 "Field 4"
    # set eid [uint16 "Entry Type"]
    # entry "Label" [lookupName [expr $eid - 0x8000]]
    # set entryLength [uint32 "Bytes"]
    # uint16 "Field 5"
    # uint16 "Field 6"
    # uint16 "Field 7"
    # readInfoEntry
    # section -collapsed "Simple Glyphs" {
    #     set numGlyphs 0
    #     while {$numGlyphs < 256} {
    #         section "Glyph" {
    #             uint16 "EntryType"
    #             set entryLength [uint16 "Entry Length"]
    #             uint16 "Glyph ID"
    #             str [expr $entryLength - 2] "ascii" "Glyph Name"
    #         }
    #         incr numGlyphs
    #     }
    # }
    section "Data" {
        while {![end]} {
            readInfoEntry
        }
    }
}