import struct

# from fontTools.misc.textTools import deHexStr, hexStr
# from io import BytesIO
from pytest import raises
from unittest import TestCase
from vfbLib.compilers.base import StreamWriter, BaseCompiler


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
        assert s.stream.getvalue() == b"\xFF"

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
        assert s.stream.getvalue() == b"\xFF\xFF"

    def test_write_uint16_negative(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint16(-1)

    def test_write_uint16_large(self):
        s = StreamWriter()
        with raises(OverflowError):
            s.write_uint16(65536)
