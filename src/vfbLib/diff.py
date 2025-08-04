from __future__ import annotations

import codecs
import logging
from argparse import ArgumentParser
from difflib import HtmlDiff, unified_diff
from pathlib import Path

import orjson

from vfbLib.vfb.vfb import Vfb

logger = logging.getLogger(__name__)


def diffvfb():
    parser = ArgumentParser(description="vfbdiff\nCopyright (c) 2024 by LucasFonts")
    parser.add_argument(
        "--html",
        type=str,
        help="Output diff in HTML format to file path",
    )
    parser.add_argument(
        "file1",
        type=str,
        nargs=1,
        help="First input file path (.vfb)",
    )
    parser.add_argument(
        "file2",
        type=str,
        nargs=1,
        help="Second input file path (.vfb)",
    )
    args = parser.parse_args()
    if not args:
        parser.print_help()
        return

    vfb1_path = Path(args.file1[0])
    vfb2_path = Path(args.file2[0])

    vfb1 = Vfb(vfb_path=vfb1_path, timing=False)
    vfb2 = Vfb(vfb_path=vfb2_path, timing=False)
    vfb1.read()
    vfb2.read()
    vfb1.decompile()
    vfb2.decompile()
    vfb1_str = orjson.dumps(
        vfb1.as_dict(),
        option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS,
    ).splitlines()
    vfb2_str = orjson.dumps(
        vfb2.as_dict(),
        option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS,
    ).splitlines()
    if args.html:
        html_diff = HtmlDiff()
        html = html_diff.make_file(
            str(vfb1_str),
            str(vfb2_str),
            str(vfb1_path),
            str(vfb2_path),
            context=True,
            numlines=5,
        )
        with codecs.open(args.html, "wb", "utf-8") as f:
            f.write(html)
    else:
        d = unified_diff(vfb1_str, vfb2_str, str(vfb1_path), str(vfb2_path))
        for line in d:
            print(line)
