from unittest import TestCase

from vfbLib.ufo.time import convert_timestamp


def fmt(d):
    return d.strftime("%Y/%m/%d %H:%M:%S")


class TestConvertTimestamp(TestCase):
    def test_negative(self):
        ts = 2082841199  # -1
        d = convert_timestamp(ts)
        assert fmt(d) == "1970/01/01 00:00:00"

    def test_origin(self):
        ts = 2082841200  # 01.01.1970, 00:00:00 UTC
        d = convert_timestamp(ts)
        assert fmt(d) == "1970/01/01 00:00:00"

    def test_summertime(self):
        ts = 3303309600
        d = convert_timestamp(ts)
        assert fmt(d) == "2008/09/03 19:00:00"

    def test_now(self):
        ts = 3754301757  # now
        d = convert_timestamp(ts)
        assert fmt(d) == "2022/12/19 14:35:57"
