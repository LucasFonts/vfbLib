set infoEntries [dict create \
    1024 "Style Group Family Name" \
    1025 "Full Font Name" \
    1026 "PostScript Font Name" \
    1027 "Typographic Family Name" \
    1028 "Weight Name" \
    1029 "Italic Angle" \
    1030 "Underline Position" \
    1031 "Underline Thickness" \
    1034 "Monospaced" \
    1037 "Copyright" \
    1038 "Description" \
    1039 "Manufacturer" \
    1044 "Type 1 Unique ID" \
    1046 "Complete Version Record" \
    1047 "1047" \
    1048 "Weight Class" \
    1054 "MS Character Set" \
    1056 "Menu Name" \
    1057 "PCL ID" \
    1058 "VP ID" \
    1060 "MS ID" \
    1061 "Trademark" \
    1062 "Designer" \
    1063 "Designer URL" \
    1064 "Manufacturer URL" \
    1065 "Width Name" \
    1066 "Default Glyph" \
    1068 "1068" \
    1069 "License" \
    1070 "License URL" \
    1090 "FOND Family ID" \
    1092 "FOND Name" \
    1093 "1093" \
    1118 "Panose" \
    1121 "Vendor ID" \
    1127 "Style Name" \
    1128 "TrueType Version Record" \
    1129 "TrueType Unique ID Record" \
    1130 "Version Major" \
    1131 "Version Minor" \
    1132 "Year" \
    1133 "Type 1 XUIDs" \
    1134 "Type 1 XUIDs Count" \
    1135 "Units Per Em" \
    1136 "1136" \
    1137 "Typographic Style Name" \
    1138 "1138" \
    1139 "OT Mac Name" \
    1140 "1140" \
    1141 "1141" \
    1250 "Glyph Unicode" \
    1254 "Primary Instances" \
    1255 "TrueType Zones" \
    1264 "Metrics" \
    1265 "Gasp Ranges" \
    1267 "Selection" \
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
    1530 "Blue Values Count" \
    1531 "Other Blues Count" \
    1532 "Family Blues Count" \
    1533 "Family Other Blues Count" \
    1534 "StemSnapH Count" \
    1535 "StemSnapV Count" \
    1536 "PostScript Info" \
    1604 "1604" \
    1742 "1742" \
    1743 "1743" \
    1744 "1744" \
    2001 "Glyph" \
    2007 "Background" \
    2008 "Links" \
    2009 "Mask" \
    2012 "Mark Color" \
    2015 "Glyph User Data" \
    2016 "Font User Data" \
    2017 "Glyph Note" \
    2018 "Glyph GDEF Data" \
    2020 "Glyph Anchors Supplemental" \
    2021 "Unicode Ranges" \
    2023 "2023" \
    2025 "Font Note" \
    2026 "OpenType Class Flags" \
    2027 "Glyph Origin" \
    2029 "Glyph Anchors MM" \
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

proc readEncodedValue {} {
    section "Encoded Value" {
        set raw [uint8 "Byte 1"]
        if {$raw < 0xF7} {
            entry "Value" [expr $raw - 0x8B]
        } elseif {$raw < 0xFA} {
            set raw2 [uint8 "Byte 2"]
            entry "Value" [expr $raw - 0x8B + ($raw - 0xF7) * 0xFF + $raw2]
        } elseif {$raw < 0xFF} {
            set raw2 [uint8 "Byte 2"]
            entry "Value" [expr 0x8F - $raw - ($raw - 0xFB) * 0xFF - $raw2]
        } elseif {$raw == 0xFF} {
            # set raw2 [uint8 "Byte 2"]
            # set raw3 [uint8 "Byte 3"]
            # set raw4 [uint8 "Byte 4"]
            # set raw5 [uint8 "Byte 5"]
            set bytes [uint32 "Bytes 2-5"]
            binary scan $bytes S val
            entry "Value" $val
        } 
    }
}

section "Header" {
    uint8 "Field 0"
    str 5 "ascii" "Filetype"
    uint16 "Field 1"
    uint8 "Field 2"
    uint8 "Field 3"
    set num 1
    while {$num < 24} {
        uint16 "Value"
        incr num
    }
    uint8 "Field 4"
    readEncodedValue
    uint8 "Field 5"
    readEncodedValue
    uint8 "Field 6"
    readEncodedValue
    uint8 "Field 7"
    uint16 "NumGlyphs"
    uint16 "NumGlyphs"
    # readInfoEntry
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
    #     while {$numGlyphs < 128} {
    #         section "Glyph" {
    #             uint16 "EntryType"
    #             set entryLength [uint16 "Entry Length"]
    #             uint16 "Glyph ID"
    #             str [expr $entryLength - 2] "ascii" "Glyph Name"
    #         }
    #         incr numGlyphs
    #     }
    # }
}

section "Data" {
    while {![end]} {
        readInfoEntry
    }
}