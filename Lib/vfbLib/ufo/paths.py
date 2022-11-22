from __future__ import annotations
from typing import List, Tuple, TYPE_CHECKING


if TYPE_CHECKING:
    Point = Tuple[int, int]
    Contour = List[List[None | str | Point]] | None
    ContourList = List[Contour]
    ComponentList = List[
        Tuple[str, Tuple[float, float, float, float, int, int]]
    ]


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
        for n in mmglyph.mm_nodes:
            # Nodes for the current master
            nodes = n["points"][master_index]
            segment_type = n["type"]
            flags = n["flags"]

            # print("****", segment_type, nodes)

            if segment_type == "line":
                if qcurve:
                    effective_type = "qcurve"
                    qcurve = False
                else:
                    effective_type = "line"

                assert contour is not None
                contour.append(
                    [effective_type, flags, (nodes[0]["x"], nodes[0]["y"])]
                )

            elif segment_type == "move":
                if contour is not None:
                    if not open_path:
                        contour[0] = contour.pop()
                    contours.append(contour)
                open_path = bool(flags & 8)  # Current contour is open
                contour = [["move", flags, (nodes[0]["x"], nodes[0]["y"])]]
                qcurve = False

            elif segment_type == "curve":
                pt3, pt1, pt2 = nodes
                assert contour is not None
                contour.append([None, flags, (pt1["x"], pt1["y"])])
                contour.append([None, flags, (pt2["x"], pt2["y"])])
                contour.append(["curve", flags, (pt3["x"], pt3["y"])])
                qcurve = False

            elif segment_type == "qcurve":
                qcurve = True
                assert contour is not None
                contour.append([None, flags, (nodes[0]["x"], nodes[0]["y"])])

        if contour is not None:
            if not open_path:
                if contour[-1][0] is not None:
                    contour[0] = contour.pop()
                else:
                    if qcurve:
                        contour[0][0] = "qcurve"
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
