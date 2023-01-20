"""Test cases for GET requests sent to the api.position API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    login_user,
    create_position,
    retrieve_position,
    update_position,
)

UPDATED_NAME = "new_position_name"


def test_update_position(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    response = update_position(
        client,
        access_token,
        position_id=id,
        name=UPDATED_NAME,
    )
    assert response.status_code == HTTPStatus.OK
    response = retrieve_position(client, access_token, position_id=id)
    assert response.status_code == HTTPStatus.OK
    assert "name" in response.json and response.json["name"] == UPDATED_NAME
