"""API endpoint definitions for /positions namespace."""
from http import HTTPStatus

from flask_restx import Namespace, Resource

from alisabot.api.position.dto import (
    create_position_reqparser,
    update_position_reqparser,
    pagination_reqparser,
    position_model,
    position_service_model,
    pagination_links_model,
    pagination_model,
    service_id_reqparser,
)
from alisabot.api.position.business import (
    create_position,
    retrieve_position_list,
    retrieve_position,
    update_position,
    delete_position,
    append_service,
    remove_service,
)

position_ns = Namespace(name="positions", validate=True)
position_ns.models[position_model.name] = position_model
position_ns.models[pagination_links_model.name] = pagination_links_model
position_ns.models[pagination_model.name] = pagination_model
position_ns.models[position_service_model.name] = position_service_model


@position_ns.route("", endpoint="position_list")
@position_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@position_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@position_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class PositionList(Resource):
    """Handles HTTP requests to URL: /positions."""

    @position_ns.doc(security="Bearer")
    @position_ns.response(HTTPStatus.OK, "Retrieved position list.", pagination_model)
    @position_ns.expect(pagination_reqparser)
    def get(self):
        """Retrieve a list of positions."""
        request_data = pagination_reqparser.parse_args()
        page = request_data.get("page")
        per_page = request_data.get("per_page")
        return retrieve_position_list(page, per_page)

    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.CREATED), "Added new position.")
    @position_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @position_ns.expect(create_position_reqparser)
    def post(self):
        """Create a position."""
        position_dict = create_position_reqparser.parse_args()
        return create_position(position_dict)


@position_ns.route("/<id>", endpoint="position")
@position_ns.param("id", "Position id")
@position_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@position_ns.response(int(HTTPStatus.NOT_FOUND), "Position not found.")
@position_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@position_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Position(Resource):
    """Handles HTTP requests to URL: /positions/{id}."""

    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.OK), "Retrieved position.", position_model)
    @position_ns.marshal_with(position_model)
    def get(self, id):
        """Retrieve a position."""
        return retrieve_position(id)

    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.OK), "Position was updated.", position_model)
    @position_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @position_ns.expect(update_position_reqparser)
    def put(self, id):
        """Update a position."""
        position_dict = update_position_reqparser.parse_args()
        return update_position(id, position_dict)

    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.NO_CONTENT), "Position was deleted.")
    @position_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    def delete(self, id):
        """Delete a position."""
        return delete_position(id)


@position_ns.route("/services/<id>", endpoint="position_services")
@position_ns.param("id", "Position id")
@position_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
@position_ns.response(int(HTTPStatus.NOT_FOUND), "Position not found.")
@position_ns.response(int(HTTPStatus.UNAUTHORIZED), "Unauthorized.")
@position_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class PositionService(Resource):
    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.OK), "Service was added.")
    @position_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @position_ns.expect(service_id_reqparser)
    def post(self, id):
        service_id_dict = service_id_reqparser.parse_args()
        return append_service(id, service_id_dict)

    @position_ns.doc(security="Bearer")
    @position_ns.response(int(HTTPStatus.OK), "Service was added.")
    @position_ns.response(int(HTTPStatus.FORBIDDEN), "Administrator token required.")
    @position_ns.expect(service_id_reqparser)
    def delete(self, id):
        service_id_dict = service_id_reqparser.parse_args()
        return remove_service(id, service_id_dict)
