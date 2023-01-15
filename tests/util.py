"""Общие функции и константы для модульных тестов."""
from datetime import date

from flask import url_for

EMAIL = "new_user@email.com"
ADMIN_EMAIL = "admin_user@email.com"
PASSWORD = "test1234"
BAD_REQUEST = "Input payload validation failed"
UNAUTHORIZED = "Unauthorized"
FORBIDDEN = "You are not an administrator"
WWW_AUTH_NO_TOKEN = 'Bearer realm="registered_users@mydomain.com"'

DEFAULT_NAME = "some-widget"
DEFAULT_URL = "https://www.fakesite.com"
DEFAULT_DEADLINE = date.today().strftime("%m/%d/%y")

DEFAULT_NAME_SERVICE = "some-service"
DEFAULT_DESCRIPTION_SERVICE = "some-service_description"
DEFAULT_DURATION_SERVICE = 30


def register_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_register"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def login_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(
        url_for("api.auth_login"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def get_user(test_client, access_token):
    return test_client.get(url_for("api.auth_user"), headers={"Authorization": f"Bearer {access_token}"})


def logout_user(test_client, access_token):
    return test_client.post(url_for("api.auth_logout"), headers={"Authorization": f"Bearer {access_token}"})


def create_widget(
    test_client,
    access_token,
    widget_name=DEFAULT_NAME,
    info_url=DEFAULT_URL,
    deadline_str=DEFAULT_DEADLINE,
):
    return test_client.post(
        url_for("api.widget_list"),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"name={widget_name}&info_url={info_url}&deadline={deadline_str}",
        content_type="application/x-www-form-urlencoded",
    )


def retrieve_widget_list(test_client, access_token, page=None, per_page=None):
    return test_client.get(
        url_for("api.widget_list", page=page, per_page=per_page),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def retrieve_widget(test_client, access_token, widget_name):
    return test_client.get(
        url_for("api.widget", name=widget_name),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_widget(test_client, access_token, widget_name, info_url, deadline_str):
    return test_client.put(
        url_for("api.widget", name=widget_name),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"info_url={info_url}&deadline={deadline_str}",
        content_type="application/x-www-form-urlencoded",
    )


def delete_widget(test_client, access_token, widget_name):
    return test_client.delete(
        url_for("api.widget", name=widget_name),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_service(
    test_client,
    access_token,
    service_name=DEFAULT_NAME_SERVICE,
    description=DEFAULT_DESCRIPTION_SERVICE,
    duration=DEFAULT_DURATION_SERVICE,
):
    return test_client.post(
        url_for("api.service_list"),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"name={service_name}&description={description}&duration={duration}",
        content_type="application/x-www-form-urlencoded",
    )


def retrieve_service_list(test_client, access_token, page=None, per_page=None):
    return test_client.get(
        url_for("api.service_list", page=page, per_page=per_page),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def retrieve_service(test_client, access_token, service_id):
    return test_client.get(
        url_for("api.service", id=service_id),
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_service(test_client, access_token, service_id, name, description, duration):
    return test_client.put(
        url_for("api.service", id=service_id),
        headers={"Authorization": f"Bearer {access_token}"},
        data=f"name={name}&description={description}&duration={duration}",
        content_type="application/x-www-form-urlencoded",
    )


def delete_service(test_client, access_token, service_id):
    return test_client.delete(
        url_for("api.service", id=service_id),
        headers={"Authorization": f"Bearer {access_token}"},
    )
