from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from vfbLib.ufo.typing import UfoGroups, UfoMasterKerning, UfoMMKerning


logger = logging.getLogger(__name__)


class UfoKerning:
    def __init__(
        self,
        glyphOrder: List[str],
        groups: UfoGroups,
        mm_kerning: UfoMMKerning,
    ):
        self.glyphOrder = glyphOrder
        self.groups = groups
        self.mm_kerning = mm_kerning
        self.master_kerning: UfoMasterKerning = {}
        self._build_glyph_to_groups_mapping()
        self._make_name_based_kerning()

    def _build_glyph_to_groups_mapping(self) -> None:
        """
        Glyph name to kerning groups
        """
        self.glyph_group_1: Dict[str, str] = {}
        self.glyph_group_2: Dict[str, str] = {}
        for group in self.groups.items():
            name, glyphs = group
            if name.startswith("public.kern1"):
                for g in glyphs:
                    if g in self.glyph_group_1:
                        logger.error(
                            f"Multiple kerning groups (kern1) for glyph {g}: "
                            f"{self.glyph_group_1[g]}, {name}. New group ignored."
                        )
                        continue
                    self.glyph_group_1[g] = name
            elif name.startswith("public.kern2"):
                for g in glyphs:
                    if g in self.glyph_group_2:
                        logger.error(
                            f"Multiple kerning groups (kern2) for glyph {g}: "
                            f"{self.glyph_group_2[g]}, {name}. New group ignored."
                        )
                        continue
                    self.glyph_group_2[g] = name

    def _is_exception(self, L: str, R: str):
        L_group = f"public.kern1.{L}"
        if L_group in self.groups:
            left_is_key = True
        else:
            left_is_key = L not in self.glyph_group_1

        right_group = f"public.kern2.{R}"
        if right_group in self.groups:
            right_is_key = True
        else:
            right_is_key = R not in self.glyph_group_2

        if left_is_key and right_is_key:
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
            self.mm_kerning_names[left, right] = values

    def extract_master_kerning(self, master_index) -> None:
        """
        Extract the kerning value for master_index.
        """
        self.master_kerning = {}
        for pair, values in self.mm_kerning_names.items():
            value = values[master_index]
            if value != 0 or self._is_exception(*pair):
                self.master_kerning[*pair] = value
