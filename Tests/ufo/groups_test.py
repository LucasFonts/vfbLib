from unittest import TestCase

from vfbLib.ufo.groups import transform_groups

FIRST = 2**10
SECOND = 2**11


class GroupsTest(TestCase):
    def test_kerning(self) -> None:
        orig_groups = {
            "_E1": ["Eacute", "E'", "AE"],
            "_E2": ["B", "D", "E'", "F", "H", "K", "L", "M", "N", "P", "R"],
            "_A": ["Aacute", "A'", "Adieresis"],
            "_F_whatever": ["F'"],
        }
        kerning_class_flags = {
            "_A": (FIRST + SECOND, 0),
            "_E1": (FIRST, 0),
            "_E2": (SECOND, 0),
        }
        glyph_order = [
            "A",
            "B",
            "D",
            "E",
            "F",
            "H",
            "K",
            "L",
            "M",
            "N",
            "P",
            "R",
            "Aacute",
            "Adieresis",
            "AE",
        ]
        ufo_groups, group_order, key_glyphs = transform_groups(
            orig_groups,
            kerning_class_flags,
            glyph_order,
            skip_missing_group_glyphs=True,
        )
        assert ufo_groups == {
            "public.kern1._A": ["A", "Aacute", "Adieresis"],
            "public.kern1._E1": ["E", "AE"],  # Eacute is dropped because not in GO
            "public.kern2._A": ["A", "Aacute", "Adieresis"],
            "public.kern2._E2": [
                "E",
                "B",
                "D",
                "F",
                "H",
                "K",
                "L",
                "M",
                "N",
                "P",
                "R",
            ],
        }
        assert group_order == [
            "public.kern1._E1",
            "public.kern2._E2",
            "public.kern1._A",
            "public.kern2._A",
        ]
        assert key_glyphs == {
            "public.kern1._A": "A",
            "public.kern1._E1": "E",
            "public.kern2._A": "A",
            "public.kern2._E2": "E",
        }

    def test_other(self) -> None:
        orig_groups = {
            ".A": ["Aacute", "A", "Adieresis"],
        }
        glyph_order = ["A", "Aacute", "Adieresis"]
        ufo_groups, group_order, key_glyphs = transform_groups(
            orig_groups,
            kerning_class_flags={},
            glyphOrder=glyph_order,
            skip_missing_group_glyphs=False,
        )
        assert ufo_groups == {
            ".A": ["Aacute", "A", "Adieresis"],
        }
        assert group_order == [
            ".A",
        ]
        assert key_glyphs == {}

    def test_other_with_key_glyph(self) -> None:
        orig_groups = {
            ".A": ["Aacute", "A'", "Adieresis"],
        }
        glyph_order = ["A", "Aacute", "Adieresis"]
        ufo_groups, group_order, key_glyphs = transform_groups(
            orig_groups,
            kerning_class_flags={},
            glyphOrder=glyph_order,
            skip_missing_group_glyphs=False,
        )
        assert ufo_groups == {
            # Key glyph is first now
            ".A": ["A", "Aacute", "Adieresis"],
        }
        assert group_order == [
            ".A",
        ]
        assert key_glyphs == {
            ".A": "A",
        }
