from __future__ import annotations

import logging

from vfbLib import export_options, opentype_export_options
from vfbLib.helpers import binaryToIntList
from vfbLib.parsers.base import BaseParser, EncodedKeyValuesParser

logger = logging.getLogger(__name__)


class ExportOptionsParser(BaseParser):
    """
    A parser that reads data a bit field representing export options.
    """

    def _parse(self) -> list[str | int]:
        val = self.read_uint16()
        bits = binaryToIntList(val)
        options = [export_options.get(i, i) for i in bits]
        return options


class OpenTypeExportOptionsParser(EncodedKeyValuesParser):
    def _parse(self) -> list[dict[str | int, str]]:
        final = []
        for d in super()._parse():
            assert len(d) == 1
            k, v = tuple(d.items())[0]
            final.append({opentype_export_options.get(k, k): v})
        return final
