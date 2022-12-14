from __future__ import annotations

import logging

from typing import Any, Dict, List
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.vfb2ufo import (
    TT_GLYPH_LIB_KEY,
    vfb2ufo_alignment_rev,
    vfb2ufo_command_codes,
)


logger = logging.getLogger(__name__)


def make_tt_cmd(tt_dict: Dict[str, Any]) -> str:
    code = tt_dict["code"]
    cmd = f'    <ttc code="{code}"'
    for attr in (
        "point",
        "point1",
        "point2",
        "stem",
        "zone",
        "align",
        "delta",
        "ppm1",
        "ppm2",
    ):
        if attr in tt_dict:
            cmd += f' {attr}="{tt_dict[attr]}"'
    if "round" in tt_dict:
        cmd += f' round="{str(tt_dict["round"]).lower()}"'
    cmd += "/>"
    return cmd


def build_tt_glyph_hints(
    glyph: VfbToUfoGlyph,
    data: List[Dict[str, Any]],
    zone_names: Dict[str, List[str]],
    tt_stem_names: List[str],
) -> None:
    # Write TT hints into glyph lib.
    tth = []
    for cmd in data:
        code = cmd["cmd"]
        params = cmd["params"]
        d: Dict[str, str | bool] = {"code": vfb2ufo_command_codes[code]}
        if code in ("AlignBottom", "AlignTop"):
            d["point"] = glyph.get_point_label(params["pt"], code)
            if code == "AlignBottom":
                zd = "ttZonesB"
            else:
                zd = "ttZonesT"
            d["zone"] = zone_names[zd][params["zone"]]
        elif code in ("AlignH", "AlignV"):
            d["point"] = glyph.get_point_label(params["pt"], code)
            if "align" in params:
                align = params["align"]
                if align > -1:
                    d["align"] = vfb2ufo_alignment_rev[align]
        elif code in (
            "SingleLinkH",
            "SingleLinkV",
            "DoubleLinkH",
            "DoubleLinkV",
        ):
            d["point1"] = glyph.get_point_label(params["pt1"], code)
            d["point2"] = glyph.get_point_label(params["pt2"], code)
            if "stem" in params:
                stem = params["stem"]
                if stem == -2:
                    d["round"] = True
                elif stem == -1:
                    pass
                else:
                    d["stem"] = tt_stem_names[stem]
            if "align" in params:
                align = params["align"]
                if align > -1:
                    d["align"] = vfb2ufo_alignment_rev[align]
        elif code in (
            "InterpolateH",
            "InterpolateV",
        ):
            d["point"] = glyph.get_point_label(params["pti"], code)
            d["point1"] = glyph.get_point_label(params["pt1"], code)
            d["point2"] = glyph.get_point_label(params["pt2"], code)
            if "align" in params:
                align = params["align"]
                if align > -1:
                    d["align"] = vfb2ufo_alignment_rev[align]
        elif code in (
            "MDeltaH",
            "MDeltaV",
            "FDeltaH",
            "FDeltaV",
        ):
            d["point"] = glyph.get_point_label(params["pt"], code)
            d["delta"] = params["shift"]
            d["ppm1"] = params["ppm1"]
            d["ppm2"] = params["ppm2"]
        else:
            logger.error(f"Unknown TT command: {code}")

        tth.append(make_tt_cmd(d))

    glyph.lib[TT_GLYPH_LIB_KEY] = (
        "  <ttProgram>\n" + "\n".join(tth) + "\n  </ttProgram>\n"
    )


def transform_stem_rounds(data: Dict[str, int], name: str) -> Dict[str, int]:
    d = {"0": 1}
    for k, v in data.items():
        key = str(v)
        val = int(k)
        if key in d:
            logger.error(
                f"Error in stem rounding settings for {name}, duplicate ppm {key}."
            )
        d[key] = val
    return d
