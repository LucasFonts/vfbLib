from __future__ import annotations

import logging

from colorsys import hls_to_rgb
from typing import TYPE_CHECKING, Any, Dict, List, Tuple
from vfbLib.ufo.vfb2ufo import vfb2ufo_label_codes

if TYPE_CHECKING:
    from vfbLib.typing import (
        Anchor,
        GuidePropertyList,
        GuideDict,
        HintDict,
        LinkDict,
        MMNode,
    )


logger = logging.getLogger(__name__)


class VfbToUfoGlyph:
    def __init__(self) -> None:
        self.anchors: List[Anchor] = []
        self.guide_properties: GuidePropertyList = []
        self.hintmasks: List[Dict[str, int]] = []
        self.labels: Dict[str, int] = {}
        self.lib: Dict[str, Any] = {}
        self.links: LinkDict = {}
        self.mm_anchors: List[Any] | None = None
        self.mm_components: List[Any] = []
        self.mm_guides: GuideDict | None = None
        self.mm_hints: HintDict = {"h": [], "v": []}
        self.mm_metrics: List[Tuple[int, int]] = []
        self.mm_nodes: List[MMNode] = []
        self.name: str | None = None
        self.note: str | None = None
        self.point_labels: Dict[int, str] = {}
        self.rename_points: Dict[str, str]
        self.tth_commands: List[Dict[str, str | bool]] = []
        self.unicodes: List[int] = []

    def get_point_label(self, index: int, code: str, start_count: int = 1) -> str:
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
        i = start_count
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
