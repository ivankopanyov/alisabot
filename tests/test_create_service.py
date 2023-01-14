"""Unit tests for POST requests sent to api.service_list API endpoint."""
from http import HTTPStatus

import pytest

from tests.util import (
    EMAIL,
    ADMIN_EMAIL,
    BAD_REQUEST,
    FORBIDDEN,
    DEFAULT_NAME_SERVICE,
    login_user,
    create_service,
)


@pytest.mark.parametrize("service_name", ["abc12341", "service-name1", "new_service11"])
def test_create_service_valid_name(client, db, admin, service_name):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token, service_name=service_name)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"New service added: {service_name}."
    assert "message" in response.json and response.json["message"] == success
    location = f"http://localhost/api/v1/services/{service_name}"
    assert "Location" in response.headers and response.headers["Location"] == location


@pytest.mark.parametrize(
    "duration",
    [
        30,
        60,
        90,
    ],
)
def test_create_service_valid_duration(client, db, admin, duration):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token, duration=duration)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    success = f"New service added: {DEFAULT_NAME_SERVICE}."
    assert "message" in response.json and response.json["message"] == success
    location = f"http://localhost/api/v1/services/{DEFAULT_NAME_SERVICE}"
    assert "Location" in response.headers and response.headers["Location"] == location


@pytest.mark.parametrize(
    "duration",
    [
        0,
        -30,
        "abc",
    ],
)
def test_create_service_invalid_duration(client, db, admin, duration):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token, duration=duration)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "errors" in response.json and "duration" in response.json["errors"]


def test_create_service_already_exists(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CREATED
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.CONFLICT
    name_conflict = f"Service name: {DEFAULT_NAME_SERVICE} already exists, must be unique."
    assert "message" in response.json and response.json["message"] == name_conflict


def test_create_service_no_admin_token(client, db, user):
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "message" in response.json and response.json["message"] == FORBIDDEN
