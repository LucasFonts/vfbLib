from __future__ import annotations

import codecs
import logging
import yaml

from argparse import ArgumentParser
from pathlib import Path
from vfbLib import VFBReader


logger = logging.getLogger(__name__)


def delta_yaml_to_human(data):
    glyphs = list(data.keys())
    r = "/" + "/".join(glyphs) + "\n\n"
    for g in glyphs:
        r += f"{g}:\n"
        deltas = []
        for d in data[g]:
            cmd = d["cmd"]
            params = d["params"]
            if cmd.startswith("F"):
                t = "F"
            else:
                t = ""
            ppms = range(params["ppm1"], params["ppm2"] + 1)
            for ppm in ppms:
                deltas.append(f"{t}{ppm}")
        r += " ".join(sorted(list(set(deltas)))) + "\n\n"
    return r


def convert_delta_yaml():
    parser = ArgumentParser(
        description=("VFB2DELTA Converter\n" "Copyright (c) 2022 by LucasFonts\n" "Build 2022-11-23")
    )
    parser.add_argument(
        "inputpath",
        type=str,
        nargs="+",
        help="input file path[s] (.tth.yaml)",
    )
    args = parser.parse_args()
    if args:
        for inputpath in args.inputpath:
            yaml_path = Path(inputpath)
            with codecs.open(yaml_path, "rb", "utf-8") as f:
                data = yaml.load(f, yaml.SafeLoader)
            if data:
                result = delta_yaml_to_human(data)
                out_path = yaml_path.with_suffix(".txt")
                with codecs.open(out_path, "wb", "utf-8") as f:
                    f.write(result)
            else:
                print(f"File {yaml_path.name} contained no data.")
    else:
        parser.print_help()


def dump_deltas():
    parser = ArgumentParser(
        description=("VFB2DELTA Converter\n" "Copyright (c) 2022 by LucasFonts\n" "Build 2022-11-23")
    )
    parser.add_argument(
        "-c",
        "--coords",
        action="store_true",
        default=False,
        help="output coordinates instead of point indices",
    )
    parser.add_argument(
        "inputpath",
        type=str,
        nargs=1,
        help="input file path (.vfb)",
    )
    args = parser.parse_args()
    master_index = 0
    if args:
        vfb_path = Path(args.inputpath[0])
        reader = VFBReader(vfb_path, only_keys=["Glyph"])
        reader.read()

        glyphs = [(k, v) for k, v in reader.data if k == "Glyph"]
        deltas = {}
        for _, v in glyphs:
            num_nodes = len(v["nodes"])
            glyph_deltas = []
            for cmd in v.get("tth", []):
                if cmd["cmd"] in ("MDeltaV", "MDeltaH", "FDeltaV", "FDeltaH"):
                    if args.coords:
                        index = cmd["params"]["pt"]
                        if num_nodes == 0:
                            # Composite
                            total_nodes = 0
                            final_index = index
                            found = False
                            for c in v["components"]:
                                gid = c["gid"]
                                _, component = glyphs[gid]
                                c_nodes = len(component["nodes"])
                                total_nodes += c_nodes
                                if index < total_nodes:
                                    found = True
                                    break
                                final_index -= c_nodes
                            if found:
                                # Resolve the coordinate with offsets
                                pt = component["nodes"][final_index]["points"][master_index][0]
                                x = pt[0] + c["offsetX"][master_index]
                                y = pt[1] + c["offsetY"][master_index]
                                # TODO: Respect scaling
                                cmd["params"]["coords"] = {"x": x, "y": y}
                            else:
                                print(f"Could not find index {index} in components.")
                                raise IndexError

                        elif index == num_nodes:
                            cmd["params"]["ref"] = "lsb"
                        elif index == num_nodes + 1:
                            cmd["params"]["ref"] = "rsb"
                        else:
                            try:
                                node = v["nodes"][index]
                            except IndexError:
                                print(v["name"], index, v["nodes"])
                                raise
                            coords = node["points"][master_index][0]
                            cmd["params"]["coords"] = dict(zip("xy", coords))
                        del cmd["params"]["pt"]
                    glyph_deltas.append(cmd)
            if glyph_deltas:
                deltas[v["name"]] = glyph_deltas

        if deltas:
            out_path = vfb_path.with_suffix(".tth.yaml")
            with codecs.open(out_path, "wb", "utf-8") as f:
                yaml.dump(deltas, f)
        else:
            print(f"{vfb_path.name}: No deltas found.")

    else:
        parser.print_help()
