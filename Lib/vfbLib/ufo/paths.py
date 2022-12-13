from __future__ import annotations

import logging

from typing import List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    from fontTools.ufoLib.glifLib import GLIFPointPen
    from vfbLib.ufo.typing import UfoComponent, UfoContour


logger = logging.getLogger(__name__)


def draw_glyph(
    contours: List[UfoContour],
    components: List[UfoComponent],
    pen: GLIFPointPen,
):
    for contour in contours:
        pen.beginPath()
        for segment_type, smooth, name, pt in contour:
            pen.addPoint(pt, segment_type, name=name, smooth=smooth)
        pen.endPath()

    for gn, tr in components:
        pen.addComponent(glyphName=gn, transformation=tr)


def apply_closepath(contour):
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

    else:
        _, smooth, name, pt = contour[0]
        contour[0] = ("line", smooth, name, pt)


def flush_contour(contour, path_is_open) -> List:
    if not path_is_open:
        last_type = contour[-1][0]
        if last_type in ("line", "curve", "qcurve"):
            apply_closepath(contour)

        elif last_type is None:
            _, smooth, name, pt = contour[0]
            contour[0] = ("qcurve", smooth, name, pt)
    return contour


def get_master_glyph(
    mmglyph, glyph_order: List[str], master_index=0
) -> Tuple[List[UfoContour], List[UfoComponent]]:
    # Extract a single master glyph from an mm glyph

    contours = []
    path_is_open = False
    in_qcurve = False
    if hasattr(mmglyph, "mm_nodes"):
        contour: UfoContour = []
        for i, n in enumerate(mmglyph.mm_nodes):
            name: str | None = mmglyph.point_labels.get(i, None)
            nodes = n["points"][master_index]
            pt = nodes[0]
            segment_type = n["type"]
            flags = n["flags"]
            smooth = bool(flags & 1)

            if segment_type == "move":
                if contour:
                    contours.append(flush_contour(contour, path_is_open))
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
            contours.append(flush_contour(contour, path_is_open))

    components: List[UfoComponent] = []
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
