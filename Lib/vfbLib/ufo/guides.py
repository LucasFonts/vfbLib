from __future__ import annotations
from typing import Dict, List


def get_master_guides(mm_guides: Dict[str, List], master_index: int) -> List:
    # Concatenate guidlines for both directions and extract coords for master_index
    guides = []
    for d in "hv":
        for master_guide in mm_guides[d][master_index]:
            coord = "y" if d == "h" else "x"
            guide = {coord: master_guide["pos"]}
            angle = master_guide["angle"]
            if angle:
                guide["angle"] = angle
            guides.append(guide)
    return guides


def apply_guide_properties(
    guides, properties: List[Dict[str, int | str]]
) -> None:
    # Update the guides with names and colors from properties
    for prop in properties:
        guide = guides[prop["index"] - 1]  # index is 1-based
        if "color" in prop:
            color = prop["color"]
            r = int(color[1:3], 16) / 0xFF
            g = int(color[3:5], 16) / 0xFF
            b = int(color[5:7], 16) / 0xFF
            guide["color"] = f"{r:0.4f},{g:0.4f},{b:0.4f},1"
        if "name" in prop:
            guide["name"] = prop["name"]
