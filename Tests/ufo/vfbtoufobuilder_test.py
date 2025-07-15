from pathlib import Path
from unittest import TestCase

from vfbLib.ufo.builder import VfbToUfoBuilder


class TestVfb:
    pass


class VfbToUfoBuilderTest(TestCase):
    def test_get_master_path(self):
        ufo_path = Path("/") / "path" / "to" / "ufo" / "my_ufo.ufo"

        # First master without number
        master_path = VfbToUfoBuilder.get_master_path(ufo_path, 0)
        assert master_path == ufo_path

        # Second master with number
        master_path = VfbToUfoBuilder.get_master_path(ufo_path, 1)
        assert master_path == ufo_path.parent / "my_ufo-1.ufo"
