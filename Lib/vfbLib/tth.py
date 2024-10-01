import codecs
import json
import logging

from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from vfbLib.version import build_date
from vfbLib.vfb.vfb import Vfb

from typing import Any


logger = logging.getLogger(__name__)


def vfb2tth():
    parser = ArgumentParser(
        description=(
            f"VFB2TTH Converter\nCopyright (c) 2024 by LucasFonts\nBuild {build_date}"
        )
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        nargs=1,
        help="output folder",
    )
    parser.add_argument(
        "inputpath",
        type=str,
        nargs=1,
        help="input file path (.vfb)",
    )
    args = parser.parse_args()
    if args:
        vfb_path = Path(args.inputpath[0])
        print(parser.description)
        print(f"Reading file {vfb_path} ...")
        vfb = Vfb(
            vfb_path,
            only_header=False,
            minimal=True,
            unicode_strings=True,
        )
        # vfb.decompile()
        suffix = ".tth.json"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        with codecs.open(str(out_path), "wb", "utf-8") as f:
            json.dump(
                extract_truetype_hinting(vfb),
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
            )
    else:
        parser.print_help()


def extract_truetype_hinting(vfb: Vfb) -> dict[str, Any]:
    font = {}
    glyphs = {}
    d: dict[str, Any] = {"font": font, "glyphs": glyphs}
    stem_round = {"ttStemsV": {}, "ttStemsH": {}}
    for entry in vfb.entries:
        key = entry.key
        if key == "Gasp Ranges":
            entry.decompile()
            assert isinstance(entry.decompiled, list)
            font["gasp"] = {
                gasp_range["maxPpem"]: gasp_range["flags"]
                for gasp_range in entry.decompiled
            }

        elif key == "TrueType Info":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            for k in ("lowest_rec_ppem", "units_per_em"):
                if k in entry.decompiled:
                    font[k] = entry.decompiled[k]

        elif key == "TrueType Stem PPEMs":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_tt_stem_ppems(entry.decompiled, stem_round)

        elif key == "TrueType Stems":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            font["stems"] = deepcopy(entry.decompiled)

        elif key == "TrueType Stem PPEMs 1":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_tt_stem_ppem_1(entry.decompiled, stem_round)

        elif key == "TrueType Zones":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            font["zones"] = deepcopy(entry.decompiled)

        elif key == "Pixel Snap":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["pixel_snap"] = entry.decompiled

        elif key == "Zone Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["zone_ppm"] = entry.decompiled

        elif key == "Code Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["code_ppm"] = entry.decompiled

        elif key == "TrueType Zone Deltas":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            font["zone_deltas"] = deepcopy(entry.decompiled)

        elif key == "Glyph":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_glyph_hints(entry.decompiled, glyphs)

    # Merge stem information
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in stem_round:
            direction_data = stem_round[direction]
            for stem_index, rounding in direction_data.items():
                stem = font["stems"][direction][stem_index]
                stem["round"].update(rounding)

    return d


def extract_glyph_hints(data: dict, target: dict) -> None:
    if tth := data.get("tth"):
        target[data["name"]] = deepcopy(tth)


def extract_tt_stem_ppems(data: dict, target: dict) -> None:
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in data:
            direction_data = data[direction]
            for stem_data in direction_data:
                target[direction][stem_data["stem"]] = deepcopy(stem_data["round"])


def extract_tt_stem_ppem_1(data: dict, target: dict) -> None:
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in data:
            direction_data = data[direction]
            for stem_data in direction_data:
                stem_index = stem_data["stem"]
                target[direction][stem_index]["1"] = stem_data["round"]["1"]
