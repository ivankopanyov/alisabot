"""API endpoint definitions for /services namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from alisabot.api.service.dto import (
    create_service_reqparser,
    update_service_reqparser,
    pagination_reqparser,
    service_owner_model,
    service_model,
    pagination_links_model,
    pagination_model,
)
from alisabot.api.service.business import (
    create_service,
    retrieve_service_list,
    retrieve_service,
    update_service,
    delete_service,
)

service_ns = Namespace(name="services", validate=True)
service_ns.models[service_owner_model.name] = service_owner_model
service_ns.models[service_model.name] = service_model
service_ns.models[pagination_links_model.name] = pagination_links_model
service_ns.models[pagination_model.name] = pagination_model


@service_ns.route("", endpoint="service_list")
@service_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@service_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@service_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class ServiceList(Resource):
    """Handles HTTP requests to URL: /services."""

    @service_ns.doc(security="Bearer")
    @service_ns.response(HTTPStatus.OK, "Retrieved service list.", pagination_model)
    @service_ns.expect(pagination_reqparser)
    def get(self):
        """Retrieve a list of services."""
        request_data = pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_service_list(page, per_page)

    @service_ns.doc(security="Bearer")
    @service_ns.response(int(HTTPStatus.CREATED), "Added new service.")
    @service_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @service_ns.expect(create_service_reqparser)
    def post(self):
        """Create a service."""
        service_dict = create_service_reqparser.parse_args()
        return create_service(service_dict)


@service_ns.route("/<id>", endpoint="service")
@service_ns.param("id", "Service id")
@service_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@service_ns.response(int(HTTPStatus.NOT_FOUND), "Service not found.")
@service_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@service_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Service(Resource):
    """Handles HTTP requests to URL: /services/{id}."""

    @service_ns.doc(security="Bearer")
    @service_ns.response(int(HTTPStatus.OK), "Retrieved service.", service_model)
    @service_ns.marshal_with(service_model)
    def get(self, id):
        """Retrieve a service."""
        return retrieve_service(id)

    @service_ns.doc(security="Bearer")
    @service_ns.response(int(HTTPStatus.OK), "Service was updated.", service_model)
    @service_ns.response(int(HTTPStatus.CREATED), "Added new service.")
    @service_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @service_ns.expect(update_service_reqparser)
    def put(self, id):
        """Update a service."""
        service_dict = update_service_reqparser.parse_args()
        return update_service(id, service_dict)

    @service_ns.doc(security="Bearer")
    @service_ns.response(int(HTTPStatus.NO_CONTENT), "Service was deleted.")
    @service_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, id):
        """Delete a service."""
        return delete_service(id)
