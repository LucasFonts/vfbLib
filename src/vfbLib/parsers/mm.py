import logging
from typing import Any

from vfbLib.parsers.base import BaseParser

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
            src_tgt = self.read_doubles(2)
            mappings.append(src_tgt)

        return mappings


class MasterLocationParser(BaseParser):
    def _parse(self) -> tuple[int, tuple[Any]]:
        # The location on all 4 axes for this master
        # FIXME: Might also be 2 uint16:
        master_index = self.read_uint32()
        flags = self.read_doubles(4)
        return master_index, flags


class PrimaryInstancesParser(BaseParser):
    def _parse(self) -> list[dict[str, Any]]:
        instances = []
        num_instances = self.read_value()
        for _ in range(num_instances):
            name_length = self.read_value()
            name = self.read_str(name_length)
            values = [self.read_value() / 10000 for _ in range(4)]
            instances.append({"name": name, "values": values})

        return instances
