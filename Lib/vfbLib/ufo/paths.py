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
        for segment_type, flags, pt in contour:
            label = mm_glyph.point_labels.get(i, None)
            if segment_type in ("move", "curve", "line"):
                smooth = bool(flags & 1)
            else:
                smooth = False
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
        # print(f"Add nodes to {mmglyph.name}...")
        contours = []
        contour: Contour = None
        open_path = False
        qcurve = False
        ccurve = False
        for n in mmglyph.mm_nodes:
            # Nodes for the current master
            nodes = n["points"][master_index]
            segment_type = n["type"]
            flags = n["flags"]

            if segment_type == "move":
                if contour is not None:
                    contours.append(
                        flush_contour(contour, open_path, ccurve, qcurve)
                    )
                open_path = bool(flags & 8)
                (node,) = nodes
                contour = [["move", flags, (node["x"], node["y"])]]
                qcurve = False
                ccurve = False

            elif segment_type == "line":
                assert contour is not None
                (node,) = nodes
                if qcurve:
                    effective_type = "qcurve"
                else:
                    effective_type = "line"
                contour.append(
                    [effective_type, flags, (nodes[0]["x"], nodes[0]["y"])]
                )
                qcurve = False
                ccurve = False

            elif segment_type == "curve":
                pt3, pt1, pt2 = nodes
                assert contour is not None
                contour.append([None, flags, (pt1["x"], pt1["y"])])
                contour.append([None, flags, (pt2["x"], pt2["y"])])
                contour.append(["curve", flags, (pt3["x"], pt3["y"])])
                qcurve = False
                ccurve = True

            elif segment_type == "qcurve":
                assert contour is not None
                (node,) = nodes
                contour.append([None, flags, (node["x"], node["y"])])
                qcurve = True
                ccurve = False

            else:
                print(f"Unknown segment type: {segment_type}")
                raise ValueError

        if contour is not None:
            if contour is not None:
                contours.append(
                    flush_contour(contour, open_path, ccurve, qcurve)
                )

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
