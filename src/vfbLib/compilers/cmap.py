from __future__ import annotations

from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import CustomCmap


class CustomCmapCompiler(BaseCompiler):
    def _compile(self, data: list[CustomCmap]) -> None:
        self.write_value(len(data))
        for cmap in data:
            for k in ("language_id", "platform_id", "encoding_id", "format", "option"):
                self.write_value(cmap[k])
            self.write_str_with_len(cmap["page_name"])
