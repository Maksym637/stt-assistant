from datetime import datetime


def to_iso_8601(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")
