"""Test cases for GET requests sent to the api.position API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    DEFAULT_NAME,
    login_user,
    create_position,
    retrieve_position,
)


def test_retrieve_position_non_admin_user(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = retrieve_position(client, access_token, position_id=id)
    assert response.status_code == HTTPStatus.OK

    assert "name" in response.json and response.json["name"] == DEFAULT_NAME
    assert "owner" in response.json and "email" in response.json["owner"]
    assert response.json["owner"]["email"] == ADMIN_EMAIL


def test_retrieve_position_does_not_exist(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = retrieve_position(client, access_token, position_id=0)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert "message" in response.json and "Position not found in database" in response.json["message"]
