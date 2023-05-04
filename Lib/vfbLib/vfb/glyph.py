from __future__ import annotations

import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vfbLib.vfb.entry import VfbEntry

logger = logging.getLogger(__name__)


class VfbGlyph:
    def __init__(self, entry: VfbEntry) -> None:
        self.entry = entry
        self._target_master = 0

    def decompile(self) -> str:
        self.entry.decompile()
        if self.entry.decompiled is None:
            raise ValueError

        return self.entry.decompiled["name"]

    @property
    def target_master(self) -> int:
        """
        Set the target master index before calling draw/pen methods to select the
        desired master.
        """
        return self._target_master

    @target_master.setter
    def target_master(self, value: int) -> None:
        self._target_master = value

    def draw(self, pen, glyph_set=None) -> None:
        """
        Draw the VFB glyph onto a segment pen.
        """
        raise NotImplementedError

    def drawPoints(self, pen, glyph_set=None) -> None:
        """
        Draw the VFB glyph onto a point pen.
        """
        raise NotImplementedError

    def getPen(self):
        """
        Get a segment pen to draw into the VFB glyph.
        """
        raise NotImplementedError

    def getPointPen(self):
        """
        Get a point pen to draw into the VFB glyph.
        """
        raise NotImplementedError
