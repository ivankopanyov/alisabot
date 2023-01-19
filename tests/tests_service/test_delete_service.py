"""Test cases for GET requests sent to the api.service API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    FORBIDDEN,
    login_user,
    create_service,
    retrieve_service,
    delete_service,
)


def test_delete_service(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = delete_service(client, access_token, service_id=id)
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = retrieve_service(client, access_token, service_id=id)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_service_no_admin_token(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = delete_service(client, access_token, service_id=id)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
