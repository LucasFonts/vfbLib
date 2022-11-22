from __future__ import annotations

from fontTools.pens.pointPen import BasePointToSegmentPen
from pprint import pprint
from typing import List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    Point = Tuple[int, int]
    Contour = List[List[None | str | Point]] | None
    ContourList = List[Contour]
    ComponentList = List[
        Tuple[str, Tuple[float, float, float, float, int, int]]
    ]


def Vfb2UfoPen(BasePointToSegmentPen):
    def _flushContour(self, segments):
        pprint(segments)


def draw_glyph(mm_glyph, contours, components, pen):
    i = 0
    for contour in contours:
        pen.beginPath()
        for segment_type, smooth, pt in contour:
            label = mm_glyph.point_labels.get(i, None)
            pen.addPoint(pt, segment_type, name=label, smooth=smooth)
            i += 1
        pen.endPath()

    for gn, tr in components:
        pen.addComponent(glyphName=gn, transformation=tr)


def flush_contour(contour, open_path, ccurve, qcurve) -> List:
    if not open_path:
        last = contour[-1][0]
        if last in ("line", "qcurve"):
            contour[0][0] = "line"
        elif last == "curve":
            if contour[0][2] == contour[-1][2]:
                contour[0][0] = contour.pop()
        elif last is None:
            if qcurve:
                contour[0][0] = "qcurve"
            elif ccurve:
                contour[0][0] = "curve"
    return contour


def get_master_glyph(
    mmglyph, glyph_order: List[str], master_index=0
) -> Tuple[ContourList, ComponentList]:
    # Extract a single master glyph from a mm glyph

    contours = []
    if hasattr(mmglyph, "mm_nodes"):
        contour = []
        for n in mmglyph.mm_nodes:
            nodes = n["points"][master_index]
            segment_type = n["type"]
            flags = n["flags"]
            smooth = bool(flags & 1)
            open_path = bool(flags & 8)

            if segment_type == "move":
                if contour:
                    contours.append(contour)
                contour = [["move", smooth, nodes[0]]]

            elif segment_type == "line":
                contour.append(["line", smooth, nodes[0]])

            elif segment_type == "curve":
                pt3, pt1, pt2 = nodes
                contour.append([None, False, pt1])
                contour.append([None, False, pt2])
                contour.append(["curve", smooth, pt3])

            elif segment_type == "qcurve":
                for pt in nodes[:-1]:
                    contour.append([None, False, pt])
                contour.append(["qcurve", smooth, nodes[-1]])

            else:
                print(f"Unknown segment type: {segment_type}")
                raise ValueError

        if contour:
            contours.append(contour)

    components: ComponentList = []
    if hasattr(mmglyph, "mm_components"):
        for c in mmglyph.mm_components:
            transform = (
                c["scaleX"][master_index],
                0.0,
                0.0,
                c["scaleY"][master_index],
                c["offsetX"][master_index],
                c["offsetY"][master_index],
            )
            components.append((glyph_order[c["gid"]], transform))

    return contours, components
