from __future__ import annotations

from fontTools.ufoLib import UFOWriter
from fontTools.ufoLib.glifLib import GlyphSet, Glyph
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING, Any, Dict, List
from ufonormalizer import normalizeUFO
from vfbLib.ufo.glyph import VfbToUfoGlyph
from vfbLib.ufo.guides import apply_guide_properties, get_master_guides
from vfbLib.ufo.kerning import UfoKerning
from vfbLib.ufo.paths import draw_glyph, get_master_glyph
from vfbLib.ufo.vfb2ufo import (
    PS_GLYPH_LIB_KEY,
    TT_GLYPH_LIB_KEY,
    TT_LIB_KEY,
    vfb2ufo_alignment_rev,
    vfb2ufo_command_codes,
)

if TYPE_CHECKING:
    from fontTools.pens.pointPen import AbstractPointPen
    from vfbLib.types import GuideDict, GuidePropertyList
    from vfbLib.ufo.types import UfoGroups, UfoGuide, UfoMMKerning


def binaryToIntList(value: int, start: int = 0):
    intList = []
    counter = start
    while value:
        if value & 1:
            intList.append(counter)
        value >>= 1
        counter += 1
    return intList


class VfbToUfoInfo:
    def __init__(self):
        # Chance to set some defaults that should always be written
        self.familyName = ""
        self.guidelines: List[UfoGuide] = []
        self.italicAngle: float | int = 0
        self.openTypeHeadCreated = 0
        self.openTypeHeadFlags: List[int] = []
        self.openTypeHheaLineGap = 0
        self.openTypeNameDescription = ""
        self.openTypeNameSampleText = ""
        self.openTypeOS2Selection: List[int] = []
        self.openTypeOS2Type: List[int] = []
        self.openTypeOS2WidthClass = 5
        self.postscriptIsFixedPitch = False
        self.postscriptFamilyBlues: List[int] = []
        self.postscriptFamilyOtherBlues: List[int] = []
        self.postscriptFontName = ""

    @property
    def ui_name(self) -> str:
        if hasattr(self, "familyName"):
            return self.familyName
        elif hasattr(self, "postscriptFontName"):
            return self.postscriptFontName
        return "Unknown master"


