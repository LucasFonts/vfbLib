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
    from vfbLib.vfb import Vfb
    from vfbLib.vfb.entry import VfbEntry

logger = logging.getLogger(__name__)


class VfbGlyph:
    def __init__(self, entry: VfbEntry, parent: Vfb) -> None:
        self.entry = entry
        self._parent = parent
        self._glyph: UfoMasterGlyph | None = None
        self._target_master = 0

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

    def empty(self, num_masters: int = 1):
        self.entry.decompiled = get_empty_glyph(num_masters)

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
            master_index=self._target_master,
        )
        self._glyph.build()

    @property
    def target_master(self) -> int:
        """
        Set the target master index before calling draw/pen methods to select the
        desired master.
        """
        if self._glyph is None:
            return self._target_master

        return self._glyph.master_index

    @target_master.setter
    def target_master(self, value: int) -> None:
        self._target_master = value
        if self._glyph is not None:
            self._glyph.master_index = value

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
        return VfbGlyphPointPen(self)

    def getPointPenMM(self) -> VfbGlyphPointPenMM:
        """
        Return a MM-capable point pen to draw into the VFB glyph.
        """
        return VfbGlyphPointPenMM(self)


class VfbGlyphPointPen(AbstractPointPen):
    # FIXME: Only supports TrueType curves
    def __init__(self, glyph: VfbGlyph) -> None:
        self.glyph = glyph
        self.currentPath = None
        self.in_qcurve = False
        self.last_type = None

    def beginPath(self) -> None:
        self.currentPath = []

    def endPath(self) -> None:
        self.glyph.entry.decompiled["nodes"].extend(self.currentPath)
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
            "points": [[(round(x), round(y))]],
        }

        if segmentType == "qcurve":
            self.in_qcurve = True

        if not self.currentPath:
            # Begin a new path

            if segmentType == "move":  # Open path
                flags += 8

            # VFB first node always has type "move", save real type for later
            node["type"] = "move"
            self.last_type = segmentType

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

    # def addComponent(self, baseName, transformation):
    #     assert self.currentPath is None
    #     # make base glyph if needed, Component() needs the index
    #     NewGlyph(self.glyph.parent, baseName, updateFont=False)
    #     baseIndex = self.glyph.parent.FindGlyph(baseName)
    #     if baseIndex == -1:
    #         raise (KeyError, "couldn't find or make base glyph")
    #     xx, xy, yx, yy, dx, dy = transformation
    #     # XXX warn when xy or yx != 0
    #     new = Component(baseIndex, Point(dx, dy), Point(xx, yy))
    #     self.glyph.components.append(new)


class VfbGlyphPointPenMM(VfbGlyphPointPen):
    def addPoint(
        self,
        pts: List[Tuple[int, int]],
        segmentType: str | None = None,
        smooth: bool = False,
        name: str | None = None,
        **kwargs: Dict[str, Any],
    ) -> None:
        assert self.currentPath is not None
        self.currentPath.append((pts, segmentType, smooth, name))

    # def addComponent(self, baseName, transformation):
    #     assert self.currentPath is None
    #     # make base glyph if needed, Component() needs the index
    #     NewGlyph(self.glyph.parent, baseName, updateFont=False)
    #     baseIndex = self.glyph.parent.FindGlyph(baseName)
    #     if baseIndex == -1:
    #         raise (KeyError, "couldn't find or make base glyph")
    #     xx, xy, yx, yy, dx, dy = transformation
    #     # XXX warn when xy or yx != 0
    #     new = Component(baseIndex, Point(dx, dy), Point(xx, yy))
    #     self.glyph.components.append(new)
