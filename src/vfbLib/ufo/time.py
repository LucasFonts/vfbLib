from datetime import UTC, datetime

TIME_ZERO = 2082841200  # = 1970-01-01 00:00:00


def convert_timestamp(t: int) -> datetime:
    """
    Convert the FontLab timestamp to a datetime object.
    """
    b = t.to_bytes(4, signed=True)
    t = int.from_bytes(b, signed=False)

    # 1970-01-01 is the earliest timestamp in FL notation, enforce it
    if t < TIME_ZERO:
        t = TIME_ZERO

    return datetime.fromtimestamp(t - TIME_ZERO, UTC)


def datetime_to_fl(d: datetime) -> int:
    ts = int(datetime.timestamp(d))
    ts += TIME_ZERO

    if ts < TIME_ZERO:
        ts = TIME_ZERO
    else:
        b = ts.to_bytes(4, signed=False)
        ts = int.from_bytes(b, signed=True)
    return ts
