from __future__ import annotations

import logging

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from vfbLib.typing import ClassFlagDict
    from vfbLib.ufo.typing import UfoGroups


logger = logging.getLogger(__name__)


def transform_groups(
    orig_groups: UfoGroups,
    kerning_class_flags: ClassFlagDict,
    glyphOrder: List[str],
    skip_missing_group_glyphs: bool,
) -> UfoGroups:
    # Rename kerning groups by applying the side flags and using the key
    # glyph for naming
    FIRST = 2**10
    SECOND = 2**11
    groups: UfoGroups = {}
    for name, glyphs in orig_groups.items():
        if name.startswith("_"):
            # Kerning group

            # Check for missing glyphs
            missing = [n for n in glyphs if n not in glyphOrder]
            num_missing = len(missing)
            num_glyphs = len(glyphs)
            if missing:
                if num_missing == num_glyphs:
                    logger.warning(
                        f"All glyphs in kerning group '{name}' are missing from "
                        f"the font: {', '.join(missing)}"
                    )
                else:
                    logger.warning(
                        f"{num_missing} of {num_glyphs} glyphs in kerning group "
                        f"'{name}' are missing from the font: {', '.join(missing)}"
                    )
                if skip_missing_group_glyphs:
                    glyphs = list(set(glyphs) - set(missing))
                    if not glyphs:
                        logger.warning("Not adding empty kerning group to the UFO.")
                        continue

            key_glyph = glyphs[0]  # Keyglyph is used for group name
            if key_glyph in missing:
                if num_missing != num_glyphs:
                    logger.warning(
                        f"Key glyph '{key_glyph}' for group '{name}' is missing "
                        "from the font."
                    )

            # Sort group glyphs by glyphOrder
            if not missing:
                glyphs.sort(key=lambda n: glyphOrder.index(n))

            if name in kerning_class_flags:
                flags = kerning_class_flags[name][0]
            else:
                flags = FIRST + SECOND
            for side, sidename in ((FIRST, 1), (SECOND, 2)):
                if flags & side:
                    ufoname = f"public.kern{sidename}.{key_glyph}"
                    if ufoname in groups:
                        logger.warning(f"Duplicate kern{sidename} group: {ufoname}")
                    else:
                        groups[ufoname] = glyphs
        else:
            # Pass non-kerning groups verbatim
            groups[name] = glyphs
    return groups
