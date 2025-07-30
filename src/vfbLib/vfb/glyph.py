from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from fontTools.pens.pointPen import AbstractPointPen, SegmentToPointPen

from vfbLib import DIRECTIONS
from vfbLib.templates.glyph import get_empty_glyph
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.paths import UfoMasterGlyph
from vfbLib.ufo.pshints import normalize_hint_dict
from vfbLib.vfb.pens import VfbGlyphPointPen

if TYPE_CHECKING:
    from fontTools.pens.basePen import AbstractPen

    from vfbLib.typing import HintTuple
    from vfbLib.vfb.entry import VfbEntry
    from vfbLib.vfb.vfb import Vfb, VfbMaster


logger = logging.getLogger(__name__)


class VfbGlyph:
    def __init__(self, entry: VfbEntry, parent: Vfb | VfbMaster) -> None:
        self.entry = entry

        # Related entries that we need when generating fonts
        self.links_entry: VfbEntry | None = None
        self.ps_hinting_options: VfbEntry | None = None

        self._parent = parent
        self._glyph: UfoMasterGlyph | None = None
        self.master_index = 0
        self.empty()

    # UFO/cu2qu compatibility

    @cached_property
    def name(self) -> str | None:
        if self._glyph is None:
            return None

        return self._glyph.name

    def clearContours(self):
        try:
            del self.entry.data["hints"]
        except KeyError:
            pass
        self.entry.data["nodes"] = []

    # Native methods

    def decompile(self) -> str:
        """
        Decompile the Glyph entry and return the glyph name.
        """
        self.entry.decompile()
        if self.entry.data is None:
            raise ValueError

        return self.entry.data["name"]

    def empty(self) -> None:
        self.entry.data = get_empty_glyph(self._parent.num_masters)

    def _copy_to_ufo_glyph(self) -> None:
        """
        Copy minimal data to the VfbToUfoGlyph. Only data that is necessary for the pen
        methods is copied.
        """
        if self.entry.data is None:
            raise ValueError

        _mm_glyph = VfbToUfoGlyph()
        _mm_glyph.name = self.entry.data["name"]

        if "components" in self.entry.data:
            _mm_glyph.mm_components = self.entry.data["components"]

        if "metrics" in self.entry.data:
            _mm_glyph.mm_metrics = self.entry.data["metrics"]

        if "nodes" in self.entry.data:
            _mm_glyph.mm_nodes = self.entry.data["nodes"]

        # TODO: Support point names used by TT hinting
        # if "tth" in self.entry.data:
        #     _mm_glyph.tth_commands = self.entry.data["tth"]

        self._glyph = UfoMasterGlyph(
            mm_glyph=_mm_glyph,
            glyph_order=self._parent.glyph_order,
            master_index=self._parent.master_index,
        )
        self._glyph.build()

    def resolve_hint_sets(self) -> dict[int, list[HintTuple]]:
        hint_sets = {}
        hints = self.resolve_hints()
        hints_entry = self.entry.data.get("hints", {})
        hintmasks = hints_entry.get("hintmasks", [])
        if hintmasks:
            set_index = 0
            set_hints = []
            for kind, index in hintmasks:
                if kind == "r":
                    if set_hints:
                        if set_index in hint_sets:
                            logger.warning(f"Duplicate hint sets for node {set_index}")
                        hint_sets[set_index] = set_hints
                    set_index = index
                    set_hints = []
                else:
                    set_hints.append(hints[kind][index])
            if set_hints:
                # TODO: Filter out any consecutive identical hintmasks
                hint_sets[set_index] = set_hints
        else:
            # All in one hint set
            hint_sets[0] = hints["h"] + hints["v"]
        return hint_sets

    def resolve_hints(self) -> dict[str, list[HintTuple]]:
        hints: dict[str, list[HintTuple]] = {"h": [], "v": []}

        mm_hints = self.entry.data.get("hints", {"h": [], "v": []})

        # Hints
        for direction in DIRECTIONS:
            direction_hints = mm_hints[direction]
            for mm_hint in direction_hints:
                hint = mm_hint[self.master_index]
                hint = normalize_hint_dict(hint, f"{direction}stem")
                hints[direction].append(hint)

        # Links
        links = self.resolve_links()
        for direction in DIRECTIONS:
            hints[direction].extend(links[direction])

        return hints

    def resolve_links(self) -> dict[str, list[HintTuple]]:
        # Convert the links to hints

        hints = {"h": [], "v": []}

        if self.links_entry is None:
            return hints

        links = self.links_entry.data
        assert isinstance(links, dict)
        if not (links["x"] or links["y"]):
            return hints

        mm_nodes = self.entry.data.get("nodes", [])

        # Do the actual conversion
        for i, axis in enumerate("xy"):
            direction_links = links[axis]
            for link in direction_links:
                isrc, itgt = link  # indices of source and target node
                src = mm_nodes[isrc]
                src_pos = src["points"][self.master_index][0][i]
                pos = src_pos
                if itgt == -1:  # Bottom ghost
                    width = -21
                    pos = src_pos - width
                elif itgt == -2:  # Top ghost
                    width = -20
                else:
                    tgt = mm_nodes[itgt]
                    tgt_pos = tgt["points"][self.master_index][0][i]
                    width = tgt_pos - src_pos

                d = "v" if axis == "x" else "h"
                # Don't normalize those values, the above code already did that
                hint = (f"{d}stem", pos, width)
                hints[d].append(hint)
        return hints

    def draw(self, pen: AbstractPen) -> None:
        """
        Draw the VFB glyph onto a segment pen. Uses the object's `master_index` property
        to determine which master is drawn.
        """
        if self.entry.data is None:
            raise ValueError

        glyph = self.entry.data

        path_is_open = False
        in_path = False
        in_qcurve = False
        qcurve = []

        for n in glyph.get("nodes", []):
            node_type = n.get("type")
            flags = n.get("flags", 0)
            pt = n["points"][self.master_index][0]
            if node_type == "move":
                if in_qcurve:
                    qcurve.append(pt)
                    pen.qCurveTo(*qcurve)
                if in_path:
                    if path_is_open:
                        pen.endPath()
                    else:
                        pen.closePath()
                    in_path = False
                in_qcurve = False
                qcurve = []
                pen.moveTo(pt)
                in_path = True
                path_is_open = bool(flags & 8)

            elif node_type == "line":
                if in_qcurve:
                    qcurve.append(pt)
                    pen.qCurveTo(*qcurve)
                    in_qcurve = False
                    qcurve = []
                else:
                    pen.lineTo(pt)
            elif node_type == "curve":
                # FIXME: What about mixed curve/qcurve?
                pt, c1, c2 = n["points"][self.master_index]
                pen.curveTo(c1, c2, pt)
            elif node_type == "qcurve":
                if not in_qcurve:
                    in_qcurve = True
                qcurve.append(pt)
            else:
                raise ValueError(f"Unknown node type: '{node_type}'")
        if in_path:
            if path_is_open:
                pen.endPath()
            else:
                pen.closePath()

        for c in glyph.get("components", []):
            baseGlyphName = self._parent.glyph_order[c["gid"]]
            transformation = (
                c["scaleX"][self.master_index],
                0,
                0,
                c["scaleY"][self.master_index],
                c["offsetX"][self.master_index],
                c["offsetY"][self.master_index],
            )
            pen.addComponent(baseGlyphName, transformation)

    def drawPoints(self, pen: AbstractPointPen) -> None:
        """
        Draw the VFB glyph onto a point pen.
        """
        if self.entry.data is None:
            raise ValueError

        if self._glyph is None:
            self._copy_to_ufo_glyph()

        if self._glyph is None:
            raise ValueError

        return self._glyph.drawPoints(pen)

    def drawPointsDirect(self, pen: AbstractPointPen) -> None:
        """
        Draw the VFB glyph onto a segment pen. Uses the object's `master_index` property
        to determine which master is drawn.
        """
        if self.entry.data is None:
            raise ValueError

        glyph = self.entry.data

        in_path = False
        in_qcurve = False

        for n in glyph.get("nodes", []):
            node_type = n.get("type")
            if node_type == "move":
                if in_qcurve:
                    pen.addPoint(n["points"][self.master_index][0], "qcurve")
                    in_qcurve = False
                if in_path:
                    pen.endPath()
                pen.beginPath()
                in_path = True
                pen.addPoint(n["points"][self.master_index][0], "move")
            elif node_type == "line":
                if in_qcurve:
                    pen.addPoint(n["points"][self.master_index][0], "qcurve")
                    in_qcurve = False
                else:
                    pen.addPoint(n["points"][self.master_index][0], "line")
            elif node_type == "curve":
                pt3, pt1, pt2 = n["points"][self.master_index]
                pen.addPoint(pt1, None)
                pen.addPoint(pt2, None)
                pen.addPoint(pt3, "curve")
            elif node_type == "qcurve":
                if not in_qcurve:
                    in_qcurve = True
                pen.addPoint(n["points"][self.master_index][0], None)
            else:
                raise ValueError(f"Unknown node type: '{node_type}'")
        if in_path:
            pen.endPath()

        for c in glyph.get("components", []):
            baseGlyphName = self._parent.glyph_order[c["gid"]]
            transformation = (
                c["scaleX"][self.master_index],
                0,
                0,
                c["scaleY"][self.master_index],
                c["offsetX"][self.master_index],
                c["offsetY"][self.master_index],
            )
            pen.addComponent(baseGlyphName, transformation)

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
        # FIXME: Add test!!!
        if self.entry.data is None:
            if self.entry.data is None:
                # Make an empty glyph
                self.empty()
            else:
                self.decompile()
        return VfbGlyphPointPen(self, self._parent)


