from __future__ import annotations

import logging

from fontTools.ufoLib import UFOFileStructure, UFOWriter
from fontTools.ufoLib.glifLib import GlyphSet
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING, Any, Dict, List, Tuple
from ufonormalizer import normalizeUFO
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.groups import transform_groups
from vfbLib.ufo.guides import apply_guide_properties, get_master_guides
from vfbLib.ufo.info import VfbToUfoInfo
from vfbLib.ufo.kerning import UfoKerning
from vfbLib.ufo.paths import UfoMasterGlyph
from vfbLib.ufo.tth import TTGlyphHints, transform_stem_rounds
from vfbLib.ufo.typing import (
    TUfoStemPPMsDict,
    TUfoStemsDict,
    TUfoTTZoneDict,
    TUfoTTZonesDict,
)
from vfbLib.ufo.vfb2ufo import TT_GLYPH_LIB_KEY, TT_LIB_KEY

if TYPE_CHECKING:
    from vfbLib.typing import Anchor, ClassFlagDict, GuidePropertyList
    from vfbLib.ufo.typing import UfoGroups, UfoMMKerning


logger = logging.getLogger(__name__)


class VfbToUfoWriter:
    def __init__(
        self,
        json: List[List[Any]],
        minimal=False,
        base64=False,
        pshints=True,
    ) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.minimal = minimal
        self.encode_data_base64 = base64
        self.include_ps_hints = pshints

        self.features_classes = ""
        self.features = ""
        self.groups: UfoGroups = {}
        self.guide_properties: GuidePropertyList = []
        self.info = VfbToUfoInfo()
        self.kerning_class_flags: ClassFlagDict = {}
        self.num_blue_values = 0
        self.num_other_blues = 0
        self.num_family_blues = 0
        self.num_family_other_blues = 0
        self.num_stem_snap_h = 0
        self.num_stem_snap_v = 0
        self.mm_guides = None
        self.mm_kerning: UfoMMKerning = {}
        self.kerning: Dict[Tuple[str, str], int] = {}
        self.lib: Dict[str, Any] = {}
        self.masters: List[str] = []
        self.masters_1505: List[Any] = []
        self.masters_ps_info: List[Dict] = []
        self.current_glyph: VfbToUfoGlyph | None = None
        self.glyph_masters: Dict[str, VfbToUfoGlyph] = {}
        self.glyphOrder: List[str] = []
        # TT
        self.stem_ppms: TUfoStemPPMsDict = {"ttStemsH": [], "ttStemsV": []}
        self.stems: TUfoStemsDict = {"ttStemsH": [], "ttStemsV": []}
        self.tt_zones: TUfoTTZonesDict = {}
        self.tt_zone_names: List[str] = []
        self.zone_names: Dict[str, List[str]] = {}
        self.build()

    def add_ot_class(self, data: str) -> None:
        if ":" not in data:
            logger.warning(f"Malformed OT class definition, skipping: {data}")
            return

        parts = data.split(":", 1)
        name: str = parts[0]
        glyphs_str: str = parts[1]
        name = name.strip()

        is_kerning = name.startswith("_")

        if name in self.groups:
            logger.warning(f"Duplicate OT class name, skipping: {name}")
            return

        glyphs_list = glyphs_str.split()

        if is_kerning:
            # Reorganize glyphs so that the "keyglyph" is first
            glyphs: List[str] = [g.strip() for g in glyphs_list if not g.endswith("'")]
            keyglyphs = [g.strip() for g in glyphs_list if g.endswith("'")]
            keyglyphs = [k.strip("'") for k in keyglyphs]
            if len(keyglyphs) != 1:
                logger.warning(
                    f"Unexpected number of key glyphs in group {name}: {keyglyphs}"
                )
            else:
                glyphs.insert(0, *keyglyphs)

        else:
            glyphs = [g.strip() for g in glyphs_list]
        self.groups[name] = glyphs
        # Also add non-kerning classes to the feature code
        if not is_kerning and not name.startswith("."):
            self.features_classes += f"@{name} = [{' '.join(glyphs)}];\n"

    def assure_tt_lib(self) -> None:
        if TT_LIB_KEY not in self.lib:
            self.lib[TT_LIB_KEY] = {}

    def assure_tt_glyphlib(self) -> None:
        if TT_GLYPH_LIB_KEY not in self.lib:
            self.lib[TT_GLYPH_LIB_KEY] = {}

    def build_mm_glyph(self, data: Dict[str, Any]) -> None:
        g = self.current_glyph = VfbToUfoGlyph()
        g.lib = {}
        g.name = data["name"]
        g.unicodes = []

        # MM Stuff, need to extract later
        if not self.minimal and "guides" in data:
            g.mm_guides = data["guides"]

        if self.include_ps_hints and "hints" in data:
            g.mm_hints = data["hints"]
            if "hintmasks" in data["hints"]:
                g.hintmasks = data["hints"]["hintmasks"]
                del data["hints"]["hintmasks"]

        if "kerning" in data:
            kerning: Dict[int, List[int]] = data["kerning"]
            for Rid, values in kerning.items():
                self.mm_kerning[(g.name, Rid)] = values

        g.mm_metrics = data["metrics"]  # width and height
        g.mm_nodes = data["nodes"]

        if "components" in data:
            g.mm_components = data["components"]

        # TrueType hinting, needs to come after mm_nodes, because it needs
        # access to the point indices.
        if "tth" in data:
            tth = TTGlyphHints(g, data["tth"], self.zone_names, self.stems)
            g.tth_commands = tth.commands
            del tth

    def set_glyph_background(self, data: Dict[str, Any]) -> None:
        assert self.current_glyph is not None
        self.current_glyph.lib["com.fontlab.v5.background"] = data

    def set_tt_stem_ppms(self, data: Dict[str, List[Dict[str, Any]]]) -> None:
        for d in ("ttStemsH", "ttStemsV"):
            direction_stems = data[d]
            for ds in direction_stems:
                rounds = transform_stem_rounds(ds["round"], d)
                stem = {
                    "index": ds["stem"],
                    "round": rounds,
                }
                self.stem_ppms[d].append(stem)

    def set_tt_stems(self, data) -> None:
        for d in ("ttStemsH", "ttStemsV"):
            direction_stems = data[d]
            for i, ds in enumerate(direction_stems):
                r = ds["round"]
                rk = list(r.keys())[0]
                rv = str(r[rk])
                stem_ppms = self.stem_ppms[d][i]
                assert i == stem_ppms["index"]
                stem = {
                    "horizontal": d == "ttStemsV",
                    "width": ds["value"],
                    "name": ds["name"],
                    "round": stem_ppms["round"],
                }
                if rv in stem["round"]:
                    logger.error(
                        f"Error in stem rounding settings for {d}, duplicate ppm {rv}."
                    )
                stem["round"][rv] = int(rk)
                self.stems[d].append(stem)

    def set_tt_zones(self, data: Dict[str, List]) -> None:
        self.zone_names = {
            "ttZonesT": [],
            "ttZonesB": [],
        }
        for d in ("ttZonesB", "ttZonesT"):
            direction_zones = data[d]
            for dz in direction_zones:
                zone = TUfoTTZoneDict(
                    position=dz["position"],
                    top=d == "ttZonesT",
                    width=dz["value"],
                )
                name = dz["name"]
                if name in self.tt_zones:
                    logger.warning(f"Duplicate zone name: {name}, overwriting.")
                self.tt_zones[name] = zone
                self.tt_zone_names.append(name)  # for deltas
                self.zone_names[d].append(name)  # for AlignTop/AlignBottom

    def set_tt_pixel_snap(self, data) -> None:
        self.assure_tt_lib()
        if data != 68:
            # Omit default value
            self.lib[TT_LIB_KEY]["stemsnaplimit"] = data

    def set_tt_zone_stop(self, data) -> None:
        self.assure_tt_lib()
        if data != 48:
            # Omit default value
            self.lib[TT_LIB_KEY]["zoneppm"] = data

    def set_tt_code_stop(self, data) -> None:
        self.assure_tt_lib()
        self.lib[TT_LIB_KEY]["codeppm"] = data

    def set_tt_zone_deltas(self, data) -> None:
        for zone_index, deltas in data.items():
            zone_name = self.tt_zone_names[int(zone_index)]
            self.tt_zones[zone_name]["delta"] = {str(k): v for k, v in deltas.items()}

    def build_tt_stems_lib(self) -> None:
        lib = {}
        for d in ("ttStemsH", "ttStemsV"):
            i = 0
            direction_stems = self.stems[d]
            for stem in direction_stems:
                name = stem["name"]
                del stem["name"]
                if name == "":
                    dname = "v" if d == "ttStemsH" else "h"
                    name = "%s%02i" % (dname, i)
                    i += 1
                if name in lib:
                    logger.error(
                        f"ERROR: Duplicate TrueType stem name '{name}'. "
                        "Make stem names unique in VFB."
                    )
                    raise KeyError
                lib[name] = stem
        if lib:
            self.lib[TT_LIB_KEY]["stems"] = lib

    def build_tt_zones_lib(self) -> None:
        self.assure_tt_lib()
        if self.tt_zones:
            self.lib[TT_LIB_KEY]["zones"] = self.tt_zones

    def build(self) -> None:  # noqa: C901
        # Non-MM data
        for e in self.json:
            name, data = e

            # Font Info
            attr = self.info.mapping.get(name, None)
            if attr is not None:
                self.info.set_attr(attr, data)
                continue

            if name == "header":
                pass
            elif name == "sgn":  # 1024
                self.info.familyName = data
                self.info.openTypeNamePreferredFamilyName = data
            elif name == "Monospaced":  # 1034
                self.info.set_fixed_pitch(data)
            elif name == "version full":
                pass
            elif name == "weight":  # 1048
                self.info.set_weight_class(data)
            elif name == "Style Name":  # 1127
                self.info.postscriptWeightName = data  # FIXME: Does not contain Italic
            elif name == "Type 1 XUIDs":  # 1133
                pass
            elif name == "tsn":  # 1137
                self.info.set_style_name(data)
            elif name == "Name Records":  # 1138
                self.info.set_name_records(data)
            elif name == "Glyph Unicode":  # 1250
                assert self.current_glyph is not None
                self.current_glyph.unicodes.extend(data)
            elif name == "Glyph Unicode Non-BMP":  # 1253
                assert self.current_glyph is not None
                self.current_glyph.unicodes.extend(data)
            elif name == "TrueType Zones":  # 1255
                self.set_tt_zones(data)
            elif name == "TrueType Info":  # 1264
                self.info.set_tt_info(data)
            elif name == "Gasp Ranges":  # 1265
                self.info.set_tt_gasp(data)
            elif name == "Selection":  # 1267
                self.info.set_selection(data)
            elif name == "TrueType Stem PPEMs":  # 1268
                self.set_tt_stem_ppms(data)
            elif name == "TrueType Stems":  # 1269
                self.set_tt_stems(data)
            elif name == "Pixel Snap":  # 1272
                self.set_tt_pixel_snap(data)
            elif name == "TrueType Zone Deltas":  # 1273
                self.set_tt_zone_deltas(data)
            elif name == "Zone Stop PPEM":  # 1274
                self.set_tt_zone_stop(data)
            elif name == "Code Stop PPEM":  # 1275
                self.set_tt_code_stop(data)
            elif name == "openTypeFeatures":  # 1276
                self.features = data
            elif name == "OpenType Class":  # 1277
                self.add_ot_class(data)
            elif name == "Global Guides":  # 1294
                self.mm_guides = data
            elif name == "Global Guide Properties":  # 1296
                self.guide_properties = data
            elif name == "Encoding":  # 1500
                pass
            elif name == "Master Count":  # 1503
                self.master_count = data
            elif name == "Master Name":  # 1504
                self.masters.append(data)
            elif name == "1505":
                self.masters_1505.append(data)
            elif name == "Axis Count":  # 1513
                self.axis_count = data
            elif name == "Axis Name":  # 1514
                pass
            elif name == "Axis Mapping":  # 1516
                pass
            elif name == "Blue Values Count":  # 1530
                self.num_blue_values = data
            elif name == "Other Blues Count":  # 1531
                self.num_other_blues = data
            elif name == "Family Blues Count":  # 1532
                self.num_family_blues = data
            elif name == "Family Other Blues Count":  # 1533
                self.num_family_other_blues = data
            elif name == "StemSnapH Count":  # 1534
                self.num_stem_snap_h = data
            elif name == "StemSnapV Count":  # 1535
                self.num_stem_snap_v = data
            elif name == "PostScript Info":  # 1536
                self.masters_ps_info.append(data)
            elif name == "Glyph":  # 2001
                if self.current_glyph is not None:
                    name = self.current_glyph.name
                    if name in self.glyph_masters:
                        for i in range(255):
                            n = f"{name}#{i}"
                            if n not in self.glyph_masters:
                                self.glyph_masters[n] = self.current_glyph
                                self.glyphOrder.append(n)
                                logger.warning(
                                    f"Duplicate glyph, renamed from {name} to {n}."
                                )
                                break
                    else:
                        if name is None:
                            logger.error("Glyph without name.")
                        else:
                            self.glyph_masters[name] = self.current_glyph
                            self.glyphOrder.append(name)
                self.build_mm_glyph(data)
            elif name == "Background Bitmap":  # 2007
                self.set_glyph_background(data)
            elif name == "Links":  # 2008
                assert self.current_glyph is not None
                self.current_glyph.links = data
            elif name == "Mask":  # 2009
                pass
            elif name == "2010":
                pass
            elif name == "2011":
                pass
            elif name == "Mark Color":  # 2012
                assert self.current_glyph is not None
                self.current_glyph.set_mark(data)
            elif name == "Glyph User Data":  # 2015
                assert self.current_glyph is not None
                self.current_glyph.lib["com.fontlab.v5.userData"] = data
            elif name == "Font User Data":  # 2016
                self.lib["com.fontlab.v5.userData"] = data
            elif name == "Glyph Note":  # 2017
                assert self.current_glyph is not None
                self.current_glyph.note = data
            elif name == "Glyph GDEF Data":  # 2018
                if "anchors" in data:
                    assert self.current_glyph is not None
                    self.current_glyph.anchors = []
                    for anchor in data["anchors"]:
                        a: Anchor = {
                            "x": anchor["x"],
                            "y": anchor["y"],
                        }
                        if "name" in anchor:
                            a["name"] = anchor["name"]
                        self.current_glyph.anchors.append(a)
            elif name == "Glyph Anchors Supplemental":  # 2020
                pass
            elif name == "Unicode Ranges":  # 2021
                self.info.set_unicode_ranges(data)
            elif name == "2023":
                pass
            elif name == "OpenType Metrics Class Flags":  # 2024
                self.lib["com.fontlab.v5.metricsClassFlags"] = data
            elif name == "OpenType Kerning Class Flags":  # 2026
                self.kerning_class_flags = data
            elif name == "Glyph Origin":  # 2027
                pass
            elif name == "Glyph Anchors MM":  # 2029
                assert self.current_glyph is not None
                self.current_glyph.mm_anchors = data
            elif name == "Glyph Guide Properties":  # 2031
                assert self.current_glyph is not None
                self.current_glyph.guide_properties = data
            else:
                logger.info(f"Unhandled key: {name}")

        if self.current_glyph is not None:
            assert self.current_glyph.name is not None
            self.glyph_masters[self.current_glyph.name] = self.current_glyph
            self.glyphOrder.append(self.current_glyph.name)
        self.lib["public.glyphOrder"] = self.glyphOrder
        self.assure_tt_lib()
        self.build_tt_stems_lib()
        self.build_tt_zones_lib()
        if not self.lib[TT_LIB_KEY]:
            del self.lib[TT_LIB_KEY]
        self.info.fix_underline_position()

    def get_master_info(self, master_index: int = 0) -> VfbToUfoInfo:
        # Update the info with master-specific values
        properties = [
            ("ascender", "ascender"),
            ("descender", "descender"),
            ("x_height", "xHeight"),
            ("cap_height", "capHeight"),
        ]
        if self.include_ps_hints:
            properties.extend(
                [
                    # ("force_bold", "postscriptForceBold"),
                    ("blue_scale", "postscriptBlueScale"),
                    ("blue_shift", "postscriptBlueShift"),
                    ("blue_fuzz", "postscriptBlueFuzz"),
                ]
            )

        for key, attr in properties:
            value = self.masters_ps_info[master_index].get(key, None)
            if value is not None:
                setattr(self.info, attr, value)

        if self.include_ps_hints:
            # Set "force bold"
            value = self.masters_ps_info[master_index].get("force_bold", None)
            if value is not None:
                self.info.postscriptForceBold = bool(value)

            # Set attributes that must be clipped at a certain index
            for key, attr in (
                ("blue_values", "postscriptBlueValues"),
                ("other_blues", "postscriptOtherBlues"),
                ("family_blues", "postscriptFamilyBlues"),
                ("family_other_blues", "postscriptFamilyOtherBlues"),
                ("stem_snap_h", "postscriptStemSnapH"),
                ("stem_snap_v", "postscriptStemSnapV"),
            ):
                # Get the number of values from the corresponding attribute
                num_values = getattr(self, f"num_{key}")
                if num_values == 0:
                    continue

                value = self.masters_ps_info[master_index].get(key, None)
                if value is not None:
                    setattr(self.info, attr, value[:num_values])

        # Guides
        if not self.minimal and self.mm_guides is not None:
            guides = get_master_guides(self.mm_guides, master_index)
            apply_guide_properties(guides, self.guide_properties)

            if guides:
                self.info.guidelines = guides

        return self.info

    def write(self, out_path: Path, overwrite=False, silent=False, ufoz=False) -> None:
        self.ufo_groups = transform_groups(
            self.groups,
            self.kerning_class_flags,
            self.glyphOrder,
            self.minimal,
        )
        self.ufo_kerning = UfoKerning(self.glyphOrder, self.ufo_groups, self.mm_kerning)
        for i in range(len(self.masters)):
            self.writer_master(i, out_path, overwrite, silent, ufoz)

    def writer_master(
        self, index: int, out_path: Path, overwrite=False, silent=False, ufoz=False
    ) -> None:
        self.master_index = index

        if index > 0:
            master_path = out_path.with_stem(f"{out_path.stem}-{index}")
        else:
            master_path = out_path

        if master_path.exists():
            if overwrite:
                rmtree(master_path)
            else:
                raise FileExistsError

        if not silent:
            print(f"Processing font: {self.info.ui_name.strip()}, master {index}")

        strct = UFOFileStructure.ZIP if ufoz else None
        writer = UFOWriter(
            master_path, fileCreator="com.lucasfonts.vfb3ufo", structure=strct
        )
        # FIXME: In ufoz, we can't make a directory
        glyphs_path = master_path / "glyphs"
        glyphs_path.mkdir()
        self.glyph_set = GlyphSet(glyphs_path)
        for name, mm_glyph in self.glyph_masters.items():
            logger.debug(f"    {name}, {type(name)}, {mm_glyph}")
            master_glyph = UfoMasterGlyph(
                mm_glyph, self.glyphOrder, self.master_index
            )
            master_glyph.build(
                self.minimal, self.include_ps_hints, self.encode_data_base64
            )
            self.glyph_set.writeGlyph(
                name, glyphObject=master_glyph, drawPointsFunc=master_glyph.draw_glyph
            )

        self.glyph_set.writeContents()
        self.glyph_set.writeLayerInfo(writer.getGlyphSet())

        writer.writeLayerContents()
        writer.writeGroups(self.ufo_groups)

        master_info = self.get_master_info(master_index=index)
        writer.writeInfo(master_info)

        self.ufo_kerning.extract_master_kerning(master_index=index)
        writer.writeKerning(self.ufo_kerning.master_kerning)

        if self.features:
            if self.features_classes:
                features = self.features_classes + "\n\n" + self.features
            else:
                features = self.features
            writer.writeFeatures(features)
        writer.writeLib(self.lib)
        writer.close()
        normalizeUFO(ufoPath=master_path, onlyModified=False, writeModTimes=False)
