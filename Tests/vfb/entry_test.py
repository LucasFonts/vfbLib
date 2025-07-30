import warnings
from unittest import TestCase

from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.vfb import Vfb


class VfbTest(TestCase):
    def test_deprecation(self):
        vfb = Vfb()
        e = VfbEntry(parent=vfb)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # VfbEntry.decompiled is deprecated
            e.decompiled
            assert len(w) == 1
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "deprecated" in str(w[-1].message)
