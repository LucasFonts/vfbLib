from datetime import UTC, datetime
from unittest import TestCase

from vfbLib.ufo.time import convert_timestamp, datetime_to_fl


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

    def test_flip_0(self):
        ts = 2147483647
        d = convert_timestamp(ts)
        assert fmt(d) == "1972/01/19 04:14:07"

    def test_flip_1(self):
        ts = -2147483648
        d = convert_timestamp(ts)
        assert fmt(d) == "1972/01/19 04:14:08"

    def test_dst(self):
        ts = -991664896
        d = convert_timestamp(ts)
        assert fmt(d) == "2008/09/03 17:00:00"

    def test_now_dst(self):
        ts = -434743306  # now
        d = convert_timestamp(ts)
        assert fmt(d) == "2026/04/28 13:26:30"

    def test_datetime_to_fl_negative(self):
        d = datetime(1969, 1, 1, 0, 0, 0, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == 2082841200

    def test_datetime_to_fl_origin(self):
        d = datetime(1970, 1, 1, 0, 0, 0, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == 2082841200

    def test_datetime_to_fl_flip_0(self):
        d = datetime(1972, 1, 19, 4, 14, 7, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == 2147483647  # max i32

    def test_datetime_to_fl_flip_1(self):
        d = datetime(1972, 1, 19, 4, 14, 8, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == -2147483648  # min i32

    def test_datetime_to_fl_dst(self):
        d = datetime(2008, 9, 3, 17, 0, 0, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == -991664896

    def test_datetime_to_fl_now_dst(self):
        d = datetime(2026, 4, 28, 13, 26, 30, tzinfo=UTC)
        ts = datetime_to_fl(d)
        assert ts == -434743306
