import codecs
import json
import logging
from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from sys import exit
from typing import Any

from vfbLib.ufo.glyph import IndexVfbToUfoGlyph
from vfbLib.ufo.tth import TTGlyphHints, transform_stem_rounds
from vfbLib.version import build_date
from vfbLib.vfb.vfb import Vfb

logger = logging.getLogger(__name__)


def vfb2tth():
    parser = ArgumentParser(
        description=(
            f"VFB2TTH Converter\nCopyright (c) 2024 by LucasFonts\nBuild {build_date}"
        )
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="json",
        help="The output format: json (default), toml, or yaml",
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
        suffix = f".tth.{args.format}"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        data = extract_truetype_hinting(vfb)
        if args.format == "toml":
            import tomli_w

            with open(out_path, "wb") as f:
                tomli_w.dump(data, f)
        elif args.format == "yaml":
            import yaml

            with codecs.open(str(out_path), "wb", "utf-8") as f:
                yaml.dump(data, f, sort_keys=True, indent=2)
        else:
            with codecs.open(str(out_path), "wb", "utf-8") as f:
                json.dump(
                    data,
                    f,
                    ensure_ascii=False,
                    indent=4,
                    sort_keys=True,
                )
        if vfb.any_errors:
            exit("There were decompilation errors.")
    else:
        parser.print_help()
        exit(2)


def extract_truetype_hinting(vfb: Vfb) -> dict[str, Any]:
    font: dict[str, Any] = {}
    glyphs: dict[str, list[dict]] = {}
    zone_names: dict[str, dict] = {"ttZonesT": {}, "ttZonesB": {}}
    d: dict[str, Any] = {"font": font, "glyphs": glyphs}
    stem_round: dict[str, dict] = {"ttStemsV": {}, "ttStemsH": {}}
    for entry in vfb.entries:
        key = entry.key
        if key == "Gasp Ranges":
            entry.decompile()
            assert isinstance(entry.decompiled, list)
            font["gasp"] = {
                str(gasp_range["maxPpem"]): gasp_range["flags"]
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
            extract_tt_stems(entry.decompiled, font)

        elif key == "TrueType Stem PPEMs 1":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_tt_stem_ppem_1(entry.decompiled, stem_round)

        elif key == "TrueType Zones":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_tt_zones(entry.decompiled, font, zone_names)

        elif key == "Pixel Snap":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["stemsnaplimit"] = entry.decompiled

        elif key == "Zone Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["zoneppm"] = entry.decompiled

        elif key == "Code Stop PPEM":
            entry.decompile()
            assert isinstance(entry.decompiled, int)
            font["codeppm"] = entry.decompiled

        elif key == "TrueType Zone Deltas":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_tt_zone_deltas(entry.decompiled, font)

        elif key == "Glyph":
            entry.decompile()
            assert isinstance(entry.decompiled, dict)
            extract_glyph_hints(entry.decompiled, glyphs, font, zone_names)

    merge_stem_information(stem_round, font)
    merge_zone_information(font)

    return d


def extract_glyph_hints(
    data: dict, target: dict, font_hints: dict, zone_names: dict
) -> None:
    if tth := data.get("tth"):
        ttg = TTGlyphHints(
            IndexVfbToUfoGlyph(),
            data=tth,
            zone_names=zone_names,
            stems=font_hints["stems"],
        )
        tr = ttg.get_tt_glyph_hints()
        target[data["name"]] = tr


def extract_tt_stem_ppem_1(data: dict, target: dict) -> None:
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in data:
            direction_data = data[direction]
            for stem_data in direction_data:
                stem_index = stem_data["stem"]
                target[direction][stem_index]["1"] = stem_data["round"]["1"]


def extract_tt_stem_ppems(data: dict, target: dict) -> None:
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in data:
            direction_data = data[direction]
            for stem_data in direction_data:
                target[direction][stem_data["stem"]] = deepcopy(stem_data["round"])


def extract_tt_stems(data: dict, target: dict) -> None:
    target["stems"] = {"ttStemsV": [], "ttStemsH": []}
    stem_names = set()
    for direction in ("ttStemsV", "ttStemsH"):
        for stem in data.get(direction, []):
            name = stem["name"]
            i = 1
            # Make stem names unique
            if name in stem_names:
                print(f"Duplicate stem name: {name}")
                while f"{name}#{i}" in stem_names:
                    i += 1
                name = f"{name}#{i}"
            stem_names |= {name}
            target["stems"][direction].append(
                {
                    "name": name,
                    "round": deepcopy(stem["round"]),
                    "width": stem["value"],
                    "horizontal": direction == "ttStemsV",
                }
            )


def extract_tt_zone_deltas(data: dict, target: dict):
    target["zone_deltas"] = deepcopy(data)


def extract_tt_zones(data: dict, target: dict, zone_names: dict) -> None:
    target["zones"] = {"ttZonesT": [], "ttZonesB": []}
    zone_names_global = set()
    for side in ("ttZonesT", "ttZonesB"):
        for zone_index, zone in enumerate(data.get(side, [])):
            name = zone["name"]
            i = 1
            # Make zone names unique
            if name in zone_names_global:
                print(f"Duplicate zone name: {name}")
                while f"{name}#{i}" in zone_names_global:
                    i += 1
                name = f"{name}#{i}"
            zone_names_global |= {name}
            zone_names[side][zone_index] = name
            target["zones"][side].append(
                {
                    "name": name,
                    "position": zone["position"],
                    "top": side == "ttZonesT",
                    "width": zone["value"],
                }
            )


def merge_stem_information(data, font):
    # Merge stem information
    stems_dict = {}
    for direction in ("ttStemsV", "ttStemsH"):
        if direction in data:
            direction_data = data[direction]
            for stem_index, rounding in direction_data.items():
                stem = font["stems"][direction][stem_index]
                stem["round"].update(rounding)
                # Sort the rounding dict by value (px)
                rd = transform_stem_rounds(stem["round"], stem["name"])
                srtl = sorted(rd.items(), key=lambda item: item[1])
                srd = {k: v for k, v in srtl}
                stem["round"] = srd
                stems_dict[stem["name"]] = deepcopy(stem)
                del stems_dict[stem["name"]]["name"]
    if stems_dict:
        font["stems"] = stems_dict
    else:
        del font["stems"]


def merge_zone_information(font):
    # Merge zone information
    all_zones = []
    for side in ("ttZonesB", "ttZonesT"):
        for zone in font["zones"].get(side, []):
            all_zones.append(zone)
    for zone_index, zone_delta in font.get("zone_deltas", {}).items():
        zone = all_zones[zone_index]
        # Sort and convert delta ppm to str
        zone["deltas"] = {str(k): v for k, v in sorted(zone_delta.items())}

    zones_dict = {}
    for zone in all_zones:
        zones_dict[zone["name"]] = deepcopy(zone)
        del zones_dict[zone["name"]]["name"]
    if zones_dict:
        font["zones"] = zones_dict
    else:
        del font["zones"]
    del font["zone_deltas"]
