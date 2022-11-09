from defcon import Font
from fontTools.ufoLib import UFOWriter
from fontTools.ufoLib.glifLib import GlyphSet, Glyph
from pathlib import Path
from typing import Any, List


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
    pass


class VfbToUfoGlyph:
    pass


class VfbToUfoWriter:
    def __init__(self, json) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.groups = {}
        self.info = VfbToUfoInfo()
        self.kerning = {}
        self.lib = {}
        self.masters = []
        self.masters_1505 = []
        self.masters_1536 = []
        self.current_glyph = None
        self.glyph_masters = {}
        self.glyphOrder = []
        self.build_mapping()
        self.mmdata: List[Any] = []

    def build_mapping(self):
        self.info_mapping = {
            "description": "notice",
            "ffn": "postscriptFullName",
            "psn": "postscriptFontName",
            "tfn": "openTypeNamePreferredFamilyName",
            "sgn": "familyName",  # Windows
            "weight_name": "weightName",
            "width_name": "widthName",
            "copyright": "copyright",
            "trademark": "trademark",
            "designer": "designer",
            "designerURL": "designerURL",
            "manufacturerURL": "manufacturerURL",
            "manufacturer": "manufacturer",
            "underlinePosition": "postscriptUnderlinePosition",
            "underlineThickness": "postscriptUnderlineThickness",
            "panose": "openTypeOS2Panose",
            "UniqueID": "openTypeNameUniqueID",
            "tsn": "openTypeNamePreferredSubfamilyName",
            "Style Name": "styleName",
            "vendorID": "openTypeOS2VendorID",
            "year": "year",
            "versionMajor": "versionMajor",
            "versionMinor": "versionMinor",
            "upm": "unitsPerEm",
            "hhea_ascender": "openTypeHheaAscender",
            "hhea_descender": "openTypeHheaDescender",
            "fontNote": "note",
            "Default Glyph": "postscriptDefaultCharacter",
        }

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
                self.info.openTypeOS2SSuperscriptXSize = v
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

    def build_glyph(self, data):
        g = self.current_glyph = VfbToUfoGlyph()
        g.lib = {}
        g.name = data["name"]
        masters = data["num_masters"]
        g.unicodes = []
        if "tth" in data:
            g.tth = data["tth"]
        # MM Stuff, need to extract at write time
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
            elif name == "weight":
                self.info.openTypeOS2WeightClass = max (0, data)
            elif name == "Gasp Ranges":
                # self.info.openTypeGaspRangeRecords = data
                pass
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
                pass
            elif name == "Font User Data":
                self.lib["com.fontlab.v5.userData"] = data
            elif name == "openTypeFeatures":
                self.features = data
            elif name == "Axis Mapping":
                pass
            elif name == "Master Name":
                self.masters.append(data)
            elif name == "1505":
                self.masters_1505.append(data)
            elif name == "1536":
                if len(data) > 5:
                    # FIXME: There is something in the header also called 1536
                    self.masters_1536.append(data)
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
                self.build_glyph(data)
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
        self.lib["public.glyphOrder"] = self.glyphOrder

    def write(self, out_path: Path) -> None:
        for i in range(len(self.masters)):
            if i > 0:
                master_path = out_path.with_stem(f"{out_path.stem}-{i}")
            else:
                master_path = out_path
            writer = UFOWriter(
                master_path, fileCreator="com.lucasfonts.vfb3ufo"
            )
            glyphs_path = master_path / "glyphs"
            glyphs_path.mkdir()
            gs = GlyphSet(glyphs_path)
            for name, mmglyph in self.glyph_masters.items():
                g = Glyph(name, gs)
                g.lib = mmglyph.lib
                g.unicodes = mmglyph.unicodes
                g.width, g.height = mmglyph.mm_metrics[i]
                
                gs.writeGlyph(name, g)
            gs.writeContents()
            gs.writeLayerInfo(["public.default", "glyphs"])
            writer.writeLayerContents()
            writer.writeGroups(self.groups)
            writer.writeInfo(self.info)
            writer.writeKerning(self.kerning)
            writer.writeFeatures(self.features)
            writer.writeLib(self.lib)
            writer.close()
            # For now, normalize like defcon
            # f = Font(out_path)
            # f.save(out_path)
