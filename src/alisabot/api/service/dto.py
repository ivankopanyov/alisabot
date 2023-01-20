"""Parsers and serializers for /services API endpoints."""
from flask_restx import Model
from flask_restx.fields import Boolean, DateTime, Integer, List, Nested, String, Url
from flask_restx.inputs import positive
from flask_restx.reqparse import RequestParser


def service_name(name):
    if len(name) > 100:
        raise ValueError("Name max 100.")
    return name


def service_description(description):
    if len(description) > 1000:
        raise ValueError("Description max 1000.")
    return description


def service_duration(duration):
    try:
        duration = int(duration)
    except ValueError:
        raise ValueError("Duration must be integer.")
    if duration <= 0:
        raise ValueError("Duration must be more zero.")
    return duration


create_service_reqparser = RequestParser(bundle_errors=True)
create_service_reqparser.add_argument("name", type=service_name, location="form", required=True, nullable=False)
create_service_reqparser.add_argument(
    "description",
    type=service_description,
    location="form",
    required=True,
    nullable=False,
)
create_service_reqparser.add_argument(
    "duration",
    type=service_duration,
    location="form",
    required=True,
    nullable=False,
)


pagination_reqparser = RequestParser(bundle_errors=True)
pagination_reqparser.add_argument("page", type=positive, required=False, default=1)
pagination_reqparser.add_argument("per_page", type=positive, required=False, choices=[5, 10, 25, 50, 100], default=10)

service_model = Model(
    "Service",
    {
        "id": String,
        "name": String,
        "description": String,
        "duration": Integer,
        "created_at_iso8601": DateTime(attribute="created_at"),
        "created_at_rfc822": DateTime(attribute="created_at", dt_format="rfc822"),
        "link": Url("api.service"),
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
        "items": List(Nested(service_model)),
    },
)


update_service_reqparser = create_service_reqparser.copy()
