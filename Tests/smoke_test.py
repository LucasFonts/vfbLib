from unittest import TestCase

from vfbLib.vfb.vfb import Vfb


class SmokeTest(TestCase):
    def test_init(self) -> None:
        vfb = Vfb()
        assert isinstance(vfb, Vfb)
