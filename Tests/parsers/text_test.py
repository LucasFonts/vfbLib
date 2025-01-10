from unittest import TestCase
from vfbLib.parsers.text import (
    NameRecordsParser,
    OpenTypeStringParser,
    StringParser,
)


class StringParserTest(TestCase):
    def test_links_1(self):
        data = "57 74 30 20 57 64 31 20"
        expected = "Wt0 Wd1"  # Trailing space gets stripped
        result = StringParser().parse_hex(data)
        assert result == expected
