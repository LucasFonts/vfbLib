from __future__ import annotations

import xml.etree.cElementTree as elementTree

from vfbLib.ufo.types import UfoHintingV2, UfoHintSet
from vfbLib.ufo.vfb2ufo import PS_GLYPH_LIB_KEY
from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from vfbLib.types import Hint
    from fontTools.ufoLib.glifLib import Glyph
    from vfbLib.ufo.glyph import VfbToUfoGlyph


def normalize_hint(hint: Tuple[str, int, int]):
    print("Normalize:", hint)
    direction, pos, width = hint
    if width < 0:
        if width not in (-21, -20):  # Skip ghost hints
            pos = pos + width
            width = abs(width)
    print((direction, pos, width))
    return (direction, pos, width)


def normalize_hint_dict(hint: Hint, name: str = "dummy"):
    return normalize_hint((name, hint["pos"], hint["width"]))


def build_ps_glyph_hints(
    mmglyph: VfbToUfoGlyph,
    glyph: Glyph,
    master_hints: Dict[str, List[Tuple[str, int, int]]],
) -> None:
    # Set the master-specific hints from data to the glyph lib
    # Use the format defined in UFO3, not what FL does.
    # https://github.com/adobe-type-tools/psautohint/blob/master/python/psautohint/ufoFont.py
    # https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#publicpostscripthints
    print(f"Building glyph hints for {mmglyph.name}")
    hint_sets = []
    label = mmglyph.get_point_label(
        index=0, code="PSHintReplacement", start_count=0
    )
    hint_set = {
        "pointTag": label,
        "stems": [],
    }
    if mmglyph.hintmasks:
        for mask in mmglyph.hintmasks:
            for d in ("h", "v"):
                if d in mask:
                    hint_index = mask[d]
                    hint = master_hints[d][hint_index]
                    print("   ", d, mask[d], "->", hint)
                    hint_set["stems"].append(hint)
            if "r" in mask:
                hint_sets.append(hint_set)
                node_index = mask["r"]
                print(f"    Replacement point: {node_index}")
                # FIXME: What do negative values mean?
                if node_index < 0:
                    node_index = abs(node_index) - 1
                label = mmglyph.get_point_label(
                    index=node_index, code="PSHintReplacement"
                )
                hint_set = {
                    "pointTag": label,
                    "stems": [],
                }

        if hint_set["stems"]:
            # Append the last hint set
            hint_sets.append(hint_set)
    else:
        # Only one hint set, always make a hint set with first point
        for d in ("h", "v"):
            for hint in master_hints[d]:
                hint_set["stems"].append(hint)
        hint_sets = [hint_set]

    # Reformat stems from sortable tuples to str required by UFO spec
    for hint_set in hint_sets:
        hint_set["stems"] = [
            f"{cmd} {pos} {width}"
            for cmd, pos, width in sorted(set(hint_set["stems"]))
        ]

    if hint_sets:
        glyph.lib[PS_GLYPH_LIB_KEY] = {
            # "id": "FIXME",
            "hintSetList": hint_sets,
            # "flexList": [],
        }


def get_master_hints(
    mmglyph: VfbToUfoGlyph, glyph: Glyph, master_index=0
) -> Dict[str, List[Tuple[str, int, int]]]:
    hints = {"h": [], "v": []}

    # Hints
    for d in "hv":
        dh = mmglyph.mm_hints[d]
        for mm_hints in dh:
            hint = mm_hints[master_index]
            hint = normalize_hint_dict(hint, f"{d}stem")
            hints[d].append(hint)

    # Links
    if not mmglyph.links:
        return hints

    # Convert links to hints
    for i, axis in enumerate("xy"):
        direction_links = mmglyph.links[axis]
        for link in direction_links:
            isrc, itgt = link  # indices of source and target node
            src = mmglyph.mm_nodes[isrc]
            src_pos = src["points"][master_index][0][i]
            pos = src_pos
            if itgt == -1:  # Bottom ghost
                width = -21
            elif itgt == -2:  # Top ghost
                width = -20
            else:
                tgt = mmglyph.mm_nodes[itgt]
                tgt_pos = tgt["points"][master_index][0][i]
                # This would be correct IMHO:
                # width = abs(tgt_pos - src_pos)
                # pos = min(src_pos, tgt_pos)
                # This is how FontLab does it:
                width = tgt_pos - src_pos
            d = "v" if axis == "x" else "h"
            hints[d].append((f"{d}stem", pos, width))

    return hints


def update_adobe_hinting(data) -> UfoHintingV2:
    # Convert Adobe hinting data from v1 to v2.
    # https://github.com/adobe-type-tools/psautohint/blob/master/python/psautohint/ufoFont.py
    try:
        # Data may be base64-encoded
        data = data.decode()
    except AttributeError:
        pass
    if not isinstance(data, str):
        # V1 data is stored as str, so if it is not a str, we have nothing to do
        return data

    v2: UfoHintingV2 = {
        # "flexList": [],
        # "id": "",
    }
    root = elementTree.fromstring(data)
    hintset: UfoHintSet | None = None
    hintSetList: List[UfoHintSet] = []
    for el in root.iter():
        if el.tag == "hintSetList":
            hintSetList = []
        elif el.tag == "hintset":
            if hintset:
                hintSetList.append(hintset)
            hintset = {
                "pointTag": el.attrib["pointTag"],
                "stems": [],
            }
        elif el.tag in ("hstem", "vstem"):
            if hintset is not None:
                hintset["stems"].append(
                    f'{el.tag} {el.attrib["pos"]} {el.attrib["width"]}'
                )
    if hintset:
        hintSetList.append(hintset)
    if hintSetList:
        v2["hintSetList"] = hintSetList

    # Remove empty entries
    empty = [k for k in v2 if not v2[k]]
    for k in empty:
        del v2[k]
    return v2
