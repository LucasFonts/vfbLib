from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase

from vfbLib.vfb.vfb import Vfb

empty_vfb_path = Path(__file__).parent.parent / "Data" / "empty_522.vfb"


class VfbGlyphTest(TestCase):
    def test_read_from_file(self) -> None:
        vfb = Vfb(empty_vfb_path)
        assert isinstance(vfb, Vfb)

    def test_read_from_io(self) -> None:
        buf = BytesIO()
        with open(empty_vfb_path, "rb") as f:
            buf.write(f.read())
        buf.seek(0)
        vfb = Vfb()
        vfb.read_bytes(buf)
        assert isinstance(vfb, Vfb)

    def test_write_to_file(self) -> None:
        buf = BytesIO()
        with open(empty_vfb_path, "rb") as f:
            buf.write(f.read())
        buf.seek(0)
        vfb = Vfb()
        vfb.read_bytes(buf)
        assert isinstance(vfb, Vfb)

        try:
            # Python 3.12+
            with NamedTemporaryFile(delete_on_close=True) as f:
                path = Path(f.name)
                vfb.write(path)
        except TypeError:
            # Python 3.11
            with NamedTemporaryFile(delete=False) as f:
                path = Path(f.name)
                vfb.write(path)
            path.unlink(missing_ok=True)

    def test_write_to_io(self) -> None:
        buf = BytesIO()
        with open(empty_vfb_path, "rb") as f:
            buf.write(f.read())
        buf.seek(0)
        vfb = Vfb()
        vfb.read_bytes(buf)
        assert isinstance(vfb, Vfb)

        out = BytesIO()
        vfb.write_bytes(out)
        out.seek(0)
