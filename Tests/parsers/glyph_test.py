from unittest import TestCase

from vfbLib.parsers.glyph import GlyphParser


class GlyphParserTest(TestCase):
    def test_glyph_1(self):
        # fmt: off
        data = (
            "01090701"              # constant
            "01"                    # glyph name
            "91 64 61 67 67 65 72"  # [6]dagger
            "08"                    # outlines
               "8c f730 a5"
               "00 f77d a5"
               "01 8b f774"
               "01 a5 f757"
               "01 ac 8b"
               "01 a5 fb57"
               "01 8b fb74"
               "01 71 fb76"
               "01 6a 8b"
               "00 fb67 f968"
               "01 e2 8b"
               "01 f16f"
               "01 8b 6f"
               "01 25 6f"
               "01 34 8b"
               "00 f74d f771"
               "01 8b e2"
               "01 e0 8b"
               "01 8b 34"
               "01 71 fb22"
               "01 6a 8b"
               "00 c2 58"
               "01 8b a7"
               "01 f1a7"
               "01 e2 8b"
               "01 8b 37"
               "01 34 8b"
            "02"                    # metrics
               "f8bb 8b"
            "03"                    # Hints
               "8e f980 77 fb47 76 f84c df 8c f77d e0 8b"
            "04"                    # Guides
               "8b 8b"
            "0a"                    # TrueType commands
               "a3 90"
               "01 9a 8e"
               "02 92 8c"
               "06 93 98 8a"
               "04 93 a1 8a 8a"
               "04 98 a4 8a 8a"
               "8b 8b 8b"
            "0f"                    # End of glyph
        )
        # fmt: on
        expected = {
            "name": "dagger",
            "num_masters": 1,
            "nodes": [
                {"type": "move", "flags": 0, "points": [[(233, 26)]]},
                {"type": "line", "flags": 0, "points": [[(233, 250)]]},
                {"type": "line", "flags": 0, "points": [[(259, 445)]]},
                {"type": "line", "flags": 0, "points": [[(292, 445)]]},
                {"type": "line", "flags": 0, "points": [[(318, 250)]]},
                {"type": "line", "flags": 0, "points": [[(318, 26)]]},
                {"type": "line", "flags": 0, "points": [[(292, -200)]]},
                {"type": "line", "flags": 0, "points": [[(259, -200)]]},
                {"type": "move", "flags": 0, "points": [[(48, 524)]]},
                {"type": "line", "flags": 0, "points": [[(135, 524)]]},
                {"type": "line", "flags": 0, "points": [[(237, 496)]]},
                {"type": "line", "flags": 0, "points": [[(237, 468)]]},
                {"type": "line", "flags": 0, "points": [[(135, 440)]]},
                {"type": "line", "flags": 0, "points": [[(48, 440)]]},
                {"type": "move", "flags": 0, "points": [[(233, 661)]]},
                {"type": "line", "flags": 0, "points": [[(233, 748)]]},
                {"type": "line", "flags": 0, "points": [[(318, 748)]]},
                {"type": "line", "flags": 0, "points": [[(318, 661)]]},
                {"type": "line", "flags": 0, "points": [[(292, 519)]]},
                {"type": "line", "flags": 0, "points": [[(259, 519)]]},
                {"type": "move", "flags": 0, "points": [[(314, 468)]]},
                {"type": "line", "flags": 0, "points": [[(314, 496)]]},
                {"type": "line", "flags": 0, "points": [[(416, 524)]]},
                {"type": "line", "flags": 0, "points": [[(503, 524)]]},
                {"type": "line", "flags": 0, "points": [[(503, 440)]]},
                {"type": "line", "flags": 0, "points": [[(416, 440)]]},
            ],
            "metrics": [(551, 0)],
            "hints": {
                "v": [[{"pos": 233, "width": 85}]],
                "h": [
                    [{"pos": 748, "width": -20}],
                    [{"pos": -179, "width": -21}],
                    [{"pos": 440, "width": 84}],
                ],
            },
            "guides": {"h": [], "v": []},
            "tth": [
                {"cmd": "AlignTop", "params": {"pt": 15, "zone": 3}},
                {"cmd": "AlignBottom", "params": {"pt": 7, "zone": 1}},
                {"cmd": "DoubleLinkV", "params": {"pt1": 8, "pt2": 13, "stem": -1}},
                {
                    "cmd": "SingleLinkV",
                    "params": {"pt1": 8, "pt2": 22, "stem": -1, "align": -1},
                },
                {
                    "cmd": "SingleLinkV",
                    "params": {"pt1": 13, "pt2": 25, "stem": -1, "align": -1},
                },
            ],
        }
        result = GlyphParser().parse_hex(data)
        assert result == expected
