from __future__ import annotations

import logging
from argparse import ArgumentParser
from pathlib import Path

from vfbLib.enum import F
from vfbLib.json import save_vfb_json
from vfbLib.ufo.builder import VfbToUfoBuilder
from vfbLib.vfb.vfb import Vfb

logger = logging.getLogger(__name__)


def vfb2json():
    parser = ArgumentParser(
        description="vfb2json Converter\nCopyright (c) 2024 by LucasFonts"
    )
    parser.add_argument(
        "-d",
        "--no-decompile",
        action="store_true",
        default=False,
        help="don't decompile data, output binary in JSON",
    )
    parser.add_argument(
        "--header",
        action="store_true",
        default=False,
        help="only read the VFB header, not the actual data",
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
        "-r",
        "--roundtrip",
        action="store_true",
        default=False,
        help="roundtrip data by decompiling and compiling again before saving",
    )
    parser.add_argument(
        "-u",
        "--unicode-strings",
        action="store_true",
        default=False,
        help="interpret name strings as Unicode instead of Windows-1252",
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
        if not vfb_path.exists():
            import sys

            print(f"File not found: '{vfb_path}'", file=sys.stderr)
            sys.exit(1)

        print(parser.description)
        print(f"Reading file {vfb_path} ...")
        save_vfb_json(
            vfb_path,
            out_path=args.path[0] if args.path else None,
            only_header=args.header,
            minimal=args.minimal,
            unicode_strings=args.unicode_strings,
            no_decompile=args.no_decompile,
            roundtrip=args.roundtrip,
        )

    else:
        parser.print_help()


def vfb2ufo():
    parser = ArgumentParser(
        description="vfb3ufo Converter\nCopyright (c) 2024 by LucasFonts"
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
        "-g",
        "--keep-groups",
        action="store_true",
        default=False,
        help="don't move non-kerning groups from groups.plist to feature code",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        default=False,
        help=(
            "serialize UFO as JSON; "
            "combine with -z to write JSON without line breaks/indentation"
        ),
    )
    parser.add_argument(
        "-k",
        "--add-kerning-groups",
        action="store_true",
        default=False,
        help="add kerning groups to feature code",
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
        help="write GLIF lib 'data' section using base64",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        default=False,
        help="no display (silent mode)",
    )
    parser.add_argument(
        "-n",
        "--no-normalize",
        action="store_true",
        default=False,
        help="don't normalize the UFOs (faster)",
    )
    parser.add_argument(
        "-nops",
        "--no-postscript-hints",
        action="store_true",
        default=False,
        help="Don't output PostScript hinting",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Print debugging output",
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
    parser.add_argument(
        "-u",
        "--unicode-strings",
        action="store_true",
        default=False,
        help="interpret name table strings as Unicode instead of Windows-1252",
    )
    args = parser.parse_args()
    if args:
        vfb_path = Path(args.inputpath[0])
        if not vfb_path.exists():
            import sys

            print(f"File not found: '{vfb_path}'", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        if not args.silent:
            print(parser.description)
            print(f"Reading file {vfb_path} ...")
        vfb = Vfb(
            vfb_path,
            minimal=args.minimal,
            drop_keys={F.Encoding, F.EncodingDefault},
            unicode_strings=args.unicode_strings,
        )
        suffix = ".ufo"
        if args.zip and not args.json:
            suffix += "z"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        vfb.decompile()
        builder = VfbToUfoBuilder(
            vfb,
            minimal=args.minimal,
            base64=args.base64,
            pshints=not args.no_postscript_hints,
            add_kerning_groups=args.add_kerning_groups,
            move_groups=not args.keep_groups,
            normalize=not args.no_normalize,
        )
        builder.write(
            out_path,
            overwrite=args.force_overwrite,
            silent=args.silent,
            ufoz=args.zip,
            json=args.json,
        )
    else:
        parser.print_help()
