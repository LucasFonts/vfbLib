from __future__ import annotations

from pathlib import Path

import orjson

from vfbLib.vfb.vfb import Vfb


def save_vfb_json(
    vfb_path: Path,
    out_path: Path | None = None,
    only_header: bool = False,
    minimal: bool = False,
    unicode_strings: bool = False,
    no_decompile: bool = False,
    roundtrip: bool = False,
) -> None:
    vfb = Vfb(
        vfb_path,
        only_header=only_header,
        minimal=minimal,
        unicode_strings=unicode_strings,
    )
    if roundtrip:
        vfb.decompile()
        vfb.compile()

    if not no_decompile:
        vfb.decompile()

    suffix = ".vfb.json"
    if out_path:
        out_path = (Path(out_path) / vfb_path.name).with_suffix(suffix)
    else:
        out_path = vfb_path.with_suffix(suffix)
    with open(str(out_path), "wb") as f:
        f.write(
            orjson.dumps(
                vfb.as_dict(), option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS
            )
        )
