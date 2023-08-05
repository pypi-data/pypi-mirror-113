import datetime
import decimal
import enum
from itertools import chain
from uuid import UUID

from sqlalchemy import MetaData


def merge_metadata(*metadata_set: MetaData):
    m = MetaData()
    for table in chain.from_iterable(
        [metadata.tables.values() for metadata in metadata_set]
    ):
        table.tometadata(m)

    return m


def can_json(value):
    if isinstance(value, datetime.datetime):
        r = value.isoformat()
        if value.microsecond:
            r = r[:23] + r[26:]
        return r
    elif isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, datetime.time):
        assert value.utcoffset() is None, "aware time not allowed"
        r = value.isoformat()
        if value.microsecond:
            r = r[:12]
        return r
    elif isinstance(value, enum.Enum):
        return value.name
    elif isinstance(value, decimal.Decimal):
        return str(value)
    elif isinstance(value, UUID):
        return value.hex
    else:
        return value
