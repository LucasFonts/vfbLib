from __future__ import annotations

import logging

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from fontTools.designspaceLib import (
        AxisDescriptor,
        DiscreteAxisDescriptor,
    )


def get_ds_master_location(
    axes: List[AxisDescriptor | DiscreteAxisDescriptor], vfb_location: List[float]
) -> Dict[str, float]:
    ds_location: Dict[str, float] = {}
    for i in range(len(axes)):
        axis = axes[i]
        if axis.name:
            ds_location[axis.name] = 1000 * vfb_location[i]
        else:
            raise ValueError(f"Axis doesn't have a name: {axis}")
    return ds_location
