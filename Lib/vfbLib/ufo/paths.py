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


class Vfb2UfoPen(BasePointToSegmentPen):
    def __init__(self) -> None:
        super().__init__()
        self.contours = []

    def _flushContour(self, segments):
        self.contours.append(segments)


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


def flush_contour(contour, path_is_open) -> List:
    if not path_is_open:
        last_type = contour[-1][0]
        if last_type == "line":
            if contour[-1][2] == contour[0][2]:
                # Equal coords, use closepath to draw the last line
                # raise ValueError
                contour[0] = contour.pop()
            else: contour[0][0] = "line"
        elif last_type == "curve":
            if contour[-1][2] == contour[0][2]:
                contour[0] = contour.pop()
            else:
                contour[0][0] = "line"
        elif last_type == "qcurve":
            if contour[-1][2] == contour[0][2]:
                contour[0] = contour.pop()
            else:
                contour[0][0] = "line"
        elif last_type is None:
            contour[0][0] = "qcurve"
    return contour


def get_master_glyph(
    mmglyph, glyph_order: List[str], master_index=0
) -> Tuple[ContourList, ComponentList]:
    # Extract a single master glyph from an mm glyph

    contours = []
    path_is_open = False
    in_qcurve = False
    if hasattr(mmglyph, "mm_nodes"):
        contour = []
        for n in mmglyph.mm_nodes:
            nodes = n["points"][master_index]
            pt = nodes[0]
            segment_type = n["type"]
            flags = n["flags"]
            smooth = bool(flags & 1)

            if segment_type == "move":
                if contour:
                    contours.append(flush_contour(contour, path_is_open))
                contour = [["move", smooth, pt]]
                path_is_open = bool(flags & 8)
                in_qcurve = False

            elif segment_type == "line":
                if in_qcurve:
                    contour.append(["qcurve", smooth, pt])
                    in_qcurve = False
                else:
                    contour.append(["line", smooth, pt])

            elif segment_type == "curve":
                pt, c1, c2 = nodes
                contour.append([None, False, c1])
                contour.append([None, False, c2])
                contour.append(["curve", smooth, pt])
                in_qcurve = False

            elif segment_type == "qcurve":
                contour.append([None, False, pt])
                in_qcurve = True

            else:
                print(f"Unknown segment type: {segment_type}")
                raise ValueError

        if contour:
            contours.append(flush_contour(contour, path_is_open))

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
