from unittest import TestCase

from vfbLib.parsers.pclt import PcltParser


class EncodedValueListParserTest(TestCase):
    def test_pclt_empty(self):
        data = (
            "8b8b8b8b8b8b8b"
            "00000000000000"
            "00000000000000"
            "00000000000000"
            "00000000000000"
            "0000000000"
        )

        expected = {
            "font_number": 0,
            "pitch": 0,
            "x_height": 0,
            "style": 0,
            "type_family": 0,
            "cap_height": 0,
            "symbol_set": 0,
            "typeface": (
                "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            ),
            "character_complement": [
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
            "file_name": "\x00\x00\x00\x00\x00\x00",
            "stroke_weight": 0,
            "width_type": 0,
            "serif_style": 0,
        }
        result = PcltParser().parse_hex(data)
        assert result == expected

    def test_pclt(self):
        data = (
            "ffcd000003c2f88ad4ff00004002f952a4"
            "534d4820202020202020202020202020"
            "1a34567809123400"
            "544e5252300002fe82"
        )
        expected = {
            "font_number": 3439329283,
            "pitch": 55,
            "x_height": 502,
            "style": 73,
            "type_family": 16386,
            "cap_height": 702,
            "symbol_set": 25,
            "typeface": "SMH             ",
            "character_complement": [
                0x1A,
                0x34,
                0x56,
                0x78,
                0x09,
                0x12,
                0x34,
                0x00,
            ],
            "file_name": "TNRR0\x00",
            "stroke_weight": 2,
            "width_type": -2,
            "serif_style": 130,
        }
        result = PcltParser().parse_hex(data)
        assert result == expected
