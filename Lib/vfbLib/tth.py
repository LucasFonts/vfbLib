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
        suffix = ".vfb.json"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        with codecs.open(str(out_path), "wb", "utf-8") as f:
            json.dump(extract_truetype_hinting(vfb), f, ensure_ascii=False, indent=4)
    else:
        parser.print_help()


def extract_truetype_hinting(vfb: Vfb) -> dict[str, Any]:
    d = {}
    stem_round = {"ttStemsV": {}, "ttStemsH": {}}
    for entry in vfb.entries:
        key = entry.key
        if key == "Gasp Ranges":
            entry.decompile()
            assert isinstance(entry.decompiled, list)
            d["gasp"] = {
                gasp_range["maxPpem"]: gasp_range["flags"]
                for gasp_range in entry.decompiled
            }

        elif key == "TrueType Info":
            entry.decompile()
            assert isinstance(entry.decompiled, list)
            for k, v in entry.decompiled:
                if k == "lowest_rec_ppem":
                    d["lowest_rec_ppem"] = v
                if k == "units_per_em":
                    d["units_per_em"] = v

        elif key == "TrueType Stem PPEMs":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            for direction in ("ttStemsV", "ttStemsH"):
                if direction in entry.decompiled:
                    direction_data = entry.decompiled[direction]
                    for stem_data in direction_data:
                        stem_round[direction][stem_data["stem"]] = deepcopy(
                            stem_data["round"]
                        )

        elif key == "TrueType Stems":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            d["stems"] = deepcopy(entry.decompiled)

        elif key == "TrueType Stem PPEMs 1":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            for direction in ("ttStemsV", "ttStemsH"):
                if direction in entry.decompiled:
                    direction_data = entry.decompiled[direction]
                    for stem_data in direction_data:
                        stem_index = stem_data["stem"]
                        stem_round[direction][stem_index]["1"] = stem_data["round"]["1"]

        elif key == "TrueType Zones":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            d["zones"] = deepcopy(entry.decompiled)

        elif key == "Pixel Snap":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            d["pixel_snap"] = entry.decompiled

        elif key == "Zone Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            d["zone_ppm"] = entry.decompiled

        elif key == "Code Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            d["code_ppm"] = entry.decompiled

        elif key == "TrueType Zone Deltas":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            d["zone_deltas"] = deepcopy(entry.decompiled)

        elif key == "TrueType Info":
            entry.decompile()
            assert isinstance(entry.decompiled, list)
            for k, v in entry.decompiled:
                if k == "lowest_rec_ppem":
                    d["lowest_rec_ppem"] = v
                if k == "units_per_em":
                    d["units_per_em"] = v

    # Merge stem information
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in stem_round:
            direction_data = stem_round[direction]
            for stem_index, rounding in direction_data.items():
                stem = d["stems"][direction][stem_index]
                stem["round"].update(rounding)

    return d
