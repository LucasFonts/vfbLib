import logging

from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class TrueTypeInfoParser(BaseParser):
    """
    A parser that reads data as "TrueType Info" values.
    """

    def assert_unique(
        self, d: dict[str, int | list[int] | list[str]], key: str
    ) -> None:
        if key in d:
            logger.error(f"Duplicate key in TrueType Info: {key} in {d}")
            raise KeyError

    def _parse(self):
        info_names = {
            0x33: "0x33",
            0x34: "0x34",
            0x35: "0x35",
            0x36: "0x36",
            0x37: "0x37",
            0x38: "0x38",
            0x39: "tt_font_info_settings",  # 0 = false, 65536 = true
            0x3A: "units_per_em",  # duplicate
            0x3B: "0x3b",
            0x3C: "lowest_rec_ppem",
            0x3D: "font_direction_hint",
            0x3E: "weight_class",  # duplicate
            0x3F: "width_class",  # duplicate
            0x40: "embedding",
            0x41: "subscript_x_size",
            0x42: "subscript_y_size",
            0x43: "subscript_x_offset",
            0x44: "subscript_y_offset",
            0x45: "superscript_x_size",
            0x46: "superscript_y_size",
            0x47: "superscript_x_offset",
            0x48: "superscript_y_offset",
            0x49: "strikeout_size",
            0x4A: "strikeout_position",
            0x4B: "ibm_classification",  # ibm_classification + subclass
            0x4C: "OpenTypeOS2Panose",
            0x4D: "OpenTypeOS2TypoAscender",
            0x4E: "OpenTypeOS2TypoDescender",
            0x4F: "OpenTypeOS2TypoLineGap",
            0x50: "0x50",
            0x51: "OpenTypeOS2WinAscent",
            0x52: "OpenTypeOS2WinDescent",
            0x53: "Hdmx PPMs 1",
            0x54: "Codepages",
            0x56: "timestamp",
            0x57: "0x57",
            0x58: "Hdmx PPMs 2",
            0x5C: "Average Width",
        }
        info = {}

        while True:
            k = self.read_uint8()
            bk = info_names.get(k, f"bit{k}")  # dict key, as a bit number
            dk = info_names.get(k, str(k))  # dict key, human-readable
            hk = info_names.get(k, hex(k))  # dict key, hex

            if k == 0x32:
                return info

            elif k in (0x33, 0x34, 0x35, 0x36, 0x37, 0x38):
                self.assert_unique(info, dk)
                info[dk] = self.read_value()

            elif k == 0x39:
                # Options
                self.assert_unique(info, dk)
                bits = binaryToIntList(self.read_value())
                settings = {
                    16: "use_custom_tt_values",
                    17: "create_vdmx",
                    18: "add_null_cr_space",
                }
                info[dk] = [settings.get(i, str(i)) for i in bits]

            elif k in (0x3A, 0x3B, 0x3C, 0x3D, 0x3E, 0x3F):
                self.assert_unique(info, bk)
                info[bk] = self.read_value()

            elif k in (
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
                self.assert_unique(info, dk)
                info[dk] = self.read_value()

            elif k == 0x4C:  # PANOSE?
                self.assert_unique(info, dk)
                info[dk] = [self.read_uint8() for _ in range(10)]

            elif k in (0x4D, 0x4E, 0x4F, 0x50, 0x51, 0x52):
                self.assert_unique(info, dk)
                info[dk] = self.read_value()

            elif k == 0x53:
                self.assert_unique(info, dk)
                num_values = self.read_value()
                info[dk] = [self.read_uint8() for _ in range(num_values)]

            elif k == 0x54:
                # Codepages
                self.assert_unique(info, dk)
                info[dk] = [
                    self.read_value(signed=False),
                    self.read_value(signed=False),
                ]

            elif k == 0x56:
                # Timestamp, unsigned
                self.assert_unique(info, dk)
                info[dk] = self.read_value(signed=False)

            elif k in (0x57, 0x5C):
                self.assert_unique(info, dk)
                info[dk] = self.read_value()

            elif k == 0x58:
                self.assert_unique(info, hk)
                num_values = self.read_value()
                info[hk] = [self.read_uint8() for _ in range(num_values)]

            else:
                logger.warning(f"Unknown key in TrueType info: {hex(k)}")


class TrueTypeStemsParser(BaseParser):
    def _parse(self):
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            for _ in range(num_stems):
                width = self.read_value()
                stem_name_length = self.read_uint8()
                stem_name = self.stream.read(stem_name_length).decode("cp1252")
                ppm6 = self.read_value()

                direction.append(
                    {
                        "value": width,
                        "name": stem_name,
                        "round": {"6": ppm6},
                    }
                )
            result[names[i]] = direction

        return result


class TrueTypeStemPpemsParser(BaseParser):
    def _parse(self):
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            d = {}
            for j in range(num_stems):
                for k in range(2, 6):
                    ppm = self.read_value()
                    d[str(k)] = ppm

                direction.append(
                    {
                        "stem": j,
                        "round": d.copy(),
                    }
                )
            result[names[i]] = direction

        return result


class TrueTypeStemPpems1Parser(BaseParser):
    # PPEM 1 for each stem is stored in a separate entry ...
    def _parse(self):
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = (self.ttStemsV_count, self.ttStemsH_count)[i]
            if num_stems is None:
                raise ValueError

            for j in range(num_stems):
                ppm = self.read_value()
                direction.append(
                    {
                        "stem": j,
                        "round": {"1": ppm},
                    }
                )
            result[names[i]] = direction

        return result


class TrueTypeZoneDeltasParser(BaseParser):
    def _parse(self):
        num_deltas = self.read_value()
        result = {}
        for _ in range(num_deltas):
            # Index into Bottom + Top Zones
            index = self.read_value()
            ppm = self.read_value()
            shift = self.read_value()
            if index in result:
                result[index][ppm] = shift
            else:
                result[index] = {ppm: shift}

        return result


class TrueTypeZonesParser(BaseParser):
    def _parse(self):
        names = ("ttZonesT", "ttZonesB")
        result = {}
        for i in range(2):
            side = []
            num_zones = self.read_value()
            logger.debug(f"Zones: {num_zones}")
            for _ in range(num_zones):
                position = self.read_value()
                width = self.read_value()
                logger.debug(f"    pos: {position}, width: {width}")
                name_length = self.read_value()
                logger.debug(f"Name of length {name_length} follows")
                zone_name = self.read_str(name_length)
                side.append(
                    {
                        "position": position,
                        "value": width,
                        "name": zone_name,
                    }
                )
            result[names[i]] = side

        return result
