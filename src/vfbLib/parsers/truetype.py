from __future__ import annotations

import logging
from struct import unpack

from vfbLib import tt_settings, ttinfo_names
from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser
from vfbLib.typing import (
    FlagsOptionsDict,
    GaspList,
    TTStemDict,
    TTStemsDict,
    TTZoneDict,
    TTZonesDict,
    VdmxRecDict,
)

logger = logging.getLogger(__name__)


def convert_int_to_flags_options(value: int) -> FlagsOptionsDict:
    flags = binaryToIntList(value & 0xFFFF)
    options = binaryToIntList(value >> 16)
    return {
        "flags": flags,
        "options": [tt_settings.get(i, str(i)) for i in options],
    }


class GaspParser(BaseParser):
    """
    A parser that reads data as an array representing Gasp table values.
    """

    def _parse(self) -> GaspList:
        data = self.stream.read()
        gasp = unpack(f"<{len(data) // 2}H", data)
        it = iter(gasp)
        return [
            {
                "maxPpem": a,
                "flags": b,
            }
            for a, b in zip(it, it)
        ]


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
        info = {}

        while True:
            k = self.read_uint8()
            bk = ttinfo_names.get(k, f"bit{k}")  # dict key, as a bit number
            dk = ttinfo_names.get(k, str(k))  # dict key, human-readable
            hk = ttinfo_names.get(k, hex(k))  # dict key, hex

            if k == 0x32:
                return info

            elif k in (0x33, 0x34, 0x35, 0x36, 0x37, 0x38):
                self.assert_unique(info, dk)
                info[dk] = self.read_value()

            elif k == 0x39:
                # Options and head flags
                self.assert_unique(info, dk)
                info[dk] = convert_int_to_flags_options(self.read_value())

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

            elif k in (0x56, 0x57):
                # 0x56: head_creation
                # 0x57: value 2 of the list that FL5 returns for ttinfo.head_creation
                # The timestamps are returned by the FL5 API as signed, so for current
                # dates they have wrapped to a negative number.
                self.assert_unique(info, dk)
                # We read the number as unsigned anyway
                info[dk] = self.read_value(signed=False)

            elif k == 0x5C:
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
        result = TTStemsDict(ttStemsV=[], ttStemsH=[])
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            for _ in range(num_stems):
                width = self.read_value()
                stem_name_length = self.read_uint8()
                stem_name = self.stream.read(stem_name_length).decode(self.encoding)
                ppm6 = self.read_value()

                direction.append(
                    TTStemDict(value=width, name=stem_name, round={6: ppm6})
                )

            result[names[i]] = direction

        return result


class TrueTypeStemPpemsParser(BaseParser):
    def _parse(self) -> TTStemsDict:
        names = ("ttStemsV", "ttStemsH")
        result = TTStemsDict(ttStemsV=[], ttStemsH=[])
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            d = {}
            for j in range(num_stems):
                for k in range(2, 6):
                    ppm = self.read_value()
                    d[k] = ppm

                direction.append(TTStemDict(stem=j, round=d.copy()))

            result[names[i]] = direction

        return result


class TrueTypeStemPpems1Parser(BaseParser):
    # PPEM 1 for each stem is stored in a separate entry ...
    def _parse(self) -> TTStemsDict:
        names = ("ttStemsV", "ttStemsH")
        result = TTStemsDict(ttStemsV=[], ttStemsH=[])
        for i in range(2):
            direction = []
            num_stems = (self.ttStemsV_count, self.ttStemsH_count)[i]
            if num_stems is None:
                raise ValueError

            for j in range(num_stems):
                ppm = self.read_value()
                direction.append(TTStemDict(stem=j, round={1: ppm}))

            result[names[i]] = direction

        return result


class TrueTypeStemPpems23Parser(BaseParser):
    # PPEM 2 and 3 for each stem are stored in a separate entry ... sometimes!?
    def _parse(self):
        names = ("ttStemsV", "ttStemsH")
        result = TTStemsDict(ttStemsV=[], ttStemsH=[])
        for i in range(2):
            direction = []
            num_stems = self.read_value()
            if num_stems is None:
                raise ValueError

            for j in range(num_stems):
                ppm2 = self.read_value()
                ppm3 = self.read_value()
                direction.append(TTStemDict(stem=j, round={2: ppm2, 3: ppm3}))

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
        result = TTZonesDict(ttZonesT=[], ttZonesB=[])
        for i in range(2):
            side = []
            num_zones = self.read_value()
            logger.debug(f"Zones: {num_zones}")
            for _ in range(num_zones):
                position = self.read_value()
                width = self.read_value()
                zone_name = self.read_str_with_len()
                side.append(TTZoneDict(position=position, value=width, name=zone_name))

            result[names[i]] = side

        return result


class VdmxParser(BaseParser):
    def _parse(self) -> list[VdmxRecDict]:
        result = []
        num_records = self.read_value()
        for _ in range(num_records):
            rec = {}
            rec["pelHeight"] = self.read_value()
            rec["max"] = self.read_value()
            rec["min"] = self.read_value()
            result.append(rec)

        return result
