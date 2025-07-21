from __future__ import annotations

from typing import Any

from vfbLib.compilers.base import BaseCompiler


class AnisotropicInterpolationsCompiler(BaseCompiler):
    # FIXME: Untested
    def _compile(self, data: Any) -> None:
        for axis_mappings in data:
            self.write_value(len(axis_mappings))
            for src, tgt in axis_mappings:
                self.write_value(src)
                self.write_value(tgt)


class AxisMappingsCountCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for value in data:
            self.write_uint32(value)


class AxisMappingsCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        for src, tgt in data:
            self.write_double(src)
            self.write_double(tgt)


class MasterLocationCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        master_index, location = data
        self.write_uint32(master_index)
        self.write_doubles(location)


class PrimaryInstancesCompiler(BaseCompiler):
    def _compile(self, data: Any) -> None:
        # FIXME: Untested
        self.write_value(len(data))
        for instance in data:
            name = instance["name"]
            self.write_str_with_len(name)
