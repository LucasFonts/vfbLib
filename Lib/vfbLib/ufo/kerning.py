from __future__ import annotations

import logging

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vfbLib.ufo.typing import UfoGroups, UfoMasterKerning, UfoMMKerning


logger = logging.getLogger(__name__)


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

    def extract_master_kerning(self, master_index) -> None:
        """
        Extract the kerning value for master_index. Also solves group kerning
        references.
        """
        self.master_kerning = {}
        for pair, values in self.mm_kerning.items():
            L, Rid = pair
            # Make right GID into glyph name
            R = self.glyphOrder[int(Rid)]

            # Is the left glyph a keyglyph? It is so if there's a kerning group
            # named after it. In that case, use the group name instead of the
            # glyph name.
            left_group = f"public.kern1.{L}"
            if left_group in self.groups:
                left = left_group
            else:
                left = L

            # Is the right glyph a keyglyph?
            right_group = f"public.kern2.{R}"
            if right_group in self.groups:
                right = right_group
            else:
                right = R

            self.master_kerning[left, right] = values[master_index]
