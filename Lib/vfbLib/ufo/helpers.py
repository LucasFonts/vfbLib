import codecs

from defcon import Font
from ufonormalizer import normalizeUFO
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal


delete_lib_keys = []


def fix_vfb2ufo_feature_encoding(ufo_path: Path) -> None:
    # Read vfb2ufo's Windows-1252-encoded feature file and convert to UTF-8
    fea_path = ufo_path / "features.fea"
    if not fea_path.exists():
        # UFOs may omit the fea file
        return

    with codecs.open(str(fea_path), "rb", "windows-1252") as f:
        fea = f.read()
    with codecs.open(str(fea_path), "wb", "utf-8") as f:
        f.write(fea)


def normalize_ufo(
    filepath: Path, structure: Literal["package", "zip"] = "package"
) -> None:
    print(f"Processing {filepath.name}...")

    normalized_file = filepath / ".normalized"

    if structure == "package":

        if normalized_file.exists():
            print(f"    Skipping already normalized UFO: {filepath.name}")
            return

        fix_vfb2ufo_feature_encoding(filepath)  # FIXME: Support ufoz

    try:
        f = Font(filepath)
    except:
        print(f"Skipping UFO with errors: {filepath}")
        raise

    with NamedTemporaryFile(suffix="ufoz") as tf:
        f.save(path=tf.name, formatVersion=3, structure="zip")
        f = Font(tf.name)
        for glyph in f:
            for key in delete_lib_keys:
                try:
                    del glyph.lib[key]
                except KeyError:
                    pass
            # Make glyph data readable
            for k in ("com.fontlab.ttprogram", "com.adobe.type.autohint"):
                if k in glyph.lib:
                    data = glyph.lib[k]
                    try:
                        data = data.decode()
                    except AttributeError:
                        pass
                    glyph.lib[k] = data

        if structure == "zip":
            if not filepath.suffix == ".ufoz":
                filepath = filepath.with_suffix(".ufoz")
        else:
            if filepath.suffix == ".ufoz":
                filepath = filepath.with_suffix(".ufo")
        f.save(path=filepath, formatVersion=3, structure=structure)
        normalizeUFO(ufoPath=filepath, onlyModified=False)
        if structure == "package":
            normalized_file.touch()


def normalize_ufoz(filepath):
    """
    Normalize the ufo, but save as .ufoz
    """
    normalize_ufo(filepath, structure="zip")


def normalize():
    from sys import argv

    for ufo_path in argv[1:]:
        normalize_ufo(Path(ufo_path))
