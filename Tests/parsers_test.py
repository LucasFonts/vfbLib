from fontTools.misc.textTools import deHexStr
from unittest import TestCase

from vfbLib.parsers import EncodedValueParser


class EncodedValueParserTest(TestCase):
    def expect(self, encoded, decoded):
        assert EncodedValueParser.parse(deHexStr(encoded)) == decoded

    def test_links_1(self):
        self.expect("8c8d898b", [1, 2, -2, 0])
