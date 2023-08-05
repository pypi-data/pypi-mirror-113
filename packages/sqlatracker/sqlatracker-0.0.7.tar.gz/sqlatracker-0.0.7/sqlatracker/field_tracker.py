import datetime

from sqlalchemy import JSON, BigInteger, Column, DateTime, String
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import symbol

from sqlatracker.utils import can_json

__all__ = ["FieldTracker"]


@as_declarative()
class Base:
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_time = Column(DateTime, default=datetime.datetime.utcnow)


class FieldTracker(Base):
    __tablename__ = "field_tracker"

    table = Column(String(64), nullable=False, index=True)
    row = Column(BigInteger, nullable=False, index=True)
    field = Column(String(64), nullable=False, index=True)
    old_value = Column(JSON)
    new_value = Column(JSON)

    @classmethod
    def listen_for(cls, *fields):
        for i in fields:

            @listens_for(i, "set")
            def create(target, value, oldvalue, initiator):
                if any(
                    [
                        oldvalue is symbol("NO_VALUE"),
                        value == oldvalue,
                    ]
                ):
                    return value

                Session.object_session(target).add(
                    cls(
                        table=target.__tablename__,
                        row=target.id,
                        field=initiator.key,
                        old_value=can_json(oldvalue),
                        new_value=can_json(value),
                    )
                )
                return value
