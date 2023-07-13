from __future__ import annotations

import logging

from pathlib import Path
from time import time
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Tuple
from vfbLib.vfb.glyph import VfbGlyph
from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.header import VfbHeader

if TYPE_CHECKING:
    from io import BufferedReader


logger = logging.getLogger(__name__)


# Convenience objects for vfb access


class Vfb:
    """
    Object to represent the vfb data, with the ability to read and write. You can use
    the Vfb object to access glyphs through dict methods, where the glyph name is the
    key and the glyph object is the value.
    """

    def __init__(
        self,
        vfb_path: Path,
        timing=True,
        minimal=False,
        only_keys: List[str] | None = None,
        only_header=False,
    ) -> None:
        self.vfb_path = vfb_path
        self.timing = timing
        self.minimal = minimal
        if only_keys is None:
            self.only_keys = []
        else:
            self.only_keys = only_keys
        self.only_header = only_header

        # We need some minimal API to make pen access work ...
        self._glyphs: Dict[str, VfbGlyph] = {}
        self.glyph_order: List[str] = []

        self.read()

    def as_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Return the Vfb structure as Dict, e.g. for saving as JSON. The dict has the keys
        "header" and "entries".
        """
        d = {}
        if self.header is not None:
            d["header"] = self.header.as_dict()
        if self.entries:
            d["entries"] = [e.as_dict() for e in self.entries]
        return d

    def clear(self):
        """
        Clear any data that may have been read before.
        """
        self.header: VfbHeader | None = None
        self.entries: List[VfbEntry] = []

    def _decompile_glyphs(self):
        for entry in self.entries:
            if entry.key == "Glyph":
                glyph = VfbGlyph(entry, self)
                name = glyph.decompile()
                if name in self._glyphs:
                    logger.error(f"VFB contains duplicate glyph name: {name}")
                    # FIXME: Disambiguate duplicate names
                self._glyphs[name] = glyph
                self.glyph_order.append(name)

    def __getitem__(self, key: str) -> VfbGlyph:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs[key]

    def items(self) -> Iterable[Tuple[str, VfbGlyph]]:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs.items()

    def keys(self) -> Iterable[str]:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs.keys()

    def parse(self, stream: BufferedReader):
        """
        Lazily parse the vfb stream, i.e. parse the header, but only read the binary
        data of other entries.
        """
        start = time()
        self.header = VfbHeader()
        self.header.read(stream)
        if self.only_header:
            return

        entry: VfbEntry | None = None
        while True:
            try:
                entry = VfbEntry()
                entry.read(stream)
            except EOFError:
                break

            if entry is not None:
                self.entries.append(entry)

        end = time()
        if self.timing:
            print(
                "Source file was successfully imported in",
                round((end - start) * 1000),
                "ms.",
            )

    def read(self):
        """
        Read data from the file at vfb_path, without decompiling
        """
        self.clear()
        with open(self.vfb_path, "rb") as vfb:
            self.parse(vfb)

    def write(self, out_path: Path) -> None:
        """
        Compile any entries with changes, and write the VFB to out_path.
        """
        if self.header is None:
            raise ValueError

        with open(out_path, "wb") as vfb:
            if self.header.modified:
                self.header.compile()
            assert self.header.data
            vfb.write(self.header.data)

            for entry in self.entries:
                if entry.modified:
                    entry.compile()
                vfb.write(entry.header)
                vfb.write(entry.data)
            # File end marker
            vfb.write(b"\05\00\00\00\02\00\00\00")