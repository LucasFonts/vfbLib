from io import BytesIO
from pprint import pprint
from sys import argv

from fontTools.misc.textTools import deHexStr, hexStr

from vfbLib.parsers import EncodedValueParser, MetricsParser
from vfbLib.parsers.glyph import GlyphParser
from vfbLib.parsers.mm import PrimaryInstancesParser


def decode_data(data):
    result = EncodedValueParser.parse(BytesIO(data), len(data))
    print(result)


def decode_glyph():
    data = deHexStr(
        "01090701019041452e7363088df77aa200f7b38bf7ef8b018bf71a8bd201fb538bfb1e8b0140fb1a6a4401528bfb548b01f7c0f89cf790f89c01f7c08bf86b8b018b618bfb2501fb738bfb478b018bfb508b6101f7608bf7378b018b618bfb1f01fb608bfb378b018bfb618b5c01f7738bf7478b018b608bfb2700fba9f86bfbfcf80b01898b878b048177837504735e7657017666817601fb05fb58643601f73e8bdd8b02f9128bf9888b038b8ba0018c028b018b018d028cff8c018e028b018b028cff8e018c028c018b028b018dffa0018e028b018b028c048cf80b8bf80b8b8c8b8b8b8b0af703a2078f8b038f99898a0d8b8f998b038f8e8b8a038b908a8a0d9c908b8a0d8d8e9c8a0d928f998b038b988b8a0398948a8a0d96998f8b0da09c8e8a038ba18a8a019092028b8c028e8c0e8c8b908b0490928b8a0e978b908b0497948b8a048b988b8a0e9c8b908a048ca18b8a8b8b8b0f"
    )
    print(data)
    result = GlyphParser.parse(data)
    pprint(result)


def decode_metrics():
    data = deHexStr(
        "33 8B 34 8B 35 8B 36 8B 37 8B 38 8B 39 8B 56 FF D2 1F 16 FF 57 8B 3E F9 50 3F 90 40 8B 4B 8B 4C 00 00 08 09 00 00 00 00 00 00 4D FF 00 00 06 68 4E FC 2E 4F F7 52 50 AB 51 FF 00 00 09 C8 52 FF 00 00 05 38 54 8B 8B 32"
    )
    result = MetricsParser.parse(BytesIO(data), len(data))
    pprint(result)


data = "".join(argv[1:])
decode_data(deHexStr(data))
# decode_metrics()
