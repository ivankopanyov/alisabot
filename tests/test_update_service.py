"""Test cases for GET requests sent to the api.service API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    DEFAULT_NAME_SERVICE,
    login_user,
    create_service,
    retrieve_service,
    update_service,
)

UPDATED_DESCRIPTION = "https://www.newurl.com"
UPDATED_DURATION = 150


def test_update_service(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CREATED

    response = update_service(
        client,
        access_token,
        service_name=DEFAULT_NAME_SERVICE,
        description=UPDATED_DESCRIPTION,
        duration=UPDATED_DURATION,
    )
    assert response.status_code == HTTPStatus.OK
    response = retrieve_service(client, access_token, service_name=DEFAULT_NAME_SERVICE)
    assert response.status_code == HTTPStatus.OK

    assert "name" in response.json and response.json["name"] == DEFAULT_NAME_SERVICE
    assert "description" in response.json and response.json["description"] == UPDATED_DESCRIPTION
    assert "duration" in response.json and response.json["duration"] == UPDATED_DURATION
    assert "owner" in response.json and "email" in response.json["owner"]
    assert response.json["owner"]["email"] == ADMIN_EMAIL
