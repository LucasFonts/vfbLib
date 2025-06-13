from __future__ import annotations

import logging
from collections.abc import Iterable
from pathlib import Path
from time import time
from typing import TYPE_CHECKING, Any

from vfbLib.vfb.entry import VfbEntry
from vfbLib.vfb.glyph import VfbGlyph, VfbGlyphMaster
from vfbLib.vfb.header import VfbHeader
from vfbLib.vfb.info import VfbInfo

if TYPE_CHECKING:
    from io import BufferedReader

    from vfbLib.typing import VfbDict


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
        vfb_path: Path | None = None,
        timing=True,
        minimal=False,
        drop_keys: set[str] | None = None,
        only_header=False,
        unicode_strings=False,
    ) -> None:
        self.vfb_path = vfb_path
        self.timing = timing
        self.minimal = minimal
        if drop_keys is None:
            self.drop_keys = set()
        else:
            self.drop_keys = set(drop_keys)
        self.only_header = only_header
        # String encoding for nametable entries
        self.encoding = "utf-8" if unicode_strings else "cp1252"

        # We need some minimal API to make pen access work ...
        self._glyphs: dict[str, VfbGlyph] = {}
        self.glyph_order: list[str] = []

        # cu2qu accesses the info and lib ...
        self.info = VfbInfo(vfb=self)
        self.lib: dict[str, Any] = {}

        self.master_index = 0
        self.num_masters: int = 0
        self.ttStemsV_count: int = 0
        self.ttStemsH_count: int = 0

        self.ps_hinting_options: VfbEntry | None = None

        # Track decompile errors
        self.any_errors = False
        if self.vfb_path:
            self.read()
        else:
            self.header: VfbHeader = VfbHeader()
            self.entries: list[VfbEntry] = []

    def add_entry(self, entry: VfbEntry) -> None:
        """Add an entry to the Vfb. Also sets the parent of the entry to the Vfb.

        Args:
            entry (VfbEntry): The VfbEntry to be added to Vfb.entries.
        """
        entry.vfb = self
        self.entries.append(entry)

    def as_dict(self) -> VfbDict:
        """
        Return the Vfb structure as Dict, e.g. for saving as JSON. The dict has the keys
        "header" and "entries".
        """
        d: VfbDict = {"header": {}, "entries": []}
        if self.header is not None:
            d["header"] = self.header.as_dict()
        if self.entries:
            d["entries"] = [e.as_dict() for e in self.entries]
        return d

    def clear(self) -> None:
        """
        Clear any data that may have been read before.
        """
        self.header = VfbHeader()
        self.entries = []

    def _decompile_glyphs(self) -> None:
        name = None
        for entry in self.entries:
            if entry.key == "Glyph":
                glyph = VfbGlyph(entry, self)
                name = glyph.decompile()
                i = 1
                # Disambiguate duplicate names
                if name in self._glyphs:
                    logger.error(f"VFB contains duplicate glyph name: {name}")
                    while f"{name}#{i}" in self._glyphs:
                        i += 1
                    name = f"{name}#{i}"
                self._glyphs[name] = glyph
                self.glyph_order.append(name)
            elif entry.key == "Links":
                # We need to store the links of the glyph for converting links to
                # PS hints before writing charstrings
                entry.decompile()
                if name is None:
                    logger.error("Links entry without preceding glyph entry")
                else:
                    self._glyphs[name].links_entry = entry
            elif entry.key == "Glyph Hinting Options":
                # We need this to decide if we should generate hstem3/vstem3 hints
                entry.decompile()
                if name is None:
                    logger.error(
                        "Glyph Hinting Options entry without preceding glyph entry"
                    )
                else:
                    self._glyphs[name].ps_hinting_options = entry
            elif entry.key == "PostScript Hinting Options":
                # We need this to decide if we should generate flex hints
                entry.decompile()
                self.ps_hinting_options = entry

    def __contains__(self, key: str) -> bool:
        if not self._glyphs:
            self._decompile_glyphs()
        return key in self._glyphs

    def __getitem__(self, key: str) -> VfbGlyph:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs[key]

    def getGlyphMaster(self, key: str, master_index: int) -> VfbGlyphMaster:
        return VfbGlyphMaster(self[key], master_index)

    def get_masters(self) -> list[VfbMaster]:
        return [VfbMaster(self, i) for i in range(self.num_masters)]

    def decompile(self) -> None:
        """
        Decompile all entries, except for the ones listed in `drop_keys`.
        """
        self.any_errors = False
        start = time()
        for entry in self.entries:
            if entry.key in self.drop_keys:
                continue

            entry.decompile()

        end = time()
        if self.timing:
            print(f"Interpreting binary data took {round((end - start) * 1000)} ms.")

    def items(self) -> Iterable[tuple[str, VfbGlyph]]:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs.items()

    def keys(self) -> Iterable[str]:
        if not self._glyphs:
            self._decompile_glyphs()
        return self._glyphs.keys()

    def read_stream(self, stream: BufferedReader) -> None:
        """
        Lazily read and parse the vfb stream, i.e. parse the header, but only read the
        binary data of other entries.
        """
        start = time()
        self.header = VfbHeader()
        self.header.read(stream)
        if self.only_header:
            return

        entry: VfbEntry | None = None
        while True:
            try:
                entry = VfbEntry(self)
                entry.read(stream)
            except EOFError:
                break

            # Some info needs to be stored for later access, so we decompile a selection
            # of entries right here.

            if entry is not None:
                if entry.key == "Master Count":
                    entry.decompile()
                    if entry.decompiled is not None:
                        if TYPE_CHECKING:
                            assert isinstance(entry.decompiled, int)
                        self.num_masters = entry.decompiled
                        entry.clean()  # Suppress warning about double decompilation

                elif entry.key == "TrueType Stems":
                    entry.decompile()
                    if entry.decompiled is not None:
                        if TYPE_CHECKING:
                            assert isinstance(entry.decompiled, dict)
                        self.ttStemsV_count = len(entry.decompiled.get("ttStemsV", []))
                        self.ttStemsH_count = len(entry.decompiled.get("ttStemsH", []))
                        entry.clean()  # Suppress warning about double decompilation

                if entry.key not in self.drop_keys:
                    self.entries.append(entry)

        end = time()
        if self.timing:
            print(
                "Source file was successfully read in "
                f"{round((end - start) * 1000)} ms."
            )

    def read(self) -> None:
        """
        Read data from the file at vfb_path, without decompiling
        """
        self.clear()
        if self.vfb_path is None:
            return

        with open(self.vfb_path, "rb") as vfb:
            self.read_stream(vfb)

    def write(self, out_path: Path) -> None:
        """
        Compile any entries with changes, and write the VFB to out_path.
        """
        if self.header is None:
            raise ValueError

        with open(out_path, "wb") as vfb:
            self.header.compile()
            assert self.header.data is not None
            vfb.write(self.header.data)

            for entry in self.entries:
                success = entry.compile()
                if not success:
                    logger.warning(
                        f"Could not compile entry {entry.key} ({entry.id}): "
                        f"{entry.decompiled}"
                    )
                    # raise NotImplementedError
                vfb.write(entry.header)
                if entry.data is not None:
                    # There may be entries without data
                    vfb.write(entry.data)
            # File end marker
            vfb.write(b"\05\00\00\00\02\00\00\00")


class VfbMaster:
    """
    Minimal UFO interface for a single master of a multiple master VFB.
    """

    def __init__(self, vfb: Vfb, master_index: int = 0):
        self.vfb = vfb
        self.master_index = master_index

    def __contains__(self, key: str) -> bool:
        return key in self.vfb

    def __getitem__(self, key: str) -> VfbGlyphMaster:
        return self.vfb.getGlyphMaster(key, self.master_index)

    @property
    def glyph_order(self) -> list[str]:
        return self.vfb.glyph_order

    @property
    def info(self) -> VfbInfo:
        return self.vfb.info

    def items(self) -> Iterable[tuple[str, VfbGlyph]]:
        return self.vfb.items()

    def keys(self) -> Iterable[str]:
        return self.vfb.keys()

    @property
    def num_masters(self) -> int:
        return self.vfb.num_masters

    @property
    def ps_hinting_options(self) -> VfbEntry | None:
        return self.vfb.ps_hinting_options
