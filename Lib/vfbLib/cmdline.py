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
