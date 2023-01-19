"""Parsers and serializers for /positions API endpoints."""
from flask_restx import Model
from flask_restx.fields import Boolean, DateTime, Integer, List, Nested, String, Url
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser

from alisabot.api.service.dto import service_model


def position_name(name):
    if len(name) > 100:
        raise ValueError("Name max 100.")
    return name


create_position_reqparser = RequestParser(bundle_errors=True)
create_position_reqparser.add_argument("name", type=position_name, location="form", required=True, nullable=False)

pagination_reqparser = RequestParser(bundle_errors=True)
pagination_reqparser.add_argument("page", type=positive, required=False, default=1)
pagination_reqparser.add_argument("per_page", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10)

position_service_model = service_model

position_owner_model = Model("Position Owner", {"email": String, "public_id": String})

position_model = Model(
    "Position",
    {
        "id": Integer,
        "name": String,
        "services": List(Nested(position_service_model)),
        "created_at_iso8601": DateTime(attribute="created_at"),
        "created_at_rfc822": DateTime(attribute="created_at", dt_format="rfc822"),
        "owner": Nested(position_owner_model),
        "link": Url("api.position"),
    },
)

pagination_links_model = Model(
    "Nav Links",
    {"self": String, "prev": String, "next": String, "first": String, "last": String},
)

pagination_model = Model(
    "Pagination",
    {
        "links": Nested(pagination_links_model, skip_none=True),
        "has_prev": Boolean,
        "has_next": Boolean,
        "page": Integer,
        "total_pages": Integer(attribute="pages"),
        "items_per_page": Integer(attribute="per_page"),
        "total_items": Integer(attribute="total"),
        "items": List(Nested(position_model)),
    },
)

update_position_reqparser = create_position_reqparser.copy()

service_id_reqparser = RequestParser(bundle_errors=True)
service_id_reqparser.add_argument("service_id", type=positive, location="form", required=True, nullable=False)
