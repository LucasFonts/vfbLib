import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

# Import of the function to test
from vfbLib.cmdline import vfb2json, vfb2ufo


def data_path():
    return Path(__file__).parent / "Data"


def vfb_path(name: str) -> Path:
    return data_path() / name


class CmdlineTest(unittest.TestCase):
    def test_vfb2json(self):
        args = [
            "vfb2json",
            str(vfb_path("masters.vfb")),
            "-p",
            str(data_path() / "out"),
        ]
        with patch.object(sys, "argv", args):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                vfb2json()
            # with open(font_path("css")) as expected:
            #     assert f.getvalue() == expected.read()

    def test_vfb2ufo(self):
        args = [
            "vfb3ufo",
            str(vfb_path("masters.vfb")),
            "-fo",
            "-p",
            str(data_path() / "out"),
        ]
        with patch.object(sys, "argv", args):
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                vfb2ufo()
            # with open(font_path("css")) as expected:
            #     assert f.getvalue() == expected.read()
