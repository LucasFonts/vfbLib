set infoEntries [dict create \
    1024 "Family Name" \
    1025 "Full Name" \
    1026 "PostScript Font Name" \
    1027 "OT Family Name?" \
    1028 "Weight?" \
    1029 "1029" \
    1030 "1030" \
    1031 "1031" \
    1034 "1034" \
    1037 "Copyright" \
    1038 "Description" \
    1039 "Created By" \
    1044 "1044" \
    1046 "Complete Version Record" \
    1047 "1047" \
    1048 "1048" \
    1054 "1054" \
    1056 "1056" \
    1061 "Trademark" \
    1062 "Designer" \
    1063 "Designer URL" \
    1064 "Vendor URL" \
    1065 "Width" \
    1068 "1068" \
    1069 "Italic?" \
    1070 "Bold?" \
    1090 "1090" \
    1092 "1092" \
    1093 "1093" \
    1118 "1118" \
    1121 "Vendor ID" \
    1127 "Style Name" \
    1128 "TrueType Version Record" \
    1129 "TrueType Unique ID Record" \
    1130 "1130" \
    1131 "1131" \
    1132 "1132" \
    1133 "1133" \
    1134 "1134" \
    1135 "1135" \
    1137 "OT Style Name?" \
    1138 "1138" \
    1139 "Mac Name?" \
    1140 "1140" \
    1250 "Glyph Unicode" \
    1254 "Primary Instances" \
    1255 "TrueType Zones" \
    1269 "TrueType Stems" \
    1276 "OpenType Features" \
    1277 "OpenType Class" \
    1500 "Glyph Name" \
    1504 "Master Name" \
    1514 "Axis Name" \
    1517 "1517" \
    1530 "1530" \
    1531 "1531" \
    1532 "1532" \
    1533 "1533" \
    1536 "1536" \
    2016 "Font User Data" \
    2018 "Anchors" \
    2025 "Font Note" \
    2026 "OpenType Class Flags?" \

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
        entry "Label" [lookupName $eid]
        set entryLength [uint16 "Bytes"]
        if {$entryLength > 0} {
            str $entryLength "ascii" "Value"
        }
    }
}

section "Header" {
    str 6 "ascii" "Filetype"
    uint16 "Header 1"
    uint16 "Header 2"
    bytes 34 "Reserved"
    uint32 "Bla"
    uint32 "Blub"
    uint16 "Field 1"
    uint16 "Field 2"
    uint16 "Field 3"
    uint16 "Field 4"
    uint16 "Field 5"
    uint16 "Field 6"
    uint16 "Field 7"
    readInfoEntry
    section -collapsed "Simple Glyphs" {
        set numGlyphs 0
        while {$numGlyphs < 256} {
            section "Glyph" {
                uint16 "EntryType"
                set entryLength [uint16 "Entry Length"]
                uint16 "Glyph ID"
                str [expr $entryLength - 2] "ascii" "Glyph Name"
            }
            incr numGlyphs
        }
    }
    section "Font Info" {
        while {![end]} {
            readInfoEntry
        }
    }
}