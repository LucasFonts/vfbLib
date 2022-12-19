from __future__ import annotations

import logging

from typing import Dict, List, TYPE_CHECKING


if TYPE_CHECKING:
    from fontTools.ufoLib.glifLib import GLIFPointPen
    from vfbLib.ufo.glyph import VfbToUfoGlyph
    from vfbLib.ufo.typing import UfoComponent, UfoContour


logger = logging.getLogger(__name__)


class UfoMasterGlyph:
    def __init__(
        self, mm_glyph: VfbToUfoGlyph, glyph_order: List[str], master_index: int
    ) -> None:
        self.mm_glyph = mm_glyph
        self.glyph_order = glyph_order
        self.master_index = master_index

        self.components: List[UfoComponent] = []
        self.contours: List[UfoContour] = []
        self.rename_points: Dict[str, str] = {}

    def build(self) -> None:
        # Extract the single master glyph from an mm glyph. The main method.

        self.contours = []
        rename_points_dict: Dict[str, str] = {}
        path_is_open = False
        in_qcurve = False
        if hasattr(self.mm_glyph, "mm_nodes"):
            contour: UfoContour = []
            for i, n in enumerate(self.mm_glyph.mm_nodes):
                name: str | None = self.mm_glyph.point_labels.get(i, None)
                nodes = n["points"][self.master_index]
                pt = nodes[0]
                segment_type = n["type"]
                flags = n["flags"]
                smooth = bool(flags & 1)

                if segment_type == "move":
                    self._append_contour(contour, path_is_open)
                    contour = [("move", smooth, name, pt)]
                    path_is_open = bool(flags & 8)
                    in_qcurve = False

                elif segment_type == "line":
                    if in_qcurve:
                        contour.append(("qcurve", smooth, name, pt))
                        in_qcurve = False
                    else:
                        contour.append(("line", smooth, name, pt))

                elif segment_type == "curve":
                    pt, c1, c2 = nodes
                    contour.append((None, False, None, c1))
                    contour.append((None, False, None, c2))
                    contour.append(("curve", smooth, name, pt))
                    in_qcurve = False

                elif segment_type == "qcurve":
                    contour.append((None, False, name, pt))
                    in_qcurve = True

                else:
                    logger.error(f"Unknown segment type: {segment_type}")
                    raise ValueError

            if contour:
                self._append_contour(contour, path_is_open)

        self.components: List[UfoComponent] = []
        if hasattr(self.mm_glyph, "mm_components"):
            for c in self.mm_glyph.mm_components:
                transform = (
                    c["scaleX"][self.master_index],
                    0.0,
                    0.0,
                    c["scaleY"][self.master_index],
                    c["offsetX"][self.master_index],
                    c["offsetY"][self.master_index],
                )
                self.components.append((self.glyph_order[c["gid"]], transform))

    def draw_glyph(self, pen: GLIFPointPen) -> None:
        """
        Draw the glyph to the supplied point pen.
        """
        for contour in self.contours:
            pen.beginPath()
            for segment_type, smooth, name, pt in contour:
                pen.addPoint(pt, segment_type, name=name, smooth=smooth)
            pen.endPath()

        for gn, tr in self.components:
            pen.addComponent(glyphName=gn, transformation=tr)

    def _append_contour(self, contour: UfoContour, path_is_open: bool) -> None:
        """
        Append the contour to the glyph's contours, applying closepath optimizations.
        """
        if contour:
            ct = self._flush_contour(contour, path_is_open)
            self.contours.append(ct)

    def _apply_closepath(self, contour: UfoContour) -> None:
        """
        Apply closepath optimizations to the contour.
        """
        if contour[-1][3] == contour[0][3]:
            # Equal coords, use closepath to draw the last line
            name = contour[0][2]
            contour[0] = contour.pop()
            if name is not None:
                # Keep old point name
                if contour[0][2] is None:
                    t, smooth, _, pt = contour[0]
                    contour[0] = (t, smooth, name, pt)
                else:
                    logger.warning(
                        f"Point name conflict in {contour[0]} vs. {name} while "
                        f"applying closepath. Not applying old name ({name})"
                    )
                    # Note the old and new name so the labels can be updated
                    self.rename_points[name] = contour[0][2]

        else:
            _, smooth, name, pt = contour[0]
            contour[0] = ("line", smooth, name, pt)

    def _flush_contour(self, contour: UfoContour, path_is_open: bool) -> UfoContour:
        """
        Post-process a contour before it is appended to the glyph's contours.
        """
        if not path_is_open:
            last_type = contour[-1][0]
            if last_type in ("line", "curve", "qcurve"):
                self._apply_closepath(contour)

            elif last_type is None:
                _, smooth, name, pt = contour[0]
                contour[0] = ("qcurve", smooth, name, pt)
        return contour
