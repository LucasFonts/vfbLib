from __future__ import annotations

import logging

from vfbLib.helpers import binaryToIntList
from vfbLib.parsers import BaseParser


logger = logging.getLogger(__name__)


class ExportOptionsParser(BaseParser):
    """
    A parser that reads data a bit field representing export options.
    """

    @classmethod
    def _parse(cls):
        names = {
            0: "use_custom_opentype_export_options",
            # 1: "use_default_opentype_export_options",
            2: "use_custom_cmap_encoding",
        }
        val = cls.read_uint16()
        bits = binaryToIntList(val)
        options = [names.get(i, str(i)) for i in bits]
        return options
