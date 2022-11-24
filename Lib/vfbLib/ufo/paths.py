from __future__ import annotations

from fontTools.pens.pointPen import AbstractPointPen
from typing import List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from vfbLib.ufo.glyph import VfbToUfoGlyph
    from vfbLib.ufo.types import ComponentList, ContourList


def draw_glyph(
    contours: ContourList,
    components: ComponentList,
    pen: AbstractPointPen,
):
    for contour in contours:
        pen.beginPath()
        for segment_type, smooth, name, pt in contour:
            pen.addPoint(pt, segment_type, name=name, smooth=smooth)
        pen.endPath()

    for gn, tr in components:
        pen.addComponent(glyphName=gn, transformation=tr)


def flush_contour(contour, path_is_open) -> List:
    if not path_is_open:
        last_type = contour[-1][0]
        if last_type == "line":
            if contour[-1][3] == contour[0][3]:
                # Equal coords, use closepath to draw the last line
                # raise ValueError
                contour[0] = contour.pop()
            else:
                contour[0][0] = "line"
        elif last_type == "curve":
            if contour[-1][3] == contour[0][3]:
                contour[0] = contour.pop()
            else:
                contour[0][0] = "line"
        elif last_type == "qcurve":
            if contour[-1][3] == contour[0][3]:
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
        for i, n in enumerate(mmglyph.mm_nodes):
            name = mmglyph.point_labels.get(i, None)
            nodes = n["points"][master_index]
            pt = nodes[0]
            segment_type = n["type"]
            flags = n["flags"]
            smooth = bool(flags & 1)

            if segment_type == "move":
                if contour:
                    contours.append(flush_contour(contour, path_is_open))
                contour = [["move", smooth, name, pt]]
                path_is_open = bool(flags & 8)
                in_qcurve = False

            elif segment_type == "line":
                if in_qcurve:
                    contour.append(["qcurve", smooth, name, pt])
                    in_qcurve = False
                else:
                    contour.append(["line", smooth, name, pt])

            elif segment_type == "curve":
                pt, c1, c2 = nodes
                contour.append([None, False, None, c1])
                contour.append([None, False, None, c2])
                contour.append(["curve", smooth, name, pt])
                in_qcurve = False

            elif segment_type == "qcurve":
                contour.append([None, False, name, pt])
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
