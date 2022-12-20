from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Dict, List, Tuple
from vfbLib.ufo.groups import build_glyph_to_group_maps

if TYPE_CHECKING:
    from vfbLib.ufo.typing import UfoGroups, UfoMasterKerning, UfoMMKerning


logger = logging.getLogger(__name__)


class UfoKerning:
    def __init__(
        self,
        glyph_order: List[str],
        groups: UfoGroups,
        mm_kerning: UfoMMKerning,
    ):
        self.glyph_order = glyph_order
        group_info = build_glyph_to_group_maps(groups)
        self.groups, self.glyph_group_1, self.glyph_group_2 = group_info
        self.mm_kerning = mm_kerning
        self.master_kerning: UfoMasterKerning = {}
        self._make_name_based_kerning()

    def _is_exception(self, L: str, R: str):
        L_is_key = f"public.kern1.{L}" in self.groups or L not in self.glyph_group_1

        R_is_key = f"public.kern2.{R}" in self.groups or R not in self.glyph_group_2

        if L_is_key and R_is_key:
            return False

        return True

    def _make_name_based_kerning(self) -> None:
        """
        Convert the glyph indices to glyph names. Also solves group kerning
        references.
        """
        self.mm_kerning_names: Dict[Tuple[str, str], List[int]] = {}
        for pair, values in self.mm_kerning.items():
            L, Rid = pair
            # Make right GID into glyph name
            R = self.glyph_order[int(Rid)]

            # Is the left glyph a keyglyph? It is so if there's a kerning group
            # named after it. In that case, use the group name instead of the
            # glyph name.
            left_group = f"public.kern1.{L}"
            left = left_group if left_group in self.groups else L

            # Is the right glyph a keyglyph?
            right_group = f"public.kern2.{R}"
            right = right_group if right_group in self.groups else R

            self.mm_kerning_names[left, right] = values

    def extract_master_kerning(self, master_index) -> None:
        """
        Extract the kerning value for master_index.
        """
        self.master_kerning = {}
        for pair, values in self.mm_kerning_names.items():
            value = values[master_index]
            if value != 0 or self._is_exception(*pair):
                self.master_kerning[pair] = value
