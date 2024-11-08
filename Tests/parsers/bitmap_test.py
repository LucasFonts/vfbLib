from unittest import TestCase
from vfbLib.parsers.bitmap import pprint_bitmap


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


class BitmapTest(TestCase):
    def test_pprint_bitmap_15(self):
        bitmap = bitmaps[0]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "                  ",
            "    ████████    ██",
            "  ████    ████    ",
            "  ████    ████    ",
            "          ████    ",
            "    ██████████    ",
            "  ████    ████    ",
            "  ████    ████    ",
            "    ██████  ████  ",
            "                  ",
        ]

    def test_pprint_bitmap_14(self):
        bitmap = bitmaps[1]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "                ",
            "    ████████    ",
            "  ████    ████  ",
            "          ████  ",
            "    ██████████  ",
            "  ████    ████  ",
            "  ████    ████  ",
            "    ██████  ████",
            "                ",
        ]

    def test_pprint_bitmap_13(self):
        bitmap = bitmaps[2]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
            "                ",
        ]

    def test_pprint_bitmap_16(self):
        bitmap = bitmaps[3]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "                  ",
            "  ██  ██  ██  ██  ",
            "██  ██  ██  ██  ██",
            "██████████████  ██",
            "██████████████  ██",
            "██████████████  ██",
            "██████████████  ██",
            "██████████████  ██",
            "██████████████  ██",
            "██████████████  ██",
        ]

    def test_pprint_bitmap_10(self):
        bitmap = bitmaps[4]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "              ",
            "  ██████      ",
            "        ██    ",
            "    ██████    ",
            "  ██    ██    ",
            "    ████  ██  ",
            "              ",
        ]

    def test_pprint_bitmap_11(self):
        bitmap = bitmaps[5]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "                ",
            "    ██████      ",
            "          ██    ",
            "    ████████    ",
            "  ██      ██    ",
            "  ██    ████    ",
            "    ████  ████  ",
            "                ",
        ]

    def test_pprint_bitmap_8(self):
        bitmap = bitmaps[6]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "            ",
            "  ██████    ",
            "        ██  ",
            "  ██  ████  ",
            "  ████  ██  ",
            "            ",
        ]

    def test_pprint_bitmap_9(self):
        bitmap = bitmaps[7]
        gfx = pprint_bitmap(bitmap, invert=True)
        assert gfx == [
            "              ",
            "  ██████      ",
            "        ██    ",
            "    ██████    ",
            "  ██    ██    ",
            "    ████  ██  ",
            "              ",
        ]
