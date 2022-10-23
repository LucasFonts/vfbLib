import codecs
import json
from pathlib import Path
from sys import argv
from vfbLib import VFBReader

def read_vfb(vfb_path):
    reader = VFBReader(vfb_path)
    reader.read()
    # print(reader)
    out_path = Path(vfb_path).with_suffix(".json")
    with codecs.open(str(out_path), "wb", "utf-8") as f:
        json.dump(reader.data, f, ensure_ascii=False, indent=4)


def vfb3ufo():
    for arg in argv[1:]:
        read_vfb(arg)
