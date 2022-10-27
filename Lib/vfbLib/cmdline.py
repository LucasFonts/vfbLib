import codecs
import json
from pathlib import Path
from sys import argv
from vfbLib import VFBReader


def read_vfb(vfb_path: Path) -> VFBReader:
    reader = VFBReader(vfb_path)
    reader.read()
    return reader


def write_json(reader: VFBReader, vfb_path: Path) -> None:
    out_path = vfb_path.with_suffix(".json")
    with codecs.open(str(out_path), "wb", "utf-8") as f:
        json.dump(reader.data, f, ensure_ascii=False, indent=4)


def vfb2json():
    for arg in argv[1:]:
        path = Path(arg)
        reader = read_vfb(path)
        write_json(reader, path)


def vfb2ufo():
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description=(
            "VFB3UFO Converter\n"
            "Copyright (c) 2022 by LucasFonts\n"
            "Build 2022-10-27"
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
    args = parser.parse_args()
    if args:
        reader = read_vfb(Path(args.inputpath))
    else:
        parser.print_help()
