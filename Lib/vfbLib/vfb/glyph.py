from __future__ import annotations

import logging

from fontTools.pens.pointPen import PointToSegmentPen
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from fontTools.pens.pointPen import AbstractPointPen
    from vfbLib.vfb.entry import VfbEntry

logger = logging.getLogger(__name__)


class VfbGlyph:
    def __init__(self, entry: VfbEntry) -> None:
        self.entry = entry
        self._target_master = 0

    def decompile(self) -> str:
        """
        Decompile the Glyph entry and return the glyph name.
        """
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

    def draw(self, pen) -> None:
        """
        Draw the VFB glyph onto a segment pen.
        """
        sp = PointToSegmentPen(pen, outputImpliedClosingLine=False)
        self.drawPoints(sp)

    def drawPoints(self, pen: AbstractPointPen) -> None:
        """
        Draw the VFB glyph onto a point pen.
        """
        if self.entry.decompiled is None:
            raise ValueError

        in_path = False
        in_qcurve = False
        path_is_open = False
        if "nodes" in self.entry.decompiled:
            for n in self.entry.decompiled["nodes"]:
                nodes = n["points"][self._target_master]
                pt = nodes[0]
                segment_type = n["type"]
                flags = n["flags"]
                smooth = bool(flags & 1)

                if segment_type == "move":
                    path_is_open = bool(flags & 8)
                    if in_path:
                        pen.endPath()
                    pen.beginPath()
                    in_path = True
                    if path_is_open:
                        pen.addPoint(pt, "move", smooth=smooth)
                    else:
                        pen.addPoint(pt, "line", smooth=smooth)  # FIXME

                elif segment_type == "line":
                    if in_qcurve:
                        st = "qcurve"
                        in_qcurve = False
                    else:
                        st = segment_type
                    pen.addPoint(pt, st, smooth=smooth)

                elif segment_type == "curve":
                    # Reorder the curve points
                    pt, c1, c2 = nodes
                    pen.addPoint(c1)
                    pen.addPoint(c2)
                    pen.addPoint(pt, "curve")

                elif segment_type == "qcurve":
                    pen.addPoint(pt)
                    in_qcurve = True

            if in_path:
                pen.endPath()

    def getPen(self) -> None:
        """
        Get a segment pen to draw into the VFB glyph.
        """
        raise NotImplementedError

    def getPointPen(self) -> None:
        """
        Get a point pen to draw into the VFB glyph.
        """
        raise NotImplementedError
