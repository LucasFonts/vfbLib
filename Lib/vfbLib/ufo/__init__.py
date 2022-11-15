from __future__ import annotations

from colorsys import hls_to_rgb
from fontTools.ufoLib import UFOWriter
from fontTools.ufoLib.glifLib import GlyphSet, Glyph
from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING, Any, List, Tuple
from ufonormalizer import normalizeUFO

if TYPE_CHECKING:
    from fontTools.pens.pointPen import AbstractPointPen

    Point = Tuple[int, int]


def binaryToIntList(value, start=0):
    intList = []
    counter = start
    while value:
        if value & 1:
            intList.append(counter)
        value >>= 1
        counter += 1
    return intList


class VfbToUfoInfo:
    @property
    def ui_name(self):
        if hasattr(self, "familyName"):
            return self.familyName
        elif hasattr(self, "postscriptFontName"):
            return self.postscriptFontName
        return "Unknown master"


class VfbToUfoGlyph:
    def set_mark(self, hue):
        self.lib["public.markColor"] = "%f,%f,%f,1" % hls_to_rgb(
            h=hue / 255, l=0.8, s=0.76
        )


class VfbToUfoWriter:
    def __init__(self, json: List[List[Any]]) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.features_classes = ""
        self.features = ""
        self.groups = {}
        self.info = VfbToUfoInfo()
        self.num_blue_values = 0
        self.num_other_blues = 0
        self.num_family_blues = 0
        self.num_family_other_blues = 0
        self.num_stem_snap_h = 0
        self.num_stem_snap_v = 0
        self.mm_kerning = {}
        self.kerning = {}
        self.lib = {}
        self.masters = []
        self.masters_1505 = []
        self.masters_ps_info = []
        self.current_glyph = None
        self.glyph_masters = {}
        self.glyphOrder = []
        self.build_mapping()
        self.build()

    def build_mapping(self):
        self.info_mapping = {
            "sgn": "openTypeNamePreferredFamilyName",
            # "sgn": "styleMapFamilyName",  # ?
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
            "fontNote": "note",
            "Default Glyph": "postscriptDefaultCharacter",
        }

    def add_ot_class(self, data):
        if ":" not in data:
            print("Malformed OT class definition, skipping:", data)
            return

        name, glyphs = data.split(":", 1)
        name = name.strip()
        if f"@{name}" in self.groups:
            print("Duplicate OT class name, skipping:", name)
            return

        glyphs_list = glyphs.split()

        if name.startswith("_"):
            # Kerning class
            glyphs = [g.strip() for g in glyphs_list if not g.endswith("'")]
            keyglyphs = [g.strip() for g in glyphs_list if g.endswith("'")]
            keyglyphs = [k.strip("'") for k in keyglyphs]
            if len(keyglyphs) != 1:
                print(
                    f"Unexpected number of key glyphs in group {name}: {keyglyphs}"
                )
            glyphs.insert(0, *keyglyphs)

        else:
            glyphs = [g.strip() for g in glyphs_list]
        self.groups[f"@{name}"] = glyphs
        self.features_classes += f"@{name} = [{' '.join(glyphs)}];\n"

    def assignMetrics(self, data):
        for k, v in data:
            if k == "embedding":
                self.info.openTypeOS2Selection = [
                    i for i in binaryToIntList(v) if i in (1, 2, 3, 4)
                ]
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

    def build_mm_glyph(self, data):
        g = self.current_glyph = VfbToUfoGlyph()
        g.lib = {}
        g.name = data["name"]
        masters = data["num_masters"]
        g.unicodes = []

        if "tth" in data:
            g.tth = data["tth"]

        # MM Stuff, need to extract later
        if "kerning" in data:
            for Rid, values in data["kerning"].items():
                self.mm_kerning[g.name, Rid] = values

        g.mm_metrics = data["metrics"]  # width and height
        g.mm_nodes = data["nodes"]

        if "components" in data:
            g.mm_components = data["components"]

    def build(self):
        for e in self.json:
            name, data = e

            # Font Info
            attr = self.info_mapping.get(name, None)
            if attr is not None:
                setattr(self.info, attr, data)
                continue

            if name == "Encoding":
                pass
            elif name == "Monospaced":
                self.info.postscriptIsFixedPitch = bool(data)
            elif name == "weight":
                self.info.openTypeOS2WeightClass = max(0, data)
            elif name == "Gasp Ranges":
                gasp = []
                for rec in data:
                    gasp.append({
                        "rangeMaxPPEM": rec["maxPpem"],
                        "rangeGaspBehavior": binaryToIntList(rec["flags"]),
                    })
                self.info.openTypeGaspRangeRecords = gasp
            elif name == "Metrics":
                self.assignMetrics(data)
            elif name == "TrueType Stem PPEMs":
                pass
            elif name == "TrueType Stems":
                pass
            elif name == "TrueType Zones":
                pass
            elif name == "Pixel Snap":
                pass
            elif name == "Zone Stop PPEM":
                pass
            elif name == "TrueType Zone Deltas":
                pass
            elif name == "Name Records":
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
            elif name == "Font User Data":
                self.lib["com.fontlab.v5.userData"] = data
            elif name == "openTypeFeatures":
                self.features = data
            elif name == "OpenType Class":
                self.add_ot_class(data)
            elif name == "Axis Mapping":
                pass
            elif name == "Master Name":
                self.masters.append(data)
            elif name == "1505":
                self.masters_1505.append(data)
            elif name == "Blue Values Count":
                self.num_blue_values = data
            elif name == "Other Blues Count":
                self.num_other_blues = data
            elif name == "Family Blues Count":
                self.num_family_blues = data
            elif name == "Family_Other Blues Count":
                self.num_family_other_blues = data
            elif name == "StemSnapH Count":
                self.num_stem_snap_h = data
            elif name == "StemSnapV Count":
                self.num_stem_snap_v = data
            elif name == "PostScript Info":
                self.masters_ps_info.append(data)
            elif name == "Glyph":
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
            elif name == "Links":
                self.current_glyph.links = data
            elif name == "2023":
                pass
            elif name == "2010":
                pass
            elif name == "Mask":
                pass
            elif name == "2011":
                pass
            elif name == "Mark Color":
                self.current_glyph.set_mark(data)
            elif name == "Glyph Origin":
                pass
            elif name == "2031":
                pass
            elif name == "Glyph Unicode":
                self.current_glyph.unicodes.extend(data)
            elif name == "2012":
                pass
            elif name == "Glyph User Data":
                self.current_glyph.lib["com.fontlab.v5.userData"] = data
            elif name == "Glyph Note":
                self.current_glyph.note = data
            elif name == "Glyph Unicode Non-BMP":
                self.current_glyph.unicodes.extend(data)
            elif name == "Glyph GDEF Data":
                pass
            elif name == "Glyph Anchors Supplemental":
                pass
            else:
                pass
                # print(f"Unhandled key: {name}")
        if self.current_glyph is not None:
            self.glyph_masters[self.current_glyph.name] = self.current_glyph
            self.glyphOrder.append(self.current_glyph.name)
        self.lib["public.glyphOrder"] = self.glyphOrder

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

        return self.info

    def get_master_kerning(self, master_index=0):
        # TODO: Must look up class kerning references
        kerning = {}
        for pair, values in self.mm_kerning.items():
            L, Rid = pair
            kerning[L, self.glyphOrder[int(Rid)]] = values[master_index]
        return kerning

    def get_master_glyph(self, mmglyph, master_index=0):
        # Extract a single master glyph from a mm glyph
        contours = []
        last_type = None
        if hasattr(mmglyph, "mm_nodes"):
            # print(f"Add nodes to {mmglyph.name}...")
            contours = []
            contour: List[List[None | str | Point]] | None = None
            qcurve = False
            for n in mmglyph.mm_nodes:
                # Nodes for the current master
                nodes = n["points"][master_index]
                segment_type = n["type"]

                # print("****", segment_type, nodes)

                if segment_type == "line":
                    if qcurve:
                        effective_type = "qcurve"
                        qcurve = False
                    else:
                        effective_type = "line"

                    contour.append(
                        [effective_type, (nodes[0]["x"], nodes[0]["y"])]
                    )
                    last_type = segment_type

                elif segment_type == "move":
                    if contour is not None:
                        if last_type == "line":
                            contour[0][0] = "line"
                        elif last_type == "curve":
                            contour[0][0] = "curve"
                        elif last_type == "qcurve":
                            contour[0][0] = "qcurve"
                        contours.append(contour)
                    contour = [["move", (nodes[0]["x"], nodes[0]["y"])]]
                    qcurve = False

                elif segment_type == "curve":
                    pt3, pt1, pt2 = nodes
                    contour.append([None, (pt1["x"], pt1["y"])])
                    contour.append([None, (pt2["x"], pt2["y"])])
                    contour.append(["curve", (pt3["x"], pt3["y"])])
                    qcurve = False

                elif segment_type == "qcurve":
                    qcurve = True
                    contour.append([None, (nodes[0]["x"], nodes[0]["y"])])
                    last_type = segment_type

            if contour is not None:
                if last_type == "line":
                    contour[0][0] = "line"
                elif last_type == "curve":
                    contour[0][0] = "curve"
                elif last_type == "qcurve":
                    contour[0][0] = "qcurve"
                contours.append(contour)

        components: List[
            Tuple[str, Tuple[float, float, float, float, int, int]]
        ] = []
        if hasattr(mmglyph, "mm_components"):
            for c in mmglyph.mm_components:
                transform = (
                    c["scaleX"][master_index],
                    0.0,
                    0.0,
                    c["scaleY"][master_index],
                    c["offsetX"][master_index],
                    c["offsetY"][master_index],
                )
                components.append((self.glyphOrder[c["gid"]], transform))

        return contours, components

    def draw_glyph(self, pen: AbstractPointPen):
        """
        Draw the current glyph onto pen. Use self.master_index for which outlines
        or component transformations to use.
        """

        contours, components = self.get_master_glyph(
            self.current_mmglyph, self.master_index
        )

        for contour in contours:
            pen.beginPath()
            for segment_type, pt in contour:
                pen.addPoint(pt, segment_type)
            pen.endPath()

        for gn, tr in components:
            pen.addComponent(glyphName=gn, transformation=tr)

    def write(self, out_path: Path, overwrite=False, silent=False) -> None:
        for i in range(len(self.masters)):
            self.master_index = i

            if i > 0:
                master_path = out_path.with_stem(f"{out_path.stem}-{i}")
            else:
                master_path = out_path

            if master_path.exists():
                if overwrite:
                    rmtree(master_path)
                else:
                    raise FileExistsError

            print(f"Processing font: {self.info.ui_name}")

            writer = UFOWriter(
                master_path, fileCreator="com.lucasfonts.vfb3ufo"
            )
            glyphs_path = master_path / "glyphs"
            glyphs_path.mkdir()
            gs = GlyphSet(glyphs_path)
            for name, self.current_mmglyph in self.glyph_masters.items():
                g = Glyph(name, gs)
                g.lib = self.current_mmglyph.lib
                g.unicodes = self.current_mmglyph.unicodes
                g.width, g.height = self.current_mmglyph.mm_metrics[i]
                gs.writeGlyph(
                    name, glyphObject=g, drawPointsFunc=self.draw_glyph
                )
            gs.writeContents()
            gs.writeLayerInfo(writer.getGlyphSet())

            master_kerning = self.get_master_kerning(master_index=i)
            master_info = self.get_master_info(master_index=i)

            writer.writeLayerContents()
            writer.writeGroups(self.groups)
            writer.writeInfo(master_info)
            writer.writeKerning(master_kerning)
            if self.features:
                if self.features_classes:
                    features = self.features_classes + "\n\n" + self.features
                else:
                    features = self.features
                writer.writeFeatures(features)
            writer.writeLib(self.lib)
            writer.close()
            normalizeUFO(ufoPath=out_path, onlyModified=False)
