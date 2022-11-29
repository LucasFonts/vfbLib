from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vfbLib.ufo.types import UfoGroups, UfoMasterKerning, UfoMMKerning


class UfoKerning:
    def __init__(
        self,
        glyphOrder: List[str],
        groups: UfoGroups,
        mm_kerning: UfoMMKerning,
        master_index: int = 0,
    ):
        self.glyphOrder = glyphOrder
        self.groups = groups
        self.mm_kerning = mm_kerning
        self.master_index = master_index
        self.master_kerning: UfoMasterKerning = {}

    def extract_master_kerning(self, master_index) -> UfoMasterKerning:
        # FIXME: Must look up class kerning references
        self.master_kerning = kerning = {}
        for pair, values in self.mm_kerning.items():
            L, Rid = pair
            kerning[L, self.glyphOrder[int(Rid)]] = values[master_index]
        return kerning
