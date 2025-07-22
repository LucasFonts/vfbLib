from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Literal

# Used by guides and links
DIRECTIONS: Sequence[Literal["h", "v"]] = ("h", "v")

GLYPH_CONSTANT = (1, 9, 7, 1)
