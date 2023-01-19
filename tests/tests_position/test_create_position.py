"""Unit tests for POST requests sent to api.position_list API endpoint."""
from http import HTTPStatus

import pytest

from tests.util import (
    EMAIL,
    ADMIN_EMAIL,
    FORBIDDEN,
    login_user,
    create_position,
)


@pytest.mark.parametrize("position_name", ["abc12341", "position-name1", "new_position11"])
def test_create_position_valid_name(client, db, admin, position_name):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token, position_name=position_name)
    assert response.status_code == HTTPStatus.CREATED
    id = response.json["id"]
    assert "status" in response.json and response.json["status"] == "success"
    success = f"New position added: {position_name}."
    assert "message" in response.json and response.json["message"] == success
    location = f"http://localhost/api/v1/positions/{id}"
    assert "Location" in response.headers and response.headers["Location"] == location


def test_create_position_no_admin_token(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
