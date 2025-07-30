from __future__ import annotations

import logging
import xml.etree.ElementTree as elementTree
from typing import TYPE_CHECKING

from vfbLib import DIRECTIONS
from vfbLib.ufo.typing import HintSet, UfoHintingV2, UfoHintSet
from vfbLib.ufo.vfb2ufo import PS_GLYPH_LIB_KEY

if TYPE_CHECKING:
    from vfbLib.typing import HintDict, HintTuple
    from vfbLib.ufo.glyph import VfbToUfoGlyph
    from vfbLib.ufo.paths import UfoMasterGlyph


logger = logging.getLogger(__name__)


def normalize_hint(hint: tuple[str, int, int]):
    direction, pos, width = hint
    if width < 0:
        if width not in (-21, -20):  # Skip ghost hints
            pos = pos + width
            width = abs(width)
    return (direction, pos, width)


def normalize_hint_dict(hint: HintDict, name: str = "dummy"):
    return normalize_hint((name, hint["pos"], hint["width"]))


def build_ps_glyph_hints(
    mmglyph: VfbToUfoGlyph,
    glyph: UfoMasterGlyph,
    master_hints: dict[str, list[HintTuple]],
) -> None:
    """
    Set the master-specific hints from data to the glyph lib

    Args:
        mmglyph (VfbToUfoGlyph): The multiple-master auxilliary glyph object
        glyph (UfoMasterGlyph): The target glyph
        master_hints (dict[str, list[HintTuple]]): The hints with their position and
            width adapted to the master
    """
    # Set the master-specific hints from data to the glyph lib
    # Use the format defined in UFO3, not what FL does.
    # https://unifiedfontobject.org/versions/ufo3/glyphs/glif/#publicpostscripthints

    # Quote from
    # https://github.com/adobe-type-tools/psautohint/blob/master/python/psautohint/ufoFont.py
    """
    A <dict> element in the hintSetList array identifies a specific point by its
    name, and describes a new set of stem hints which should be applied before the
    specific point.

    A <string> element in the flexList identifies a specific point by its name.
    The point is the first point of a curve. The presence of the element is a
    processing suggestion, that the curve and its successor curve should be
    converted to a flex operator.

    One challenge in applying the hintSetList and flexList elements is that in
    the GLIF format, there is no explicit start and end operator: the first path
    operator is both the end and the start of the path. I have chosen to convert
    this to T1 by taking the first path operator, and making it a move-to. I then
    also use it as the last path operator. An exception is a line-to; in T1, this
    is omitted, as it is implied by the need to close the path. Hence, if a hintset
    references the first operator, there is a potential ambiguity: should it be
    applied before the T1 move-to, or before the final T1 path operator? The logic
    here applies it before the move-to only.
    <glyph>
    ...
        <lib>
            <dict>
                <key><com.adobe.type.autohint></key>
                <dict>
                    <key>id</key>
                    <string> <fingerprint for glyph> </string>
                    <key>hintSetList</key>
                    <array>
                        <dict>
                        <key>pointTag</key>
                        <string> <point name> </string>
                        <key>stems</key>
                        <array>
                            <string>hstem <position value> <width value></string>*
                            <string>vstem <position value> <width value></string>*
                            <string>hstem3 <position value 0>...<position value 5>
                            </string>*
                            <string>vstem3 <position value 0>...<position value 5>
                            </string>*
                        </array>
                        </dict>*
                    </array>

                    <key>flexList</key>*
                    <array>
                        <string><point name></string>+
                    </array>
                </dict>
            </dict>
        </lib>
    </glyph>

    Example from "B" in SourceCodePro-Regular
    <key><com.adobe.type.autohint><key>
    <dict>
        <key>id</key>
        <string>64bf4987f05ced2a50195f971cd924984047eb1d79c8c43e6a0054f59cc85dea23
        a49deb20946a4ea84840534363f7a13cca31a81b1e7e33c832185173369086</string>
        <key>hintSetList</key>
        <array>
            <dict>
                <key>pointTag</key>
                <string>hintSet0000</string>
                <key>stems</key>
                <array>
                    <string>hstem 338 28</string>
                    <string>hstem 632 28</string>
                    <string>hstem 100 32</string>
                    <string>hstem 496 32</string>
                </array>
            </dict>
            <dict>
                <key>pointTag</key>
                <string>hintSet0005</string>
                <key>stems</key>
                <array>
                    <string>hstem 0 28</string>
                    <string>hstem 338 28</string>
                    <string>hstem 632 28</string>
                    <string>hstem 100 32</string>
                    <string>hstem 454 32</string>
                    <string>hstem 496 32</string>
                </array>
            </dict>
            <dict>
                <key>pointTag</key>
                <string>hintSet0016</string>
                <key>stems</key>
                <array>
                    <string>hstem 0 28</string>
                    <string>hstem 338 28</string>
                    <string>hstem 632 28</string>
                    <string>hstem 100 32</string>
                    <string>hstem 496 32</string>
                </array>
            </dict>
        </array>
    <dict>
    """
    hint_sets = []
    stems: list[HintTuple] = []
    hint_set: HintSet = HintSet(pointTag="0", stems=stems)
    if mmglyph.hintmasks:
        for mask in mmglyph.hintmasks:
            for direction in DIRECTIONS:
                dd, hint_index = mask
                if direction == dd:
                    master_direction_hints = master_hints[direction]
                    if hint_index < len(master_direction_hints):
                        hint: HintTuple = master_direction_hints[hint_index]
                        hint_set["stems"].append(hint)
                    else:
                        logger.debug(
                            f"Hint mask '{direction}' with index {hint_index} found in "
                            f"glyph {glyph.name}, but hint list is empty."
                        )
            if mask[0] == "r":
                hint_set["pointTag"] = mmglyph.get_point_label(
                    index=int(hint_set["pointTag"]),
                    code="PSHintReplacement",
                    start_count=0,
                )
                hint_sets.append(hint_set)
                node_index = mask[1]
                # FIXME: What do negative values mean?
                if node_index < 0:
                    node_index = abs(node_index) - 1
                stems = []
                hint_set = HintSet(pointTag=str(node_index), stems=stems)

        if hint_set["stems"]:
            # Append the last hint set
            hint_set["pointTag"] = mmglyph.get_point_label(
                index=int(hint_set["pointTag"]),
                code="PSHintReplacement",
                start_count=0,
            )
            hint_sets.append(hint_set)
    else:
        # Only one hint set, always make a hint set with first point
        for direction in DIRECTIONS:
            for hint in master_hints[direction]:
                hint_set["stems"].append(hint)
        if hint_set["stems"]:
            hint_set["pointTag"] = mmglyph.get_point_label(
                index=int(hint_set["pointTag"]),
                code="PSHintReplacement",
                start_count=0,
            )
            hint_sets = [hint_set]

    # Reformat stems from sortable tuples to str required by UFO spec
    ufo_hint_sets = {}
    for hint_set in hint_sets:
        point_tag = hint_set["pointTag"]
        ufo_hint_set = UfoHintSet(
            pointTag=point_tag,
            stems=[f"{h[0]} {h[1]} {h[2]}" for h in sorted(set(hint_set["stems"]))],
        )
        if ufo_hint_set["stems"]:
            # Only add if the set has stems
            if ufo_hint_set["pointTag"] in ufo_hint_sets:
                if ufo_hint_sets[point_tag] != ufo_hint_set:
                    # Warn about duplicate hint sets per point, but use the last one
                    logger.warning(
                        f"Duplicate hint sets for point '{point_tag}' "
                        f"in glyph '{glyph.name}':"
                    )
                    logger.warning(f"    Old: {ufo_hint_sets[point_tag]}")
                    logger.warning(f"    New: {ufo_hint_set}")
                    logger.warning("    Using the new hint set.")
            ufo_hint_sets[point_tag] = ufo_hint_set

    if ufo_hint_sets:
        if not hasattr(glyph, "lib"):
            glyph.lib = {}
        glyph.lib[PS_GLYPH_LIB_KEY] = {
            "formatVersion": "1",
            # "id": "FIXME",
            "hintSetList": list(ufo_hint_sets.values()),
            # "flexList": [],
        }


