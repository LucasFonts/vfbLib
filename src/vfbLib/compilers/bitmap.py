from __future__ import annotations

import logging
from itertools import chain, groupby
from typing import TYPE_CHECKING

from vfbLib.compilers.base import BaseCompiler

if TYPE_CHECKING:
    from vfbLib.typing import BackgroundImageDict, BitmapDataDict, GlyphBitmapDict

logger = logging.getLogger(__name__)


class BaseBitmapCompiler(BaseCompiler):
    def _encode_bitmap(self, data: list[list[int]]) -> list[list[int]]:
        # Encode to the run-length-encoded format

        # Returns a list of lists in which the first element is the repetition specifier
        # and the rest of the values are the byte values.
        # A positive number means the following bytes should be used verbatim.
        # E.g.: [[3, 128, 128, 64, 32]]: Use the following 3 + 1 bytes verbatim
        # A negative first number means the following byte should be repeated.
        # The number of repetitions is -n + 1.
        # E.g. [[-2, 0]]: Use the 0 three times

        max_chunk_len = 128

        encoded = []
        buf: list[int] = []
        for value, expanded in groupby(chain.from_iterable(data)):
            d = list(expanded)
            count = len(d)
            if count > 2:
                # Repeated value

                # Flush the buffer before handling the repetition.
                # The buffer must be split into chunks of max. max_chunk_len (128)
                # values, because its length needs to be written as a signed int8
                # (len(buf) - 1) which has a maximum value of 127.
                for i in range(0, len(buf), max_chunk_len):
                    chunk = buf[i : i + max_chunk_len]
                    encoded.append([len(chunk) - 1] + chunk)
                buf = []
                # Write the repeated value.
                # It also needs to be split into chunks.
                full_chunks = count // max_chunk_len
                for _ in range(full_chunks):
                    encoded.append([-max_chunk_len + 1, value])
                partial_chunk_length = count % max_chunk_len
                if partial_chunk_length:
                    encoded.append([-partial_chunk_length + 1, value])
            else:
                # Verbatim values

                # The buffer must be written in chunks, but we take care of that when it
                # is flushed (see above).
                buf.extend(d)
        return encoded

    def _compile_bitmap_data(self, bitmap: BitmapDataDict) -> None:
        encoded = self._encode_bitmap(bitmap["data"])
        num_values = len(list(chain.from_iterable(encoded)))
        self.write_value(num_values)
        for entry in encoded:
            bytes_spec = entry.pop(0)
            self.write_int8(bytes_spec)
            for b in entry:
                self.write_uint8(b)


class BackgroundBitmapCompiler(BaseBitmapCompiler):
    def _compile(self, data: BackgroundImageDict) -> None:
        x, y = data["origin"]
        self.write_value(x)
        self.write_value(y)

        w, h = data["size_units"]
        self.write_value(w, signed=False)
        self.write_value(h, signed=False)

        w, h = data["size_pixels"]
        self.write_value(w, signed=False)
        self.write_value(h, signed=False)

        bitmap = data["bitmap"]
        self._compile_bitmap_data(bitmap)


class GlyphBitmapsCompiler(BaseBitmapCompiler):
    def _compile(self, data: list[GlyphBitmapDict]) -> None:
        self.write_value(len(data), signed=False)
        for d in data:
            self.write_value(d["ppm"], signed=False)
            x, y = d["origin"]
            self.write_value(x)
            self.write_value(y)

            w, h = d["adv"]
            self.write_value(w, signed=False)
            self.write_value(h, signed=False)

            w, h = d["size_pixels"]
            self.write_value(w, signed=False)
            self.write_value(h, signed=False)

            bitmap = d["bitmap"]
            self.write_value(1 + len(bitmap["data"]), signed=False)
            self._compile_bitmap_data(bitmap)
