from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Any, Dict, List
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.vfb2ufo import (
    TT_GLYPH_LIB_KEY,
    vfb2ufo_alignment_rev,
    vfb2ufo_command_codes,
)

if TYPE_CHECKING:
    from vfbLib.ufo.typing import TUfoStemsDict


logger = logging.getLogger(__name__)


def get_xml_tth(commands) -> List[str]:
    """
    Convert the glyph's list of TTH commands to a list of TTH command xml strings.
    """
    return [tt_cmd_dict_to_xml(cmd_dict) for cmd_dict in commands]


def set_tth_lib(glyph, commands) -> None:
    """
    Save the TTH commands to the glyph's lib. Optionally rename the hinted points.
    """
    tth = get_xml_tth(commands)
    if tth:
        glyph.lib[TT_GLYPH_LIB_KEY] = (
            "  <ttProgram>\n" + "\n".join(tth) + "\n  </ttProgram>\n"
        )


def tt_cmd_dict_to_xml(tt_dict: Dict[str, Any]) -> str:
    """
    Convert the dict tt command into a FontLab XML string.
    """
    code = tt_dict["code"]
    cmd = f'    <ttc code="{code}"'
    for attr in (
        "point",
        "point1",
        "point2",
        "round",
        "stem",
        "zone",
        "align",
        "delta",
        "ppm1",
        "ppm2",
    ):
        if attr in tt_dict:
            if attr == "round":
                val = str(tt_dict[attr]).lower()
            else:
                val = tt_dict[attr]
            cmd += f' {attr}="{val}"'
    cmd += "/>"
    return cmd


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


class TTGlyphHints:
    def __init__(
        self,
        mm_glyph: VfbToUfoGlyph,
        data: List[Dict[str, Any]],
        zone_names: Dict[str, List[str]],
        stems: TUfoStemsDict,
    ) -> None:
        self.glyph: VfbToUfoGlyph = mm_glyph
        self.data = data
        self.zone_names = zone_names
        self.stems = stems

    def get_tt_glyph_hints(self) -> List[Dict[str, str | bool]]:
        # Build TT hints which into glyph lib and return them.
        commands: List[Dict[str, str | bool]] = []
        for cmd in self.data:
            code = cmd["cmd"]
            params = cmd["params"]
            d: Dict[str, str | bool] = {"code": vfb2ufo_command_codes[code]}
            if code in ("AlignBottom", "AlignTop"):
                d["point"] = self.glyph.get_point_label(params["pt"], code)
                if code == "AlignBottom":
                    zd = "ttZonesB"
                else:
                    zd = "ttZonesT"
                d["zone"] = self.zone_names[zd][params["zone"]]
            elif code in ("AlignH", "AlignV"):
                d["point"] = self.glyph.get_point_label(params["pt"], code)
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev.get(align, "round")
            elif code in (
                "SingleLinkH",
                "SingleLinkV",
                "DoubleLinkH",
                "DoubleLinkV",
            ):
                d["point1"] = self.glyph.get_point_label(params["pt1"], code)
                d["point2"] = self.glyph.get_point_label(params["pt2"], code)
                if "stem" in params:
                    stem = params["stem"]
                    if stem <= -2:
                        d["round"] = True
                    elif stem == -1:
                        pass
                    else:
                        stem_dir = "ttStemsH" if code.endswith("H") else "ttStemsV"
                        if stem >= len(self.stems[stem_dir]):
                            logger.warning(
                                f"Stem index in {stem_dir} out of range in "
                                f"{self.glyph.name}: {stem} (of "
                                f"{len(self.stems[stem_dir])} existing stems). "
                                "Choosing first stem."
                            )
                            logger.warning(f"{code}: {params}")
                            logger.warning(self.stems[stem_dir])
                            stem = 0
                        d["stem"] = self.stems[stem_dir][stem]["name"]
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev.get(align, "round")
            elif code in (
                "InterpolateH",
                "InterpolateV",
            ):
                d["point"] = self.glyph.get_point_label(params["pti"], code)
                d["point1"] = self.glyph.get_point_label(params["pt1"], code)
                d["point2"] = self.glyph.get_point_label(params["pt2"], code)
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev.get(align, "round")
            elif code in (
                "MDeltaH",
                "MDeltaV",
                "FDeltaH",
                "FDeltaV",
            ):
                d["point"] = self.glyph.get_point_label(params["pt"], code)
                d["delta"] = params["shift"]
                d["ppm1"] = params["ppm1"]
                d["ppm2"] = params["ppm2"]
            else:
                logger.error(f"Unknown TT command: {code}")
                raise ValueError

            commands.append(d)
        return commands
