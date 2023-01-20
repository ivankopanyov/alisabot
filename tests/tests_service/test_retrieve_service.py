"""Test cases for GET requests sent to the api.service API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    DEFAULT_NAME,
    DEFAULT_DESCRIPTION,
    DEFAULT_DURATION_SERVICE,
    login_user,
    create_service,
    retrieve_service,
)


def test_retrieve_service_non_admin_user(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = retrieve_service(client, access_token, service_id=id)
    assert response.status_code == HTTPStatus.OK

    assert "name" in response.json and response.json["name"] == DEFAULT_NAME
    assert "description" in response.json and response.json["description"] == DEFAULT_DESCRIPTION
    assert "duration" in response.json and response.json["duration"] == DEFAULT_DURATION_SERVICE


def test_retrieve_service_does_not_exist(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = retrieve_service(client, access_token, service_id=0)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "message" in response.json and "Service not found in database" in response.json["message"]
