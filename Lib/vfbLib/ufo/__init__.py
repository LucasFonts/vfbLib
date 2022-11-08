from defcon import Font
from pathlib import Path
from typing import List


class UfoWriter:
    def __init__(self, json) -> None:
        """
        Serialize the JSON structure to UFO(s)
        """
        self.json = json
        self.ufos: List[Font] = []
    
    def build(self):
        ufo = Font()
        for e in self.json:

    
    def write(self, out_path: Path) -> None:
        for ufo in self.ufos:
            ufo.save(out_path)