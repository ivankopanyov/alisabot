"""Class definition for Position model."""
from datetime import timezone

from sqlalchemy.ext.hybrid import hybrid_property

from alisabot import db
from alisabot.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
)


position_service = db.Table(
    "position_service",
    db.Column("service_id", db.Integer, db.ForeignKey("service.id")),
    db.Column("position_id", db.Integer, db.ForeignKey("position.id")),
)


class Position(db.Model):

    __tablename__ = "position"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)
    services = db.relationship("Service", secondary=position_service, backref=db.backref("positions", lazy="dynamic"))

    def __repr__(self):
        return f"<Position name={self.name}>"

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(self.created_at, use_tz=timezone.utc, localize=False)
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
