from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler


class TrueTypeZonesCompiler(BaseCompiler):
    """
    A compiler that compiles TrueType hinting "alignment zones" data
    """

    def _compile(self, data: Any) -> None:
        for side in ("ttZonesT", "ttZonesB"):
            side_zones = data.get(side, [])
            self.write_value(len(side_zones))
            for zone in side_zones:
                self.write_value(zone["position"])
                self.write_value(zone["value"])
                name = zone["name"]
                self.write_value(len(name))
                self.write_str(name)


class TrueTypeZoneDeltasCompiler(BaseCompiler):
    """
    A compiler that compiles TrueType hinting "alignment zones" deltas data
    """

    def _compile(self, data: Any) -> None:
        deltas = []
        for zone_index, spec in data.items():
            zone_index = int(zone_index)
            for ppm, shift in spec.items():
                deltas.append((zone_index, int(ppm), shift))
        deltas.sort()
        self.write_value(len(deltas))
        for zone_index, ppm, shift in deltas:
            self.write_value(zone_index)
            self.write_value(ppm)
            self.write_value(shift)
