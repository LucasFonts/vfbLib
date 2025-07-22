from __future__ import annotations

from vfbLib import export_options, opentype_export_options
from vfbLib.compilers.base import BaseCompiler
from vfbLib.helpers import intListToBinary


class ExportOptionsCompiler(BaseCompiler):
    def _compile(self, data: list[str]) -> None:
        rev = {v: k for k, v in export_options.items()}
        options = [rev[k] for k in data]
        self.write_uint16(intListToBinary(options))


class OpenTypeExportOptionsCompiler(BaseCompiler):
    def _compile(self, data: list[dict[str, int]]) -> None:
        rev = {v: k for k, v in opentype_export_options.items()}
        for opt in data:
            raw_key, v = tuple(opt.items())[0]
            if raw_key in rev:
                k = rev[raw_key]
            else:
                k = int(raw_key)
            self.write_uint8(k)
            self.write_value(v)
        self.write_uint8(0x64)
