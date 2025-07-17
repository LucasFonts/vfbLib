# from fontTools.misc.textTools import deHexStr, hexStr
# from io import BytesIO
from unittest import TestCase

from pytest import raises

from vfbLib.compilers.base import StreamWriter


class StreamWriterTest(TestCase):
    # uint8

    def test_write_uint8_0(self):
        s = StreamWriter()
        s.write_uint8(0)
        assert s.stream.getvalue() == b"\00"

    def test_write_uint8_128(self):
        s = StreamWriter()
        s.write_uint8(128)
        assert s.stream.getvalue() == b"\x80"

    def test_write_uint8_max(self):
        s = StreamWriter()
        s.write_uint8(255)
        assert s.stream.getvalue() == b"\xff"

    def test_write_uint8_negative(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint8(-1)

    def test_write_uint8_large(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint8(256)

    # uint16

    def test_write_uint16_0(self):
        s = StreamWriter()
        s.write_uint16(0)
        assert s.stream.getvalue() == b"\x00\x00"

    def test_write_uint16_128(self):
        s = StreamWriter()
        s.write_uint16(128)
        assert s.stream.getvalue() == b"\x80\x00"  # LE

    def test_write_uint16_max(self):
        s = StreamWriter()
        s.write_uint16(65535)
        assert s.stream.getvalue() == b"\xff\xff"

    def test_write_uint16_negative(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint16(-1)

    def test_write_uint16_large(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint16(65536)

    # int16 (signed)

    def test_write_int16_0(self):
        s = StreamWriter()
        s.write_int16(0)
        assert s.stream.getvalue() == b"\x00\x00"

    def test_write_int16_128(self):
        s = StreamWriter()
        s.write_int16(128)
        assert s.stream.getvalue() == b"\x80\x00"  # LE

    def test_write_int16_max(self):
        s = StreamWriter()
        s.write_int16(32767)
        assert s.stream.getvalue() == b"\xff\x7f"

    def test_write_int16_negative(self):
        s = StreamWriter()
        s.write_int16(-1)
        assert s.stream.getvalue() == b"\xff\xff"

    def test_write_int16_negative_max(self):
        s = StreamWriter()
        s.write_int16(-32767)
        assert s.stream.getvalue() == b"\x01\x80"

    def test_write_int16_large(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_int16(32768)

    def test_write_int16_large_negative(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_int16(-32769)

    # int32 (signed)

    def test_write_int32_0(self):
        s = StreamWriter()
        s.write_int32(0)
        assert s.stream.getvalue() == b"\x00\x00\x00\x00"

    def test_write_int32_128(self):
        s = StreamWriter()
        s.write_int32(128)
        assert s.stream.getvalue() == b"\x80\x00\x00\x00"  # LE

    def test_write_int32_max(self):
        s = StreamWriter()
        s.write_int32(2147483647)
        assert s.stream.getvalue() == b"\xff\xff\xff\x7f"

    def test_write_int32_negative(self):
        s = StreamWriter()
        s.write_int32(-1)
        assert s.stream.getvalue() == b"\xff\xff\xff\xff"

    def test_write_int32_negative_max(self):
        s = StreamWriter()
        s.write_int32(-2147483648)
        assert s.stream.getvalue() == b"\x00\x00\x00\x80"

    def test_write_int32_large(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_int32(2147483648)

    def test_write_int32_large_negative(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_int32(-2147483649)
