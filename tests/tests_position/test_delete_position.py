"""Test cases for GET requests sent to the api.position API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    FORBIDDEN,
    login_user,
    create_position,
    retrieve_position,
    delete_position,
)


def test_delete_position(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = delete_position(client, access_token, position_id=id)
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = retrieve_position(client, access_token, position_id=id)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_position_no_admin_token(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = delete_position(client, access_token, position_id=id)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
