from __future__ import annotations

import logging

from vfbLib.helpers import hexStr
from vfbLib.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class BinaryTableParser(BaseParser):
    def _parse(self) -> dict[str, str]:
        tag = self.read_str(4)
        data = hexStr(self.stream.read())
        return {"tag": tag, "data": data}
