TT_COMMANDS = {
    0x01: {"name": "AlignTop", "params": ["pt", "zone"]},
    0x02: {"name": "AlignBottom", "params": ["pt", "zone"]},
    0x03: {
        "name": "SingleLinkH",
        "params": ["pt1", "pt2", "stem", "align"],
    },
    0x04: {
        "name": "SingleLinkV",
        "params": ["pt1", "pt2", "stem", "align"],
    },
    0x05: {
        "name": "DoubleLinkH",
        "params": ["pt1", "pt2", "stem"],
    },
    0x06: {
        "name": "DoubleLinkV",
        "params": ["pt1", "pt2", "stem"],
    },
    0x07: {"name": "AlignH", "params": ["pt", "align"]},
    0x08: {"name": "AlignV", "params": ["pt", "align"]},
    0x0D: {
        "name": "InterpolateH",
        "params": ["pti", "pt1", "pt2", "align"],
    },
    0x0E: {
        "name": "InterpolateV",
        "params": ["pti", "pt1", "pt2", "align"],
    },
    0x14: {
        "name": "MiddleDeltaH",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x15: {
        "name": "MiddleDeltaV",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x16: {
        "name": "FinalDeltaH",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
    0x16: {
        "name": "FinalDeltaV",
        "params": ["pt", "shift", "ppm1", "ppm2"],
    },
}