from pathlib import Path
from unittest import TestCase

from fontTools.designspaceLib import DesignSpaceDocument

from vfbLib.ufo.builder import VfbToUfoBuilder
from vfbLib.vfb.vfb import Vfb


def data_path():
    return Path(__file__).parent / "Data"


def vfb_path(name: str) -> Path:
    return data_path() / name


class GlyphCompilerTest(TestCase):
    def test_vfb_to_ufo_mm(self):
        vfb = Vfb(vfb_path("masters.vfb"))
        vfb.decompile()
        builder = VfbToUfoBuilder(vfb, move_groups=False)
        ufos, designspace = builder.get_ufos_designspace(data_path())
        assert len(ufos) == 4
        assert isinstance(designspace, DesignSpaceDocument)

        # Master 0
        ufo = ufos[0]
        assert len(ufo) == 2  # 1 glyph only
        glyph = ufo["a"]
        assert len(glyph) == 1
        assert glyph.width == 353
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (176, 181)

        # Master 1
        ufo = ufos[1]
        glyph = ufo["a"]
        assert glyph.width == 457
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (228, 161)

        # Master 2
        ufo = ufos[2]
        glyph = ufo["a"]
        assert glyph.width == 437
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (218, 181)

        # Master 3
        ufo = ufos[3]
        glyph = ufo["a"]
        assert glyph.width == 565
        point = glyph.contours[0].points[3]
        assert (point.x, point.y) == (281, 151)

    def test_vfb_to_ufo_mm_reader_deepcopy(self):
        # Check that objects have been copied and are not shared anymore between UFOs
        vfb = Vfb(vfb_path("masters.vfb"))
        vfb.decompile()
        builder = VfbToUfoBuilder(vfb, move_groups=False)
        ufos = builder.get_ufo_masters(silent=True)
        assert len(ufos) == 4

        ufo0, ufo1, _, _ = ufos

        # Features

        fea0 = (
            "\n\nlanguagesystem DFLT dflt;\nfeature kern {\n  pos a t 100 ;\n} kern;\n"
        )

        assert ufo0.features.text == fea0
        assert ufo1.features.text == fea0

        # Glyphs

        glyph0 = ufo0["a"]
        assert glyph0.width == 353
        glyph0.width = 354
        point = glyph0.contours[0].points[3]
        assert (point.x, point.y) == (176, 181)
        point.x = 200
        glyph0.lib["foo"] = "bar"
        assert glyph0.unicode == 0x61
        glyph0.unicodes.append(0x41)

        # Master 1
        glyph1 = ufo1["a"]
        assert glyph1.width == 457
        point = glyph1.contours[0].points[3]
        assert (point.x, point.y) == (228, 161)
        assert "foo" not in glyph1.lib
        assert glyph1.unicodes == [0x61]

        # Groups

        expected_group_order = [
            "public.kern1._a_LEFT",
            "public.kern2._a_RIGHT",
            "public.kern1._t",
            "public.kern2._t",
            # "_empty",
            ".mtrx5",
            "letters",
        ]

        expected_groups = dict(
            zip(
                expected_group_order,
                [
                    ["a"],
                    ["a"],
                    ["t"],
                    ["t"],
                    # [],
                    ["a"],
                    ["a", "t"],
                ],
            )
        )

        assert ufo0.groups == expected_groups
        assert ufo0.groups == ufo1.groups
        del ufo1.groups[".mtrx5"]
        assert ".mtrx5" in ufo0.groups
        ufo0.groups["_empty"] = ["a"]
        assert "_empty" not in ufo1.groups

        # Kerning

        ufo0.kerning[("public.kern1._a_LEFT", "public.kern2._a_RIGHT")] = -10
        assert ("public.kern1._a_LEFT", "public.kern2._a_RIGHT") not in ufo1.kerning
        assert ufo0.kerning[("public.kern1._a_LEFT", "public.kern2._t")] == -73
        ufo0.kerning[("public.kern1._a_LEFT", "public.kern2._t")] = -72
        assert ufo0.kerning[("public.kern1._a_LEFT", "public.kern2._t")] == -72
        assert ufo1.kerning[("public.kern1._a_LEFT", "public.kern2._t")] == -166

        # Lib

        assert ufo0.lib["public.groupOrder"] == expected_group_order
        assert "com.lucasfonts.vfblib" in ufo0.lib["com.fontlab.v5.userData"]
        del ufo0.lib["com.fontlab.v5.userData"]
        assert "com.lucasfonts.vfblib" in ufo1.lib["com.fontlab.v5.userData"]
        ufo0.lib["foo"] = "bar"
        assert "foo" not in ufo1.lib
