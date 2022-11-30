from __future__ import annotations

import xml.etree.cElementTree as elementTree

from vfbLib.ufo.types import UfoHintingV2, UfoHintSet
from typing import Dict, List


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
