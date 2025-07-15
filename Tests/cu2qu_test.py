import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Import of the function to test
from vfbLib.cu2qu import vfbcu2qu


def data_path():
    return Path(__file__).parent / "Data"


def vfb_path(name: str) -> Path:
    return data_path() / name


class Cu2quTest(unittest.TestCase):
    def test_vfbcu2qu(self):
        args = [
            "vfbcu2qu",
            str(vfb_path("cu2qu.vfb")),
            "-fo",
            "-p",
            str(data_path() / "out"),
        ]
        with patch.object(sys, "argv", args):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                vfbcu2qu()
            # with open(font_path("css")) as expected:
            #     assert f.getvalue() == expected.read()

    def test_vfbcu2qu_2_masters(self):
        args = [
            "vfbcu2qu",
            str(vfb_path("cu2qu_2m.vfb")),
            "-fo",
            "-p",
            str(data_path() / "out"),
        ]
        with patch.object(sys, "argv", args):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                vfbcu2qu()
            # with open(font_path("css")) as expected:
            #     assert f.getvalue() == expected.read()
