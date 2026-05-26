import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vfbLib.typing import KerningClassFlagDict
    from vfbLib.ufo.typing import UfoGroups


logger = logging.getLogger(__name__)


def transform_groups(
    orig_groups: "UfoGroups",
    kerning_class_flags: "KerningClassFlagDict",
    glyphOrder: list[str],
    skip_missing_group_glyphs: bool = False,
) -> "tuple[UfoGroups, list[str], dict[str, str]]":
    """
    Transform the raw groups data, a dict of group name to a list of glyph names, which
    may reference glyphs not present in the font.

    The glyph name lists in orig_groups must be sorted so that the "key glyph" (a
    concept which does exist in VFB but not in UFO) is the first glyph.

    Kerning groups are renamed by looking up the side flags in `kerning_class_flags` and
    adding the appropriate `public.kern...` prefix.

    Missing glyphs are removed from groups, and if a group becomes empty, the whole
    group is omitted from the result. This clean-up can be controlled via
    `skip_missing_group_glyphs`.

    Args:
        orig_groups (UfoGroups): The unprocessed groups.
        kerning_class_flags (KerningClassFlagDict): The dict containing information
            about which side of the kerning pair a group pertains to.
        glyphOrder (list[str]): The glyph order of the font. It is used to remove any
            glyphs that are not present in the font from the groups.
        skip_missing_group_glyphs (bool, optional): Whether do omit glyphs that are not
            present in the font from the resulting groups. Empty groups are omitted as
            well.Defaults to False.

    Returns:
        tuple[UfoGroups, list[str], dict[str, str]]: The groups for the UFO, the
            original group order, and a dict of group_name to key glyph name.
    """
    FIRST = 2**10
    SECOND = 2**11
    groups: "UfoGroups" = {}
    group_order = []
    key_glyphs: dict[str, str] = {}
    for name, glyphs in orig_groups.items():
        # Find key glyph(s)
        group_key_glyphs = [g.strip("'") for g in glyphs if g.endswith("'")]
        other_group_glyphs = [g for g in glyphs if not g.endswith("'")]

        is_kerning = name.startswith("_")
        num_keyglyphs = len(group_key_glyphs)
        if (is_kerning and num_keyglyphs != 1) or (
            not is_kerning and num_keyglyphs != 0
        ):
            # Kerning groups should have one key glyph
            # Other groups should have no key glyph
            logger.warning(
                f"Unexpected number of key glyphs in group {name}: {group_key_glyphs}"
            )
        glyphs = group_key_glyphs + other_group_glyphs

        # Check for missing glyphs
        missing = [n for n in glyphs if n not in glyphOrder]
        num_missing = len(missing)
        num_glyphs = len(glyphs)
        if missing:
            if num_missing == num_glyphs:
                logger.warning(
                    f"All glyphs in group '{name}' are missing from "
                    f"the font: {', '.join(missing)}"
                )
            else:
                logger.warning(
                    f"{num_missing} of {num_glyphs} glyphs in group "
                    f"'{name}' are missing from the font: {', '.join(missing)}"
                )
            if skip_missing_group_glyphs:
                remaining_glyphs = list(set(glyphs) - set(missing))
                if not remaining_glyphs:
                    logger.warning(f"Not adding empty group '{name}' to the UFO.")
                    continue
                glyphs = [g for g in glyphs if g not in missing]

        key_glyph = None
        if group_key_glyphs:
            logger.info(
                f"Looking for key glyph in {group_key_glyphs} for group {name} ({glyphs})"
            )
        for key_glyph_candidate in group_key_glyphs:
            if key_glyph_candidate in missing and num_missing != num_glyphs:
                # Only warn if not all group glyphs are missing from the font
                logger.warning(
                    f"Key glyph '{key_glyph}' for group '{name}' is missing "
                    "from the font."
                )
            else:
                key_glyph = key_glyph_candidate
                logger.info(
                    f"Selected key glyph {key_glyph} for group {name} ({glyphs})"
                )
                break

        # The final name in the UFO is different for kerning groups, which also must be
        # split per side of the kerning pair
        final_name = name
        if name.startswith("_"):
            # The group is a kerning group, build a valid UFO name in `final_name`
            if name in kerning_class_flags:
                flags = kerning_class_flags[name][0]
            else:
                # Don't add kerning groups without a side flag, as FLS ignores them when
                # compiling the kern feature
                logger.warning(f"Skipping kerning group without side flag: '{name}'")
                continue

            for side, sidename in ((FIRST, 1), (SECOND, 2)):
                if flags & side:
                    # Add a group for each side that applies
                    final_name = f"public.kern{sidename}.{name}"
                    if final_name in groups:
                        logger.warning(
                            f"Skipping duplicate kern{sidename} group: {final_name}"
                        )
                        continue

                    if final_name in key_glyphs:
                        if key_glyphs[final_name] != key_glyph:
                            logger.warning(
                                f"Ignoring duplicate group '{final_name}' with different "
                                f"key glyphs: {key_glyphs[final_name]} vs. {key_glyph}."
                            )
                    elif key_glyph is not None:
                        key_glyphs[final_name] = key_glyph
                    groups[final_name] = glyphs
                    group_order.append(final_name)
            continue

        # Non-kerning group, may still have a key glyph
        # (https://github.com/LucasFonts/vfbLib/issues/258)
        if final_name in key_glyphs:
            if key_glyphs[final_name] != key_glyph:
                logger.warning(
                    f"Ignoring duplicate group '{final_name}' with different "
                    f"key glyphs: {key_glyphs[final_name]} vs. {key_glyph}."
                )
        elif key_glyph is not None:
            key_glyphs[final_name] = key_glyph
        groups[final_name] = glyphs
        group_order.append(final_name)

    return groups, group_order, key_glyphs


