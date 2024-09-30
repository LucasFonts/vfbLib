from unittest import TestCase

from vfbLib.ufo.kerning import UfoKerning

glyph_order = ["A", "Adieresis", "E", "F", "T", "Tbar", "Y"]

groups = {
    "public.kern1.A": ["A", "Adieresis"],
    "public.kern2.A": ["A", "Adieresis"],
    "public.kern1.T": ["T", "Y"],
    "public.kern2.T": ["T", "Y", "Tbar"],
    "public.kern1.F": ["F", "Tbar"],
    "public.kern2.E": ["E", "F"],
}

mmk = {}

kg = {
    "public.kern1.A": "A",
    "public.kern2.A": "A",
    "public.kern1.T": "T",
    "public.kern2.T": "T",
    "public.kern1.F": "F",
    "public.kern2.E": "E",
}

kerning = UfoKerning(
    glyph_order=glyph_order, groups=groups, mm_kerning=mmk, key_glyphs=kg
)
kerning.mm_kerning_names = {
    ("public.kern1.A", "public.kern2.T"): [-100, -80],
    ("public.kern1.T", "public.kern2.A"): [-100, -80],
    ("Adieresis", "public.kern2.T"): [-80, -60],
    ("public.kern1.T", "Adieresis"): [-80, -60],
    ("public.kern1.F", "public.kern2.A"): [-70, -65],
    ("Tbar", "Adieresis"): [-60, -55],
    ("P", "A"): [-90, -85],
    ("P", "J"): [-90, -85],
}


class UfoKerningTest(TestCase):
    def test_exception_keypair(self):
        assert not kerning._is_exception("A", "T")

    def test_exception_key_member(self):
        assert kerning._is_exception("T", "Adieresis")

    def test_exception_member_key(self):
        assert kerning._is_exception("Adieresis", "T")

    def test_exception_member_member(self):
        assert kerning._is_exception("Tbar", "Adieresis")

    def test_exception_nonmember_key(self):
        assert not kerning._is_exception("P", "A")

    def test_exception_key_nonmember(self):
        assert not kerning._is_exception("T", "J")

    def test_exception_nonmember_member(self):
        assert kerning._is_exception("Ydieresis", "Adieresis")

    def test_exception_member_nonmember(self):
        assert kerning._is_exception("Adieresis", "Ydieresis")

    def test_exception_nonmember_nonmember(self):
        assert not kerning._is_exception("P", "J")

    def test_exception_unkerned(self):
        assert not kerning._is_exception("X", "hyphen")