def get_master_hints(
    mmglyph: VfbToUfoGlyph, master_index=0
) -> dict[str, list[HintTuple]]:
    hints: dict[str, list[HintTuple]] = {"h": [], "v": []}

    # Hints
    for direction in DIRECTIONS:
        dh = mmglyph.mm_hints[direction]
        for mm_hints in dh:
            hint = mm_hints[master_index]
            hint = normalize_hint_dict(hint, f"{direction}stem")
            hints[direction].append(hint)

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
                pos = src_pos - width
            elif itgt == -2:  # Top ghost
                width = -20
            else:
                tgt = mmglyph.mm_nodes[itgt]
                tgt_pos = tgt["points"][master_index][0][i]
                width = tgt_pos - src_pos
                # pos = min(src_pos, tgt_pos)

            d = "v" if axis == "x" else "h"
            # Don't normalize those values, the above code already did that
            hint = (f"{d}stem", pos, width)
            hints[d].append(hint)

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

    v2 = UfoHintingV2()
    root = elementTree.fromstring(data)
    hintset: UfoHintSet | None = None
    hintSetList: list[UfoHintSet] = []
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
                tag, pos, width = normalize_hint(
                    (el.tag, int(el.attrib["pos"]), int(el.attrib["width"]))
                )
                hintset["stems"].append(f"{tag} {pos} {width}")
    if hintset:
        hintSetList.append(hintset)
    if hintSetList:
        v2["hintSetList"] = hintSetList

    # Remove empty entries
    empty = [k for k in v2 if not v2[k]]
    for k in empty:
        del v2[k]
    return v2
