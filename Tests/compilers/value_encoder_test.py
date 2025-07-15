from io import BytesIO
from unittest import TestCase

from fontTools.misc.textTools import hexStr

from vfbLib.compilers.value import write_value, write_value_long


class ValueEncoderTest(TestCase):
    def expect(self, encoded, decoded, signed=True):
        data = BytesIO()
        write_value(decoded, data, signed)
        assert hexStr(data.getvalue()) == encoded

    def expect_unoptimized(self, encoded, decoded, signed=True):
        data = BytesIO()
        write_value_long(decoded, data, signed)
        assert hexStr(data.getvalue()) == encoded

    def test_0x20(self):
        self.expect("20", -107)

    def test_0x8b(self):
        self.expect("8b", 0)

    def test_0xf6(self):
        self.expect("f6", 107)

    def test_0xf700(self):
        self.expect("f700", 108)

    def test_0xf701(self):
        self.expect("f701", 109)

    def test_0xf7ff(self):
        self.expect("f7ff", 363)

    def test_0xf800(self):
        self.expect("f800", 364)

    def test_0xf801(self):
        self.expect("f801", 365)

    def test_0xfa00(self):
        self.expect("fa00", 876)

    def test_0xfaff(self):
        self.expect("faff", 1131)

    def test_0xfb00(self):
        # 64256
        self.expect("fb00", -108)

    def test_0xfb01(self):
        self.expect("fb01", -109)

    def test_0xfe00(self):
        self.expect("fe00", -876)

    def test_0xfeff(self):
        self.expect("feff", -1131)

    def test_0xff00000000(self):
        self.expect_unoptimized("ff00000000", 0)

    def test_0xff00001000(self):
        self.expect("ff00001000", 4096)

    def test_0xff00001000u(self):
        self.expect("ff00001000", 4096, False)

    def test_0xffffffffff(self):
        self.expect_unoptimized("ffffffffff", -1)

    def test_0xffffffffffu(self):
        # 4294967295 (max)
        self.expect("ffffffffff", 0xFFFFFFFF, False)

    def test_0xffffffefff(self):
        self.expect("ffffffefff", -4097)

    def test_0xffffffefffu(self):
        # 4294963199
        self.expect("ffffffefff", 0xFFFFEFFF, False)
