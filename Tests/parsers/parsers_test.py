from __future__ import annotations

from fontTools.misc.textTools import deHexStr
from io import BytesIO
from unittest import TestCase
from vfbLib.parsers import EncodedValueListParser


class EncodedValueListParserTest(TestCase):
    def expect(self, encoded, decoded):
        data = deHexStr(encoded)
        assert EncodedValueListParser.parse(BytesIO(data), len(data)) == decoded

    def test_links_1(self):
        self.expect("8c8d898b", [1, 2, -2, 0])