class VfbGlyphMaster:
    def __init__(self, glyph: VfbGlyph, master_index: int = 0):
        self.glyph = glyph
        self.entry = glyph.entry
        self.master_index = master_index
        self._glyph = None

    @cached_property
    def name(self) -> str | None:
        if self._glyph is None:
            return None

        return self._glyph.name

    def _copy_to_ufo_glyph(self, master_index):
        """
        Copy minimal data to the VfbToUfoGlyph. Only data that is necessary for the pen
        methods is copied.
        """
        if self.entry.data is None:
            raise ValueError

        _mm_glyph = VfbToUfoGlyph()
        _mm_glyph.name = self.entry.data["name"]

        if "components" in self.entry.data:
            _mm_glyph.mm_components = self.entry.data["components"]

        if "metrics" in self.entry.data:
            _mm_glyph.mm_metrics = self.entry.data["metrics"]

        if "nodes" in self.entry.data:
            _mm_glyph.mm_nodes = self.entry.data["nodes"]

        # TODO: Support point names used by TT hinting
        # if "tth" in self.entry.data:
        #     _mm_glyph.tth_commands = self.entry.data["tth"]

        self._glyph = UfoMasterGlyph(
            mm_glyph=_mm_glyph,
            glyph_order=self.glyph._parent.glyph_order,
            master_index=master_index,
        )
        self._glyph.build()

    def clearContours(self):
        if self.master_index == 0:
            target = self.entry.data
        else:
            if self.entry.temp_masters is None:
                self.entry.temp_masters = [
                    {} for _ in range(self.glyph._parent.num_masters)
                ]
            target = self.entry.temp_masters[self.master_index]
        try:
            del target["hints"]
        except KeyError:
            pass
        target["nodes"] = []

    def drawPoints(self, pen: AbstractPointPen) -> None:
        """
        Draw the VFB glyph onto a point pen.
        """
        if self.entry.data is None:
            raise ValueError

        if self._glyph is None:
            self._copy_to_ufo_glyph(self.master_index)

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
        # FIXME: Add test!!!
        if self.entry.data is None:
            if self.entry.data is None:
                # Make an empty glyph
                self.glyph.empty()
            else:
                self.entry.decompile()
        return VfbGlyphPointPen(self, self.glyph._parent)
