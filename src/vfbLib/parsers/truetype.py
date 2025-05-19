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
            0x33: "max_zones",
            0x34: "max_twilight_points",
            0x35: "max_storage",
            0x36: "max_function_defs",
            0x37: "max_instruction_defs",
            0x38: "max_stack_elements",
            0x39: "head_flags",  # tt_font_info_settings with head flags combined
            0x3A: "head_units_per_em",  # units_per_em, duplicate
            0x3B: "head_mac_style",
            0x3C: "head_lowest_rec_ppem",  # lowest_rec_ppem
            0x56: "head_creation",  # timestamp
            0x57: "0x57",  # TODO: head_modification (not in API)?
            0x3D: "head_font_direction_hint",  # font_direction_hint
            0x3E: "os2_us_weight_class",  # weight_class, duplicate
            0x3F: "os2_us_width_class",  # width_class, duplicate
            0x40: "os2_fs_type",  # embedding
            0x41: "os2_y_subscript_x_size",  # subscript_x_size
            0x42: "os2_y_subscript_y_size",  # subscript_y_size
            0x43: "os2_y_subscript_x_offset",  # subscript_x_offset
            0x44: "os2_y_subscript_y_offset",  # subscript_y_offset
            0x45: "os2_y_superscript_x_size",  # superscript_x_size
            0x46: "os2_y_superscript_y_size",  # superscript_y_size
            0x47: "os2_y_superscript_x_offset",  # superscript_x_offset
            0x48: "os2_y_superscript_y_offset",  # superscript_y_offset
            0x49: "os2_y_strikeout_size",  # strikeout_size
            0x4A: "os2_y_strikeout_position",  # strikeout_position
            0x4B: "os2_s_family_class",  # ibm_classification + subclass
            0x4C: "OpenTypeOS2Panose",
            0x4D: "os2_s_typo_ascender",  # OpenTypeOS2TypoAscender
            0x4E: "os2_s_typo_descender",  # OpenTypeOS2TypoDescender
            0x4F: "os2_s_typo_line_gap",  # OpenTypeOS2TypoLineGap
            0x50: "os2_fs_selection",
            0x51: "os2_us_win_ascent",  # OpenTypeOS2WinAscent
            0x52: "os2_us_win_descent",  # OpenTypeOS2WinDescent
            0x5C: "Average Width",
            0x53: "Hdmx PPMs 1",
            0x58: "Hdmx PPMs 2",
            # os2_ul_code_page_range1, os2_ul_code_page_range2:
            0x54: "Codepages",
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
                # Options and head flags
                self.assert_unique(info, dk)
                all_bits = self.read_value()
                flags = binaryToIntList(all_bits & 0xFFFF)
                options = binaryToIntList(all_bits >> 16)

                settings = {
                    0: "use_custom_tt_values",
                    1: "create_vdmx",
                    2: "add_null_cr_space",
                }
                info[dk] = {
                    "flags": flags,
                    "options": [settings.get(i, i) for i in options],
                }

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
                range1 = self.read_value(signed=False)
                range2 = self.read_value(signed=False)
                info[dk] = {
                    "os2_ul_code_page_range1": range1,
                    "os2_ul_code_page_range2": range2,
                }

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


class TrueTypeStemPpems23Parser(BaseParser):
    # PPEM 2 and 3 for each stem are stored in a separate entry ... sometimes!?
    def _parse(self):
        names = ("ttStemsV", "ttStemsH")
        result = {}
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            if num_stems is None:
                raise ValueError

            for j in range(num_stems):
                ppm2 = self.read_value()
                ppm3 = self.read_value()
                direction.append(
                    {
                        "stem": j,
                        "round": {"2": ppm2, "3": ppm3},
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


class VdmxParser(BaseParser):
    def _parse(self):
        result = []
        num_records = self.read_value()
        for _ in range(num_records):
            rec = {}
            rec["pelHeight"] = self.read_value()
            rec["max"] = self.read_value()
            rec["min"] = self.read_value()
            result.append(rec)

        return result
