from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vfbLib import tt_settings, ttinfo_names
from vfbLib.compilers.base import BaseCompiler
from vfbLib.helpers import intListToBinary

if TYPE_CHECKING:
    from vfbLib.typing import FlagsOptionsDict, TTStemsDict, TTZonesDict, VdmxRecDict


def convert_flags_options_to_int(data: dict[str, dict[str, list[int]]]) -> int:
    value = 0
    head_flags_options: FlagsOptionsDict = data["head_flags"]
    assert isinstance(head_flags_options, dict)
    flags_list: list[int] = head_flags_options.get("flags", [])
    value = intListToBinary(flags_list)
    options: tuple[str, ...]
    if options := tuple(head_flags_options["options"]):
        option_bits = []
        for k, v in tt_settings.items():
            if v in options:
                option_bits.append(k)

        value += intListToBinary(option_bits) << 16
    return value


class GaspCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for rec in data:
            self.write_uint16(rec["maxPpem"])
            self.write_uint16(rec["flags"])


class TrueTypeInfoCompiler(BaseCompiler):
    def _write_if_exists(self, numkey: int, data: Any, signed: bool = True) -> None:
        strkey = ttinfo_names[numkey]
        if strkey in data:
            self.write_uint8(numkey)
            self.write_value(data[strkey], signed=signed)

    def _compile(self, data: dict[str, int | list[int]]) -> None:
        for k in (0x33, 0x34, 0x35, 0x36, 0x37, 0x38):
            self.write_uint8(k)
            self.write_value(data[ttinfo_names[k]])

        # Convert combined flags and options dict back to a single int
        head_flags_options = convert_flags_options_to_int(data)
        self.write_uint8(0x39)
        self.write_value(head_flags_options)

        for k in (
            0x3A,
            0x3B,
            0x3C,
        ):
            self._write_if_exists(k, data)

        for k in (0x56, 0x57):
            self._write_if_exists(k, data, signed=False)

        for k in (
            0x3D,
            0x3E,
            0x3F,
            0x40,
            0x41,
            0x42,
            0x43,
            0x44,
            0x45,
            0x46,
            0x47,
            0x48,
            0x49,
            0x4A,
            0x4B,
        ):
            self._write_if_exists(k, data)

        # PANOSE
        values = data[ttinfo_names[0x4C]]
        assert len(values) == 10
        self.write_uint8(0x4C)
        for value in values:
            self.write_uint8(value)

        for k in (0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52, 0x5C):
            self._write_if_exists(k, data)

        # HDMX 1 and 2
        for k in (0x53, 0x58):
            strkey = ttinfo_names[k]
            if strkey in data:
                values = data[strkey]
                self.write_uint8(k)
                self.write_value(len(values))
                for value in values:
                    self.write_uint8(value)

        # Codepages
        cp_dict = data[ttinfo_names[0x54]]
        self.write_uint8(0x54)
        for ck in ("os2_ul_code_page_range1", "os2_ul_code_page_range2"):
            value = cp_dict[ck]
            self.write_value(value, signed=False)

        self.write_uint8(0x32)  # End marker


class TrueTypeStemPpems1Compiler(BaseCompiler):
    def _compile(self, data: TTStemsDict) -> None:
        for direction in ("ttStemsV", "ttStemsH"):
            stems = data[direction]
            for stem in stems:
                self.write_value(stem["round"][1])


class TrueTypeStemPpems23Compiler(BaseCompiler):
    def _compile(self, data: TTStemsDict) -> None:
        for direction in ("ttStemsV", "ttStemsH"):
            stems = data[direction]
            self.write_value(len(stems))
            for stem in stems:
                for k in (2, 3):
                    self.write_value(stem["round"][k])


class TrueTypeStemPpemsCompiler(BaseCompiler):
    def _compile(self, data: TTStemsDict) -> None:
        for direction in ("ttStemsV", "ttStemsH"):
            stems = data[direction]
            self.write_value(len(stems))
            for stem in stems:
                for k in range(2, 6):
                    self.write_value(stem["round"][k])


class TrueTypeStemsCompiler(BaseCompiler):
    def _compile(self, data: TTStemsDict) -> None:
        for direction in ("ttStemsV", "ttStemsH"):
            stems = data[direction]
            self.write_value(len(stems))
            for stem in stems:
                self.write_value(stem["value"])  # width
                stem_name = stem["name"].encode(self.encoding)
                self.write_uint8(len(stem_name))
                self.write_bytes(stem_name)
                self.write_value(stem["round"][6])


class TrueTypeZonesCompiler(BaseCompiler):
    """
    A compiler that compiles TrueType hinting "alignment zones" data
    """

    def _compile(self, data: TTZonesDict) -> None:
        for side in ("ttZonesT", "ttZonesB"):
            side_zones = data.get(side, [])
            self.write_value(len(side_zones))
            for zone in side_zones:
                self.write_value(zone["position"])
                self.write_value(zone["value"])
                name = zone["name"]
                self.write_str_with_len(name)


class TrueTypeZoneDeltasCompiler(BaseCompiler):
    """
    A compiler that compiles TrueType hinting "alignment zones" deltas data
    """

    def _compile(self, data: dict[int, dict[int, int]]) -> None:
        deltas = []
        for zone_index, spec in data.items():
            for ppm, shift in spec.items():
                deltas.append((zone_index, ppm, shift))
        deltas.sort()
        self.write_value(len(deltas))
        for zone_index, ppm, shift in deltas:
            self.write_value(zone_index)
            self.write_value(ppm)
            self.write_value(shift)


class VdmxCompiler(BaseCompiler):
    def _compile(self, data: list[VdmxRecDict]) -> None:
        self.write_value(len(data))
        for rec in data:
            self.write_value(rec["pelHeight"])
            self.write_value(rec["max"])
            self.write_value(rec["min"])
