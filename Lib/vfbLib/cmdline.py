from __future__ import annotations

import codecs
import json
import logging

from argparse import ArgumentParser
from pathlib import Path
from vfbLib import VFBReader
from vfbLib.ufo import VfbToUfoWriter
from vfbLib.version import build_date


logger = logging.getLogger(__name__)


def read_vfb(vfb_path: Path, minimal=False) -> VFBReader:
    reader = VFBReader(vfb_path, minimal=minimal)
    reader.read()
    return reader


def write_json(reader: VFBReader, json_path: Path) -> None:
    with codecs.open(str(json_path), "wb", "utf-8") as f:
        json.dump(reader.data, f, ensure_ascii=False, indent=4)


def vfb2json():
    parser = ArgumentParser(
        description=(
            f"VFB2JSON Converter\nCopyright (c) 2022 by LucasFonts\nBuild {build_date}"
        )
    )
    parser.add_argument(
        "-m",
        "--minimal",
        action="store_true",
        default=False,
        help="parse only minimal amount of data",
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
        reader = read_vfb(vfb_path, minimal=args.minimal)
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(".json")
        else:
            out_path = vfb_path.with_suffix(".json")
        write_json(reader, out_path)
    else:
        parser.print_help()


def vfb2ufo():
    parser = ArgumentParser(
        description=(
            f"VFB3UFO Converter\nCopyright (c) 2022 by LucasFonts\nBuild {build_date}"
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
        "-fo",
        "--force-overwrite",
        action="store_true",
        default=False,
        help="force overwrite",
    )
    parser.add_argument(
        "-ttx",
        "--ttx",
        action="store_true",
        default=False,
        help="convert binary OpenType Layout data using TTX-like format",
    )
    parser.add_argument(
        "-64",
        "--base64",
        action="store_true",
        default=False,
        help="write GLIF lib 'data' section using base64 (recommended)",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        default=False,
        help="no display (silent mode)",
    )
    parser.add_argument(
        "-nops",
        "--no-postscript-hints",
        action="store_true",
        default=False,
        help="Don't output PostScript hinting",
    )
    parser.add_argument(
        "-z",
        "--zip",
        action="store_true",
        default=False,
        help="write UFOZ (compressed UFO)",
    )
    parser.add_argument(
        "inputpath",
        type=str,
        nargs=1,
        help="input file path (.vfb)",
    )
    parser.add_argument(
        "outputpath",
        type=str,
        nargs="?",
        help="output file path (.ufo[z])",
    )
    parser.add_argument(
        "-m",
        "--minimal",
        action="store_true",
        default=False,
        help="parse only minimal amount of data, drop missing glyphs from groups, etc.",
    )
    args = parser.parse_args()
    if args:
        vfb_path = Path(args.inputpath[0])
        if not args.silent:
            print(parser.description)
            print(f"Reading file {vfb_path} ...")
        reader = read_vfb(vfb_path, minimal=args.minimal)
        suffix = ".ufo"
        # if args.zip:
        #     suffix += "z"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        writer = VfbToUfoWriter(
            reader.data,
            minimal=args.minimal,
            base64=args.base64,
            pshints=not args.no_postscript_hints,
        )
        writer.write(
            out_path,
            overwrite=args.force_overwrite,
            silent=args.silent,
            ufoz=False,  # FIXME
        )
    else:
        parser.print_help()
