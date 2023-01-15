"""Class definition for Service model."""
from datetime import timezone

from sqlalchemy.ext.hybrid import hybrid_property

from alisabot import db
from alisabot.util.datetime_util import (
    utc_now,
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
)


class Service(db.Model):

    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now)

    owner_id = db.Column(db.Integer, db.ForeignKey("site_user.id"), nullable=False)
    owner = db.relationship("User", backref=db.backref("service"))

    def __repr__(self):
        return f"<Service name={self.name}, description={self.description}>"

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(self.created_at, use_tz=timezone.utc, localize=False)
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
