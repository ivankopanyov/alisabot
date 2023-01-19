"""Конфигурация подпроекта (blueprint) для API."""
from flask import Blueprint
from flask_restx import Api

from alisabot.api.auth.endpoints import auth_ns
from alisabot.api.widgets.endpoints import widget_ns
from alisabot.api.service.endpoints import service_ns
from alisabot.api.position.endpoints import position_ns

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="Flask API with JWT-Based Authentication",
    description="Welcome to the Swagger UI documentation for the Widget API",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(widget_ns, path="/widgets")
api.add_namespace(service_ns, path="/services")
api.add_namespace(position_ns, path="/positions")
