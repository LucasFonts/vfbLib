from __future__ import annotations

import logging

from vfbLib.parsers.base import BaseParser
from vfbLib.typing import PrimaryInstanceDict

logger = logging.getLogger(__name__)


class AnisotropicInterpolationsParser(BaseParser):
    def _parse(self) -> list[list[tuple[int, int]]]:
        # The graph used for anisotropic interpolation maps, for all axes.
        values = []
        while True:
            axis_values = []
            try:
                n = self.read_value()
                axis_values = [(self.read_value(), self.read_value()) for _ in range(n)]
                values.append(axis_values)
            except EOFError:
                return values


class AxisMappingsCountParser(BaseParser):
    def _parse(self) -> list[int]:
        # An array of axis mapping counts per axis, for all 4 axes whether they exist
        # or not.
        # 0300 0000  0000 0000  0000 0000  0000 0000
        # -> [3, 0, 0, 0]
        return [self.read_uint32() for _ in range(4)]


class AxisMappingsParser(BaseParser):
    def _parse(self) -> list[tuple[float, float]]:
        # 10 pairs of (user, design) coordinates per axis.
        # Look at "Axis Mappings Count" to find out which mappings are used in each
        # axis.
        # The trailing unused fields may contain junk and must be ignored.
        mappings = []
        for _ in range(self.stream.getbuffer().nbytes // 16):
            src = self.read_double()
            tgt = self.read_double()
            mappings.append((src, tgt))

        return mappings


class MasterLocationParser(BaseParser):
    def _parse(self) -> tuple[int, tuple[float, float, float, float]]:
        # The location on all 4 axes for this master
        master_index = self.read_uint32()
        a1 = self.read_double()
        a2 = self.read_double()
        a3 = self.read_double()
        a4 = self.read_double()
        return master_index, (a1, a2, a3, a4)


class PrimaryInstancesParser(BaseParser):
    def _parse(self) -> list[PrimaryInstanceDict]:
        instances = []
        num_instances = self.read_value()
        for _ in range(num_instances):
            name = self.read_str_with_len()
            values = tuple(self.read_value() / 10000 for _ in range(4))
            instances.append(PrimaryInstanceDict(name=name, values=values))

        return instances
