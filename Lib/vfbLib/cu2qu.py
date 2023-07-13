from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from vfbLib.version import build_date
from vfbLib.vfb.vfb import Vfb


def to_quadratic_mm(vfb) -> None:
    """Convert a multiple master VFB to quadratic. The object is modified in place.

    Args:
        vfb (Vfb): The VFB object.
    """
    pass


def to_quadratic_single(vfb) -> None:
    """Convert a single master VFB to quadratic. The object is modified in place.

    Args:
        vfb (Vfb): The VFB object.
    """
    pass


def vfbcu2qu():
    parser = ArgumentParser(
        description=(
            "VFB Cubic to Quadratic Converter\nCopyright (c) 2023 by LucasFonts\n"
            f"Build {build_date}"
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
        "inputpath",
        type=str,
        nargs=1,
        help="input file path (.vfb)",
    )
    parser.add_argument(
        "outputpath",
        type=str,
        nargs="?",
        help="output file path (.vfb)",
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
        print(parser.description)
        print(f"Reading file {vfb_path} ...")
        vfb = Vfb(vfb_path, minimal=args.minimal)
        if vfb.num_masters == 1:
            to_quadratic_single(vfb)
        elif vfb.num_masters > 1:
            to_quadratic_mm(vfb)
        else:
            print(f"Unsupported number of masters: {vfb.num_masters}")
            return

        suffix = ".qu.vfb"
        if args.path:
            out_path = (Path(args.path[0]) / vfb_path.name).with_suffix(suffix)
        else:
            out_path = vfb_path.with_suffix(suffix)
        if out_path.exists():
            if not args.force_overwrite:
                print(
                    "Output file exists, new file was not saved. "
                    "Use -fo to force overwriting."
                )
                return

        print(f"Saving converted file to {out_path}.")
        vfb.write(out_path)
    else:
        parser.print_help()
