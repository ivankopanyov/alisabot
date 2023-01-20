"""Unit tests for POST requests sent to api.position_list API endpoint."""
from http import HTTPStatus

from tests.util import (
    ADMIN_EMAIL,
    EMAIL,
    DEFAULT_NAME,
    login_user,
    create_position,
    create_service,
    append_service_to_position,
    remove_service_from_position,
)


def test_remove_service(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token, position_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    position_id = response.json["id"]
    response = create_service(client, access_token, service_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    service_id = response.json["id"]
    response = append_service_to_position(client, access_token, position_id=position_id, service_id=service_id)
    assert response.status_code == HTTPStatus.OK
    response = remove_service_from_position(client, access_token, position_id=position_id, service_id=service_id)
    assert response.status_code == HTTPStatus.OK


def test_remove_no_added_service(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token, position_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    position_id = response.json["id"]
    response = create_service(client, access_token, service_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    service_id = response.json["id"]
    response = remove_service_from_position(client, access_token, position_id=position_id, service_id=service_id)
    assert response.status_code == HTTPStatus.OK


def test_remove_no_exists_service(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token, position_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    position_id = response.json["id"]
    response = remove_service_from_position(client, access_token, position_id=position_id, service_id=0)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_remove_no_exists_position(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_service(client, access_token, service_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    service_id = response.json["id"]
    response = remove_service_from_position(client, access_token, position_id=0, service_id=service_id)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_remove_service_no_admin_token(client, db, admin, user):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = create_position(client, access_token, position_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    position_id = response.json["id"]
    response = create_service(client, access_token, service_name=DEFAULT_NAME)
    assert response.status_code == HTTPStatus.CREATED
    service_id = response.json["id"]
    response = append_service_to_position(client, access_token, position_id=position_id, service_id=service_id)
    assert response.status_code == HTTPStatus.OK
    response = login_user(client, email=EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = remove_service_from_position(client, access_token, position_id=position_id, service_id=service_id)
    assert response.status_code == HTTPStatus.FORBIDDEN
