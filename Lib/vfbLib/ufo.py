from defcon import Font
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal


def normalize_ufo(
    filepath: Path, structure: Literal["package", "zip"] = "package"
) -> None:
    try:
        f = Font(filepath)
    except:
        print(f"Skipping UFO with errors: {filepath}")
        raise

    with NamedTemporaryFile(suffix="ufoz") as tf:
        f.save(path=tf.name, formatVersion=3, structure="zip")
        f = Font(tf.name)
        # for glyph in f:
        #     for key in delete_lib_keys:
        #         try:
        #             del glyph.lib[key]
        #         except KeyError:
        #             pass
        #     # Make FL glyph programs readable
        #     if "com.fontlab.ttprogram" in glyph.lib:
        #         data = glyph.lib["com.fontlab.ttprogram"]
        #         try:
        #             data = data.decode()
        #         except AttributeError:
        #             pass
        #         glyph.lib["com.fontlab.ttprogram"] = data
        if structure == "zip":
            if not filepath.suffix == ".ufoz":
                filepath = filepath.with_suffix(".ufoz")
        else:
            if filepath.suffix == ".ufoz":
                filepath = filepath.with_suffix(".ufo")
        f.save(path=filepath, formatVersion=3, structure=structure)


def normalize_ufoz(filepath):
    """
    Normalize the ufo, but save as .ufoz
    """
    normalize_ufo(filepath, structure="zip")


def normalize():
    from sys import argv

    for ufo_path in argv[1:]:
        normalize_ufo(Path(ufo_path))
