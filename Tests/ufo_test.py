from __future__ import annotations

import pytest

from fontTools.designspaceLib import DesignSpaceDocument
from pathlib import Path
from unittest import TestCase
from vfbLib.reader import VFBReader
from vfbLib.ufo import VfbToUfoBuilder


def data_path():
    return Path(__file__).parent / "Data"


def vfb_path(name: str) -> Path:
    return data_path() / name


class GlyphCompilerTest(TestCase):
    def test_vfb_to_ufo_mm_reader(self):
        reader = VFBReader(vfb_path("masters.vfb"))
        reader.read()
        builder = VfbToUfoBuilder(reader.data)
        ufos, designspace = builder.get_ufos_designspace(data_path())
        assert len(ufos) == 4
        assert isinstance(designspace, DesignSpaceDocument)

        # Master 0
        ufo = ufos[0]
        assert len(ufo) == 1  # 1 glyph only
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