def build_glyph_to_group_maps(
    groups: "UfoGroups",
) -> "tuple[UfoGroups, dict[str, str], dict[str, str]]":
    glyph_group_1: dict[str, str] = {}
    glyph_group_2: dict[str, str] = {}
    for group in groups.items():
        name, glyphs = group
        if name.startswith("public.kern1"):
            for g in glyphs:
                if g in glyph_group_1:
                    logger.error(
                        f"Multiple kerning groups (kern1) for glyph {g}: "
                        f"{glyph_group_1[g]}, {name}. New group ignored."
                    )
                    continue
                glyph_group_1[g] = name
        elif name.startswith("public.kern2"):
            for g in glyphs:
                if g in glyph_group_2:
                    logger.error(
                        f"Multiple kerning groups (kern2) for glyph {g}: "
                        f"{glyph_group_2[g]}, {name}. New group ignored."
                    )
                    continue
                glyph_group_2[g] = name
    # Rebuild groups to get rid of duplicate kerning groups per glyph and side.
    groups = rebuild_kerning_groups(groups, glyph_group_1, glyph_group_2)
    return groups, glyph_group_1, glyph_group_2


def _build_groups(glyph_to_group_mapping: dict[str, str]) -> "UfoGroups":
    groups: "UfoGroups" = {}
    for name, group in glyph_to_group_mapping.items():
        if group in groups:
            groups[group].append(name)
        else:
            groups[group] = [name]
    return groups


def rebuild_kerning_groups(
    groups: "UfoGroups", glyph_group_1: dict[str, str], glyph_group_2: dict[str, str]
) -> "UfoGroups":
    """
    Rebuild the kerning groups from the left and right side glyph to group mappings.
    This should get rid of any duplicate groups per glyph.
    """
    # Filter groups so only non-kerning groups are kept
    new_groups: "UfoGroups" = {
        n: g for n, g in groups.items() if not n.startswith("public.kern")
    }
    new_groups.update(_build_groups(glyph_group_1))
    new_groups.update(_build_groups(glyph_group_2))
    return new_groups
