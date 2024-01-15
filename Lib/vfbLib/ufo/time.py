from __future__ import annotations

from datetime import datetime
from datetime import UTC


TIME_ZERO = 2082841200


def convert_timestamp(t: int) -> datetime:
    """
    Convert the FontLab timestamp to a datetime object.
    """
    # 1970-01-01 is the earliest timestamp in FL notation, enforce it
    if t < TIME_ZERO:
        t = TIME_ZERO

    return datetime.fromtimestamp(t - TIME_ZERO, UTC)