class VfbToUfoWriter:
    def __init__(self, json: List[List[Any]]) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.features_classes = ""
        self.features = ""
        self.groups: UfoGroups = {}
        self.guide_properties: GuidePropertyList = []
        self.info = VfbToUfoInfo()
        self.num_blue_values = 0
        self.num_other_blues = 0
        self.num_family_blues = 0
        self.num_family_other_blues = 0
        self.num_stem_snap_h = 0
        self.num_stem_snap_v = 0
        self.mm_kerning: UfoMMKerning = {}
        self.kerning = {}
        self.lib = {}
        self.masters = []
        self.masters_1505 = []
        self.masters_ps_info = []
        self.current_glyph = None
        self.glyph_masters = {}
        self.glyphOrder = []
        # TT
        self.stem_ppms = {"ttStemsH": [], "ttStemsV": []}
        self.stems = {"ttStemsH": [], "ttStemsV": []}
        self.tt_stem_names = []
        self.tt_zones = {}
        self.tt_zone_names = []
        self.build_mapping()
        self.build()

    def build_mapping(self):
        self.info_mapping = {
            "sgn": "openTypeNamePreferredFamilyName",
            "Menu Name": "styleMapFamilyName",
            "ffn": "postscriptFullName",
            "psn": "postscriptFontName",
            "tfn": "familyName",
            "weight_name": "weightName",
            "Italic Angle": "italicAngle",
            "underlinePosition": "postscriptUnderlinePosition",
            "underlineThickness": "postscriptUnderlineThickness",
            # "Monospaced": "postscriptIsFixedPitch",  # below
            "copyright": "copyright",
            "description": "openTypeNameDescription",
            "manufacturer": "openTypeNameManufacturer",
            "Type 1 Unique ID": "postscriptUniqueID",
            # weight (class), below
            "trademark": "trademark",
            "designer": "openTypeNameDesigner",
            "designerURL": "openTypeNameDesignerURL",
            "manufacturerURL": "openTypeNameManufacturerURL",
            "width_name": "widthName",
            # Default glyph
            "License": "openTypeNameLicense",
            "License URL": "openTypeNameLicenseURL",
            "FOND Family ID": "macintoshFONDFamilyID",
            "FOND Name": "macintoshFONDName",
            "panose": "openTypeOS2Panose",
            "vendorID": "openTypeOS2VendorID",
            "Style Name": "styleName",
            "UniqueID": "openTypeNameUniqueID",
            "version": "openTypeNameVersion",
            "versionMajor": "versionMajor",
            "versionMinor": "versionMinor",
            "year": "year",
            "upm": "unitsPerEm",
            "tsn": "openTypeNamePreferredSubfamilyName",
            "hhea_ascender": "openTypeHheaAscender",
            "hhea_descender": "openTypeHheaDescender",
            "hhea_line_gap": "openTypeHheaLineGap",
            "fontNote": "note",
            "Default Glyph": "postscriptDefaultCharacter",
        }

    def transform_groups(self):
        # Rename kerning groups by applying the side flags and using the key
        # glyph for naming
        FIRST = 2**10
        SECOND = 2**11
        groups: UfoGroups = {}
        for name, glyphs in self.groups.items():
            if name.startswith("_"):
                key_glyph = glyphs[0]  # Keyglyph is used for group name
                # Sort group glyphs by glyphOrder
                glyphs.sort(key=lambda n: self.glyphOrder.index(n))

                if name in self.kerning_class_flags:
                    flags = self.kerning_class_flags[name][0]
                else:
                    flags = FIRST + SECOND
                for side, sidename in ((FIRST, 1), (SECOND, 2)):
                    if flags & side:
                        ufoname = f"public.kern{sidename}.{key_glyph}"
                        if ufoname in groups:
                            print(f"Duplicate kern1 group: {ufoname}")
                        else:
                            groups[ufoname] = glyphs
            else:
                # Pass non-kerning groups verbatim
                groups[name] = glyphs
        return groups

    def add_ot_class(self, data):
        if ":" not in data:
            print("Malformed OT class definition, skipping:", data)
            return

        name, glyphs = data.split(":", 1)
        name = name.strip()

        is_kerning = name.startswith("_")

        if name in self.groups:
            print("Duplicate OT class name, skipping:", name)
            return

        glyphs_list = glyphs.split()

        if is_kerning:
            # Reorganize glyphs so that the "keyglyph" is first
            glyphs = [g.strip() for g in glyphs_list if not g.endswith("'")]
            keyglyphs = [g.strip() for g in glyphs_list if g.endswith("'")]
            keyglyphs = [k.strip("'") for k in keyglyphs]
            if len(keyglyphs) != 1:
                print(
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

    def assign_tt_info(self, data):
        for k, v in data:
            if k == "lowest_rec_ppem":
                self.info.openTypeHeadLowestRecPPEM = v
            elif k == "timestamp":
                self.set_created_timestamp(v)
            elif k == "font_direction_hint":
                # self.info.openTypeOS2Type = binaryToIntList(v)
                pass
            elif k == "embedding":
                self.info.openTypeOS2Type = binaryToIntList(v)
            elif k == "subscript_x_size":
                self.info.openTypeOS2SubscriptXSize = v
            elif k == "subscript_y_size":
                self.info.openTypeOS2SubscriptYSize = v
            elif k == "subscript_x_offset":
                self.info.openTypeOS2SubscriptXOffset = v
            elif k == "subscript_y_offset":
                self.info.openTypeOS2SubscriptYOffset = v
            elif k == "superscript_x_size":
                self.info.openTypeOS2SuperscriptXSize = v
            elif k == "superscript_y_size":
                self.info.openTypeOS2SuperscriptYSize = v
            elif k == "superscript_x_offset":
                self.info.openTypeOS2SuperscriptXOffset = v
            elif k == "superscript_y_offset":
                self.info.openTypeOS2SuperscriptYOffset = v
            elif k == "strikeout_size":
                self.info.openTypeOS2StrikeoutSize = v
            elif k == "strikeout_position":
                self.info.openTypeOS2StrikeoutPosition = v
            elif k == "OpenTypeOS2Panose":
                # Duplicate?
                # if v != self.info.openTypeOS2Panose:
                #     print("Contradictory PANOSE values")
                #     print(self.info.openTypeOS2Panose, "vs.", v)
                pass
            elif k == "OpenTypeOS2TypoAscender":
                self.info.openTypeOS2TypoAscender = v
            elif k == "OpenTypeOS2TypoDescender":
                self.info.openTypeOS2TypoDescender = v
            elif k == "OpenTypeOS2TypoLineGap":
                self.info.openTypeOS2TypoLineGap = v
            elif k == "OpenTypeOS2WinAscent":
                self.info.openTypeOS2WinAscent = v
            elif k == "OpenTypeOS2WinDescent":
                self.info.openTypeOS2WinDescent = v
            elif k == "Codepages":
                self.info.openTypeOS2CodePageRanges = binaryToIntList(v[0])
            elif k == "ibm_classification":
                c = v >> 8
                s = v & ~(c << 8)
                self.info.openTypeOS2FamilyClass = [c, s]

    def assure_tt_lib(self):
        if not TT_LIB_KEY in self.lib:
            self.lib[TT_LIB_KEY] = {}

    def assure_tt_glyphlib(self):
        if not TT_GLYPH_LIB_KEY in self.lib:
            self.lib[TT_GLYPH_LIB_KEY] = {}

    def build_mm_glyph(self, data):
        g = self.current_glyph = VfbToUfoGlyph()
        g.lib = {}
        g.name = data["name"]
        g.unicodes = []

        # MM Stuff, need to extract later
        if "guides" in data:
            g.mm_guides = data["guides"]

        if "hints" in data:
            g.mm_hints = data["hints"]

        if "kerning" in data:
            for Rid, values in data["kerning"].items():
                self.mm_kerning[g.name, Rid] = values

        g.mm_metrics = data["metrics"]  # width and height
        g.mm_nodes = data["nodes"]

        if "components" in data:
            g.mm_components = data["components"]

        # TrueType hinting, needs to come after mm_nodes, because it needs
        # access to the point indices.
        if "tth" in data:
            self.build_tt_glyph_hints(g, data["tth"])

    def transform_stem_rounds(self, data, name) -> Dict[str, int]:
        d = {"0": 1}
        for k, v in data.items():
            key = str(v)
            val = int(k)
            if key in d:
                print(
                    f"Error in stem rounding settings for {name}, duplicate ppm {key}."
                )
            d[key] = val
        return d

    def set_created_timestamp(self, value: int):
        from datetime import datetime  # , timedelta
        from time import time

        # from dateutil.relativedelta import relativedelta
        # FIXME: Timestamp is 66 years in the future
        # d = datetime.fromtimestamp(value) # - timedelta(days=66*365.25)
        # Use the current date:
        d = datetime.fromtimestamp(time())
        self.info.openTypeHeadCreated = d.strftime("%Y/%m/%d %H:%M:%S")

    def set_tt_stem_ppms(self, data):
        for d in ("ttStemsH", "ttStemsV"):
            direction_stems = data[d]
            for ds in direction_stems:
                rounds = self.transform_stem_rounds(ds["round"], d)
                stem = {
                    "index": ds["stem"],
                    "round": rounds,
                }
                self.stem_ppms[d].append(stem)

    def set_tt_stems(self, data):
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
                    print(
                        f"Error in stem rounding settings for {d}, duplicate ppm {rv}."
                    )
                stem["round"][rv] = int(rk)
                self.stems[d].append(stem)

        # Stem name indices are v first, then h
        self.tt_stem_names = []
        for d in ("ttStemsV", "ttStemsH"):
            for ds in self.stems[d]:
                self.tt_stem_names.append(ds["name"])

    def set_tt_zones(self, data):
        self.zone_names = {"ttZonesT": [], "ttZonesB": []}
        for d in ("ttZonesB", "ttZonesT"):
            direction_zones = data[d]
            for dz in direction_zones:
                zone = {
                    "position": dz["position"],
                    "top": d == "ttZonesT",
                    "width": dz["value"],
                }
                name = dz["name"]
                if name in self.tt_zones:
                    print(f"Duplicate zone name: {name}, overwriting.")
                self.tt_zones[name] = zone
                self.tt_zone_names.append(name)  # for deltas
                self.zone_names[d].append(name)  # for AlignTop/AlignBottom

    def set_tt_pixel_snap(self, data):
        self.assure_tt_lib()
        if data != 68:
            # Omit default value
            self.lib[TT_LIB_KEY]["stemsnaplimit"] = data

    def set_tt_zone_stop(self, data):
        self.assure_tt_lib()
        if data != 48:
            # Omit default value
            self.lib[TT_LIB_KEY]["zoneppm"] = data

    def set_tt_code_stop(self, data):
        self.assure_tt_lib()
        self.lib[TT_LIB_KEY]["codeppm"] = data

    def set_tt_zone_deltas(self, data):
        for zone_index, deltas in data.items():
            zone_name = self.tt_zone_names[int(zone_index)]
            self.tt_zones[zone_name]["delta"] = {
                str(k): v for k, v in deltas.items()
            }

    def build_tt_stems_lib(self):
        lib = self.lib[TT_LIB_KEY]["stems"] = {}
        for d in ("ttStemsH", "ttStemsV"):
            direction_stems = self.stems[d]
            for stem in direction_stems:
                name = stem["name"]
                del stem["name"]
                if name in self.lib[TT_LIB_KEY]["stems"]:
                    print(
                        f"ERROR: Duplicate stem name {name}, overwriting. "
                        "Make stem names unique in VFB."
                    )
                lib[name] = stem

    def build_tt_zones_lib(self):
        self.assure_tt_lib()
        self.lib[TT_LIB_KEY]["zones"] = self.tt_zones

    def make_tt_cmd(self, tt_dict):
        code = tt_dict["code"]
        cmd = f'    <ttc code="{code}"'
        for attr in (
            "point",
            "point1",
            "point2",
            "stem",
            "zone",
            "align",
            "delta",
            "ppm1",
            "ppm2",
        ):
            if attr in tt_dict:
                cmd += f' {attr}="{tt_dict[attr]}"'
        if "round" in tt_dict:
            cmd += f' round="{str(tt_dict["round"]).lower()}"'
        cmd += "/>"
        return cmd

    def build_tt_glyph_hints(self, glyph, data) -> None:
        # Write TT hints into glyph lib.
        tth = []
        for cmd in data:
            code = cmd["cmd"]
            params = cmd["params"]
            d = {"code": vfb2ufo_command_codes[code]}
            if code in ("AlignBottom", "AlignTop"):
                d["point"] = glyph.get_point_label(params["pt"], code)
                if code == "AlignBottom":
                    zd = "ttZonesB"
                else:
                    zd = "ttZonesT"
                d["zone"] = self.zone_names[zd][params["zone"]]
            elif code in ("AlignH", "AlignV"):
                d["point"] = glyph.get_point_label(params["pt"], code)
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev[align]
            elif code in (
                "SingleLinkH",
                "SingleLinkV",
                "DoubleLinkH",
                "DoubleLinkV",
            ):
                d["point1"] = glyph.get_point_label(params["pt1"], code)
                d["point2"] = glyph.get_point_label(params["pt2"], code)
                if "stem" in params:
                    stem = params["stem"]
                    if stem == -2:
                        d["round"] = True
                    elif stem == -1:
                        pass
                    else:
                        d["stem"] = self.tt_stem_names[stem]
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev[align]
            elif code in (
                "InterpolateH",
                "InterpolateV",
            ):
                d["point"] = glyph.get_point_label(params["pti"], code)
                d["point1"] = glyph.get_point_label(params["pt1"], code)
                d["point2"] = glyph.get_point_label(params["pt2"], code)
                if "align" in params:
                    align = params["align"]
                    if align > -1:
                        d["align"] = vfb2ufo_alignment_rev[align]
            elif code in (
                "MDeltaH",
                "MDeltaV",
                "FDeltaH",
                "FDeltaV",
            ):
                d["point"] = glyph.get_point_label(params["pt"], code)
                d["delta"] = params["shift"]
                d["ppm1"] = params["ppm1"]
                d["ppm2"] = params["ppm2"]
            else:
                print(f"Unknown TT command: {code}")

            tth.append(self.make_tt_cmd(d))

        glyph.lib[TT_GLYPH_LIB_KEY] = (
            "  <ttProgram>\n" + "\n".join(tth) + "\n  </ttProgram>\n"
        )

    def build_ps_glyph_hints(self, glyph, data) -> None:
        # Set the master-specific hints from data to the glyph lib
        # Use format 2, not what FL does.
        # https://github.com/adobe-type-tools/psautohint/blob/master/python/psautohint/ufoFont.py
        hint_sets = []
        hint_set = {
            "pointTag": "hr01",
            "stems": [],
        }
        for h in data:
            cmd, pos, width = h
            hint_set["stems"].append(f"{cmd} {pos} {width}")
        if hint_set["stems"]:
            glyph.lib[PS_GLYPH_LIB_KEY] = {
                # "id": "FIXME",
                "hintSetList": [hint_set],
                "flexList": [],
            }

    def build(self):
        # Non-MM data
        for e in self.json:
            name, data = e

            # Font Info
            attr = self.info_mapping.get(name, None)
            if attr is not None:
                setattr(self.info, attr, data)
                continue

            if name == "header":
                pass
            elif name == "Monospaced":  # 1034
                self.info.postscriptIsFixedPitch = bool(data)
            elif name == "version full":
                pass
            elif name == "weight":  # 1048
                self.info.openTypeOS2WeightClass = max(0, data)
            elif name == "Type 1 XUIDs":
                pass
            elif name == "Name Records":  # 1138
                self.info.openTypeNameRecords = []
                for rec in data:
                    nameID, platformID, encodingID, languageID, s = rec
                    self.info.openTypeNameRecords.append(
                        {
                            "nameID": nameID,
                            "platformID": platformID,
                            "encodingID": encodingID,
                            "languageID": languageID,
                            "string": s,
                        }
                    )
            elif name == "Glyph Unicode":  # 1250
                self.current_glyph.unicodes.extend(data)
            elif name == "Glyph Unicode Non-BMP":  # 1253
                self.current_glyph.unicodes.extend(data)
            elif name == "TrueType Zones":  # 1255
                self.set_tt_zones(data)
            elif name == "TrueType Info":  # 1264
                self.assign_tt_info(data)
            elif name == "Gasp Ranges":  # 1265
                gasp = []
                for rec in data:
                    gasp.append(
                        {
                            "rangeMaxPPEM": rec["maxPpem"],
                            "rangeGaspBehavior": binaryToIntList(rec["flags"]),
                        }
                    )
                self.info.openTypeGaspRangeRecords = gasp
            elif name == "Selection":  # 1267
                # Bit 0 = Regular
                # Bit 5 = Bold
                # Bit 6 = Italic
                # Those should not be included in the list.
                # Any others could remain, but FL doesn't set them.
                self.info.openTypeOS2Selection = [
                    b for b in binaryToIntList(data) if b not in (0, 5, 6)
                ]
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
                self.mm_guides: GuideDict = data
            elif name == "Global Guide Properties":  # 1296
                self.guide_properties: GuidePropertyList = data
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
                                print(
                                    f"Duplicate glyph, renamed from {name} to {n}."
                                )
                                break
                    else:
                        self.glyph_masters[name] = self.current_glyph
                        self.glyphOrder.append(name)
                self.build_mm_glyph(data)
            elif name == "Background":  # 2007
                # Bitmap background
                pass
            elif name == "Links":  # 2008
                self.current_glyph.links = data
            elif name == "Mask":  # 2009
                pass
            elif name == "2010":
                pass
            elif name == "2011":
                pass
            elif name == "Mark Color":  # 2012
                self.current_glyph.set_mark(data)
            elif name == "Glyph User Data":  # 2015
                self.current_glyph.lib["com.fontlab.v5.userData"] = data
            elif name == "Font User Data":  # 2016
                self.lib["com.fontlab.v5.userData"] = data
            elif name == "Glyph Note":  # 2017
                self.current_glyph.note = data
            elif name == "Glyph GDEF Data":  # 2018
                if "anchors" in data:
                    self.current_glyph.anchors = []
                    for anchor in data["anchors"]:
                        self.current_glyph.anchors.append(
                            {
                                "name": anchor["name"],
                                "x": anchor["x"],
                                "y": anchor["y"],
                            }
                        )
            elif name == "Glyph Anchors Supplemental":  # 2020
                pass
            elif name == "Unicode Ranges":  # 2021
                self.info.openTypeOS2UnicodeRanges = binaryToIntList(data)
            elif name == "2023":
                pass
            elif name == "OpenType Metrics Class Flags":  # 2024
                self.lib["com.fontlab.v5.metricsClassFlags"] = data
            elif name == "OpenType Kerning Class Flags":  # 2026
                self.kerning_class_flags = data
            elif name == "Glyph Origin":  # 2027
                pass
            elif name == "Glyph Anchors MM":  # 2029
                self.current_glyph.mm_anchors = data
            elif name == "Glyph Guide Properties":  # 2031
                self.current_glyph.guide_properties = data
            else:
                print(f"Unhandled key: {name}")

        if self.current_glyph is not None:
            self.glyph_masters[self.current_glyph.name] = self.current_glyph
            self.glyphOrder.append(self.current_glyph.name)
        self.lib["public.glyphOrder"] = self.glyphOrder
        self.assure_tt_lib()
        self.build_tt_stems_lib()
        self.build_tt_zones_lib()

    def get_master_hints(self, master_index=0) -> List:
        hints = []
        for d in "hv":
            dh = self.current_mmglyph.mm_hints[d]
            for mm_hints in dh:
                hint = mm_hints[master_index]
                hints.append((f"{d}stem", hint["pos"], hint["width"]))
        return hints

    def get_master_info(self, master_index=0):
        # Update the info with master-specific values
        for k, v in (
            ("force_bold", "postscriptForceBold"),
            ("blue_scale", "postscriptBlueScale"),
            ("blue_shift", "postscriptBlueShift"),
            ("blue_fuzz", "postscriptBlueFuzz"),
            ("ascender", "ascender"),
            ("descender", "descender"),
            ("x_height", "xHeight"),
            ("cap_height", "capHeight"),
        ):
            value = self.masters_ps_info[master_index].get(k, None)
            if value is not None:
                setattr(self.info, v, value)

        value = self.masters_ps_info[master_index].get("force_bold", None)
        if value is not None:
            self.info.postscriptForceBold = bool(value)

        for k, v in (
            ("blue_values", "postscriptBlueValues"),
            ("other_blues", "postscriptOtherBlues"),
            ("family_blues", "postscriptFamilyBlues"),
            ("family_other_blues", "postscriptFamilyOtherBlues"),
            ("stem_snap_h", "postscriptStemSnapH"),
            ("stem_snap_v", "postscriptStemSnapV"),
        ):
            num_values = getattr(self, f"num_{k}")
            if num_values == 0:
                continue

            value = self.masters_ps_info[master_index].get(k, None)
            if value is not None:
                setattr(self.info, v, value[:num_values])

        # Guides
        if hasattr(self, "mm_guides"):
            guides = get_master_guides(self.mm_guides, master_index)
            apply_guide_properties(guides, self.guide_properties)

            if guides:
                self.info.guidelines = guides

        return self.info

    def draw_glyph(self, pen: AbstractPointPen):
        """
        Draw the current glyph onto pen. Use self.master_index for which outlines
        or component transformations to use.
        """

        contours, components = get_master_glyph(
            self.current_mmglyph, self.glyphOrder, self.master_index
        )
        draw_glyph(contours, components, pen)

    def write(self, out_path: Path, overwrite=False, silent=False) -> None:
        self.ufo_groups = self.transform_groups()
        self.ufo_kerning = UfoKerning(
            self.glyphOrder, self.ufo_groups, self.mm_kerning
        )
        for i in range(len(self.masters)):
            self.writer_master(i, out_path, overwrite, silent)

    def writer_master(
        self, index: int, out_path: Path, overwrite=False, silent=False
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
            print(f"Processing font: {self.info.ui_name}, master {index}")

        writer = UFOWriter(master_path, fileCreator="com.lucasfonts.vfb3ufo")
        glyphs_path = master_path / "glyphs"
        glyphs_path.mkdir()
        gs = GlyphSet(glyphs_path)
        for name, self.current_mmglyph in self.glyph_masters.items():
            g = Glyph(name, gs)
            g.anchors = self.current_mmglyph.anchors
            # Apply master anchor positions
            if hasattr(self.current_mmglyph, "mm_anchors"):
                for j, anchor in enumerate(self.current_mmglyph.mm_anchors):
                    g.anchors[j]["x"] = anchor["x"][index]
                    g.anchors[j]["y"] = anchor["y"][index]
            g.lib = self.current_mmglyph.lib

            # Apply master hint positions and widths

            # FIXME

            # master_hints = self.get_master_hints(master_index=index)
            # if master_hints:
            #     self.build_ps_glyph_hints(g, master_hints)

            if hasattr(self.current_mmglyph, "mm_guides"):
                master_guides = get_master_guides(
                    self.current_mmglyph.mm_guides, index
                )
                apply_guide_properties(
                    master_guides, self.current_mmglyph.guide_properties
                )
                if master_guides:
                    g.guidelines = master_guides

            g.unicodes = self.current_mmglyph.unicodes
            g.width, g.height = self.current_mmglyph.mm_metrics[index]
            gs.writeGlyph(name, glyphObject=g, drawPointsFunc=self.draw_glyph)

        gs.writeContents()
        gs.writeLayerInfo(writer.getGlyphSet())

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
        normalizeUFO(ufoPath=master_path, onlyModified=False)
