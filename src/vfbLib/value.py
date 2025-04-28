from __future__ import annotations

from argparse import ArgumentParser
from io import BytesIO

from vfbLib.compilers.value import write_value
from vfbLib.helpers import deHexStr, hexStr
from vfbLib.parsers.value import read_value


def yuri():
    """
    Command line interface for encoding or decoding the value format used in the VFB.

    The encoded format is identical to the one used in Type 1 font charstring number
    encoding.
    """
    parser = ArgumentParser(description="vfbtool\nCopyright (c) 2024 by LucasFonts")
    parser.add_argument(
        "-e",
        "--encode",
        action="store_true",
        default=False,
        help="Encode value instead of decoding",
    )
    parser.add_argument(
        "-l",
        "--long",
        action="store_true",
        default=False,
        help="Output longest notation when encoding",
    )
    parser.add_argument(
        "-s",
        "--signed",
        action="store_true",
        default=False,
        help="Treat value as signed",
    )
    parser.add_argument(
        "hexstring",
        type=str,
        nargs="+",
        help="Input hex string",
    )
    args = parser.parse_args()
    if args:
        if args.encode:
            stream = BytesIO()
            for value in args.hexstring:
                write_value(int(value), stream, args.signed)
            print(hexStr(stream.getvalue()))
        else:
            data = deHexStr("".join(args.hexstring))
            stream = BytesIO(data)
            while True:
                try:
                    print(read_value(stream, args.signed))
                except EOFError:
                    break

    else:
        parser.print_help()
