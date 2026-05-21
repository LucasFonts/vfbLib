from unittest import TestCase

from vfbLib.vfb.vfb import Vfb


class SmokeTest(TestCase):
    vfb = Vfb()
    assert isinstance(vfb, Vfb)
