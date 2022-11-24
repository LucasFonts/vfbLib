from __future__ import annotations

from colorsys import hls_to_rgb
from typing import TYPE_CHECKING, Dict, List
from vfbLib.ufo.vfb2ufo import vfb2ufo_label_codes

if TYPE_CHECKING:
    from vfbLib.ufo.types import Anchor, GuidePropertyList, MMHintsDict, MMNode


class VfbToUfoGlyph:
    def __init__(self) -> None:
        self.anchors: List[Anchor] = []
        self.labels: Dict[str, int] = {}
        self.point_labels: Dict[int, str] = {}
        self.mm_hints: MMHintsDict = {"h": [], "v": []}
        self.mm_nodes: List[MMNode] = []
        self.guide_properties: GuidePropertyList = []

    def get_point_label(self, index: int, code: str) -> str:
        if index in self.point_labels:
            # We already have a label for this point index
            return self.point_labels[index]

        # Special points
        num_nodes = len(self.mm_nodes)
        if index == num_nodes:
            return "lsb"
        elif index == num_nodes + 1:
            return "rsb"

        # Make a new label
        label_short = vfb2ufo_label_codes[code]
        i = 1
        label = "%s%02d" % (label_short, i)
        while label in self.labels:
            i += 1
            label = "%s%02d" % (label_short, i)
        self.labels[label] = index
        self.point_labels[index] = label
        return label

    def set_mark(self, hue):
        self.lib["public.markColor"] = "%0.4f,%0.4f,%0.4f,1" % hls_to_rgb(
            h=hue / 255, l=0.8, s=0.76
        )
