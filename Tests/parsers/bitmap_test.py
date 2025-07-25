from unittest import TestCase

from vfbLib.parsers.bitmap import BackgroundBitmapParser, pprint_bitmap

bitmaps = [
    {
        "ppm": 15,
        "origin": [0, -1],
        "adv": [8, 0],
        "size_pixels": [9, 10],
        "data": {
            "bytes": [
                0,
                0,
                59,
                0,
                102,
                0,
                102,
                0,
                62,
                0,
                6,
                0,
                102,
                0,
                102,
                0,
                60,
                254,
            ],
            "extra": [0],
        },
    },
    {
        "ppm": 14,
        "origin": [0, -1],
        "adv": [8, 0],
        "size_pixels": [8, 9],
        "data": {
            "bytes": [
                0,
                0,
                59,
                0,
                102,
                0,
                102,
                0,
                62,
                0,
                6,
                0,
                102,
                0,
                60,
                254,
            ],
            "extra": [0],
        },
    },
    {
        "ppm": 13,
        "origin": [0, -1],
        "adv": [7, 0],
        "size_pixels": [8, 9],
        "data": {"extra": [239, 0]},
    },
    {
        "ppm": 16,
        "origin": [0, -1],
        "adv": [9, 0],
        "size_pixels": [9, 10],
        "data": {
            "bytes": [
                254,
                128,
                254,
                128,
                254,
                128,
                254,
                128,
                254,
                128,
                254,
                128,
                254,
                128,
                170,
                128,
                85,
                0,
                0,
            ],
            "extra": [128],
        },
    },
    {
        "ppm": 10,
        "origin": [-1, -1],
        "adv": [5, 0],
        "size_pixels": [7, 7],
        "data": {"bytes": [0, 0, 52, 0, 72, 0, 56, 0, 8, 0, 112, 254], "extra": [0]},
    },
    {
        "ppm": 11,
        "origin": [-1, -1],
        "adv": [6, 0],
        "size_pixels": [8, 8],
        "data": {
            "bytes": [0, 0, 54, 0, 76, 0, 68, 0, 60, 0, 4, 0, 56, 254],
            "extra": [0],
        },
    },
    {
        "ppm": 8,
        "origin": [-1, -1],
        "adv": [4, 0],
        "size_pixels": [6, 6],
        "data": {"bytes": [0, 0, 104, 0, 88, 0, 8, 0, 112, 254], "extra": [0]},
    },
    {
        "ppm": 9,
        "origin": [-1, -1],
        "adv": [5, 0],
        "size_pixels": [7, 7],
        "data": {"bytes": [0, 0, 52, 0, 72, 0, 56, 0, 8, 0, 112, 254], "extra": [0]},
    },
]


# class BitmapTest(TestCase):
#     def test_pprint_bitmap_15(self):
#         bitmap = bitmaps[0]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "                  ",
#             "    ████████    ██",
#             "  ████    ████    ",
#             "  ████    ████    ",
#             "          ████    ",
#             "    ██████████    ",
#             "  ████    ████    ",
#             "  ████    ████    ",
#             "    ██████  ████  ",
#             "                  ",
#         ]

#     def test_pprint_bitmap_14(self):
#         bitmap = bitmaps[1]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "                ",
#             "    ████████    ",
#             "  ████    ████  ",
#             "          ████  ",
#             "    ██████████  ",
#             "  ████    ████  ",
#             "  ████    ████  ",
#             "    ██████  ████",
#             "                ",
#         ]

#     def test_pprint_bitmap_13(self):
#         bitmap = bitmaps[2]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#             "                ",
#         ]

#     def test_pprint_bitmap_16(self):
#         bitmap = bitmaps[3]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "                  ",
#             "  ██  ██  ██  ██  ",
#             "██  ██  ██  ██  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#             "██████████████  ██",
#         ]

#     def test_pprint_bitmap_10(self):
#         bitmap = bitmaps[4]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "              ",
#             "  ██████      ",
#             "        ██    ",
#             "    ██████    ",
#             "  ██    ██    ",
#             "    ████  ██  ",
#             "              ",
#         ]

#     def test_pprint_bitmap_11(self):
#         bitmap = bitmaps[5]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "                ",
#             "    ██████      ",
#             "          ██    ",
#             "    ████████    ",
#             "  ██      ██    ",
#             "  ██    ████    ",
#             "    ████  ████  ",
#             "                ",
#         ]

#     def test_pprint_bitmap_8(self):
#         bitmap = bitmaps[6]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "            ",
#             "  ██████    ",
#             "        ██  ",
#             "  ██  ████  ",
#             "  ████  ██  ",
#             "            ",
#         ]

#     def test_pprint_bitmap_9(self):
#         bitmap = bitmaps[7]
#         gfx = pprint_bitmap(bitmap, invert=True)
#         assert gfx == [
#             "              ",
#             "  ██████      ",
#             "        ██    ",
#             "    ██████    ",
#             "  ██    ██    ",
#             "    ████  ██  ",
#             "              ",
#         ]


image_bin = (
    "fb3a"  # -166, origin x
    "fb64"  # -208, origin y
    "f9d5f9ab"  # 833 791, size in font units
    "a3a3"  # 24 24, size in pixels
    "ec"  # 97
    "07"
    "667777ff"
    "400001ff"
    "fe0000ff"
    "fe0008ff"
    "400001ff"
    "400001ff"
    "fe0000ff"
    "fe0018ff"
    "4ca241ff"
    "4ca241ff"
    "0aa240ff"
    "0aa240ff"
    "49b241ff"
    "499c79ff"
    "fe0000ff"
    "fe0008ff"
    "400001ff"
    "400001ff"
    "fe0000ff"
    "fe0008ff"
    "400001ff"
    "777773ff"
    "fe0000ff"
    "fe0000ff"
)

image_dict = {
    "origin": (-166, -208),
    "size_units": (833, 791),
    "size_pixels": (24, 24),
    "len": 97,
    "bitmap": {
        "flag": 7,
        "data": [
            # 01110111 01100110, 11111111 01110111,
            [
                30566,
                65399,
            ],
            64,
            65281,
            254,
            65280,
            254,
            65288,
            64,
            65281,
            64,
            65281,
            254,
            65280,
            254,
            65304,
            41548,
            65345,
            41548,
            65345,
            41482,
            65344,
            41482,
            65344,
            45641,
            65345,
            40009,
            65401,
            254,
            65280,
            254,
            65288,
            64,
            65281,
            64,
            65281,
            254,
            65280,
            254,
            65288,
            64,
            65281,
            30583,
            65395,
            254,
            65280,
            254,
            65280,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ],
    },
}


class BackgroundBitmapParserTest(TestCase):
    def test_1(self):
        result = BackgroundBitmapParser().parse_hex(image_bin)
        assert result == image_dict
