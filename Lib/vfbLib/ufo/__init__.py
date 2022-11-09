from fontTools.ufoLib import UFOWriter
from pathlib import Path
from typing import Any, List


class VfbToUfoInfo:
    pass


class VfbToUfoWriter:
    def __init__(self, json) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.info = VfbToUfoInfo()
        self.build_mapping()
        self.mmdata: List[Any] = []
    
    def build_mapping(self):
        self.info_mapping = {
            "description": "notice",
            "psn": "postscriptFontName",
        }
    
    def build(self):
        for e in self.json:
            name, data = e

            # Font Info
            attr = self.info_mapping.get(name, None)
            if attr is not None:
                setattr(self.info, attr, data)

    
    def write(self, out_path: Path) -> None:
        # for mm in self.mmdata:
        writer = UFOWriter(out_path, fileCreator="com.lucasfonts.vfb3ufo")
        writer.writeInfo(self.info)
        writer.close()
