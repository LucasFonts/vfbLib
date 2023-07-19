from __future__ import annotations

import logging

from fontTools.pens.pointPen import (
    AbstractPointPen,
    PointToSegmentPen,
    SegmentToPointPen,
)
from typing import TYPE_CHECKING, Any, Dict, List, Tuple
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.paths import UfoMasterGlyph
from vfbLib.templates.glyph import get_empty_glyph

if TYPE_CHECKING:
    from fontTools.pens.basePen import AbstractPen
    from vfbLib.vfb.vfb import Vfb, VfbMaster
    from vfbLib.vfb.entry import VfbEntry

logger = logging.getLogger(__name__)


class VfbGlyph:
    def __init__(self, entry: VfbEntry, parent: Vfb | VfbMaster) -> None:
        self.entry = entry
        self._parent = parent
        self._glyph: UfoMasterGlyph | None = None

    # UFO/cu2qu compatibility

    def clearContours(self):
        try:
            del self.entry.decompiled["hints"]
        except KeyError:
            pass
        self.entry.decompiled["nodes"] = []
        self.entry.decompiled["num_node_values"] = 0
        self.entry.modified = True

    # Native methods

    def decompile(self) -> str:
        """
        Decompile the Glyph entry and return the glyph name.
        """
        self.entry.decompile()
        if self.entry.decompiled is None:
            raise ValueError

        return self.entry.decompiled["name"]

    def empty(self):
        self.entry.decompiled = get_empty_glyph(self._parent.num_masters)

    def _copy_to_ufo_glyph(self):
        """
        Copy minimal data to the VfbToUfoGlyph. Only data that is necessary for the pen
        methods is copied.
        """
        if self.entry.decompiled is None:
            raise ValueError

        _mm_glyph = VfbToUfoGlyph()
        _mm_glyph.name = self.entry.decompiled["name"]

        if "components" in self.entry.decompiled:
            _mm_glyph.mm_components = self.entry.decompiled["components"]

        if "metrics" in self.entry.decompiled:
            _mm_glyph.mm_metrics = self.entry.decompiled["metrics"]

        if "nodes" in self.entry.decompiled:
            _mm_glyph.mm_nodes = self.entry.decompiled["nodes"]

        # TODO: Support point names used by TT hinting
        # if "tth" in self.entry.decompiled:
        #     _mm_glyph.tth_commands = self.entry.decompiled["tth"]

        self._glyph = UfoMasterGlyph(
            mm_glyph=_mm_glyph,
            glyph_order=self._parent.glyph_order,
            master_index=self._parent.master_index,
        )
        self._glyph.build()

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

        if self._glyph is None:
            self._copy_to_ufo_glyph()

        if self._glyph is None:
            raise ValueError

        return self._glyph.drawPoints(pen)

    def getPen(self) -> AbstractPen:
        """
        Return a segment pen to draw into the VFB glyph.
        """
        # TODO: Test
        return SegmentToPointPen(self.getPointPen(), guessSmooth=True)

    def getPointPen(self) -> VfbGlyphPointPen:
        """
        Return a point pen to draw into the VFB glyph.
        """
        if self.entry.decompiled is None:
            if self.entry.data is None:
                # Make an empty glyph
                self.empty(self._parent.num_masters)
            else:
                self.decompile()
        return VfbGlyphPointPen(self, self._parent)


class VfbGlyphPointPen(AbstractPointPen):
    # FIXME: Only supports TrueType curves
    def __init__(self, glyph: VfbGlyph, glyphSet: Vfb | VfbMaster) -> None:
        """A PointPen to draw into the VFB glyph.

        Args:
            glyph (VfbGlyph): The glyph to draw into.
        """
        self.glyph = glyph
        self.glyphSet = glyphSet
        self.currentPath = None
        self.in_qcurve = False
        if self.glyphSet.master_index == 0:
            self.target = self.glyph.entry.decompiled
        else:
            if self.glyph.entry.temp_masters is None:
                self.glyph.entry.temp_masters = [[] * self.glyphSet.num_masters]
            self.target = self.glyph.entry.temp_masters[self.glyphSet.master_index]

    def beginPath(self) -> None:
        self.currentPath = []

    def endPath(self) -> None:
        self.target["nodes"].extend(self.currentPath)
        self.currentPath = None

    def addPoint(
        self,
        pt: Tuple[int, int],
        segmentType: str | None = None,
        smooth: bool = False,
        name: str | None = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        assert self.currentPath is not None

        flags = 0
        x, y = pt
        node = {
            "type": None,
            "flags": flags,
            "points": [
                [(round(x), round(y))] for _ in range(self.glyphSet.num_masters)
            ],
        }

        if segmentType == "qcurve":
            self.in_qcurve = True

        if not self.currentPath:
            # Begin a new path

            if segmentType == "move":  # Open path
                flags += 8

            # VFB first node always has type "move"
            node["type"] = "move"

        else:
            # During path
            if segmentType is None:
                node["type"] = "qcurve"
            elif segmentType == "qcurve":
                if self.in_qcurve:
                    node["type"] = "line"
                    self.in_qcurve = False
            elif segmentType == "line":
                node["type"] = "line"
            else:
                print(f"Unsupported segment type: {segmentType}")
                raise ValueError

        node["flags"] = flags
        self.currentPath.append(node)

    def addComponent(
        self,
        baseGlyphName: str,
        transformation: Tuple[float, float, float, float, float, float],
        identifier: str | None = None,
        **kwargs: Any,
    ) -> None:
        assert self.currentPath is None
        base_index = self.glyphSet.glyph_order.index(baseGlyphName)
        if base_index == -1:
            raise (KeyError, f"Base glyph not found: '{baseGlyphName}'")

        xx, xy, yx, yy, dx, dy = transformation

        if not "components" in self.target:
            self.target["components"] = []
        self.target["components"].append(
            {
                "gid": base_index,
                "offsetX": [dx] * self.glyphSet.num_masters,
                "offsetY": [dy] * self.glyphSet.num_masters,
                "scaleX": [xx] * self.glyphSet.num_masters,
                "scaleY": [yy] * self.glyphSet.num_masters,
            }
        )
