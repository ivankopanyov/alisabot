"""Test cases for GET requests sent to the api.position_list API endpoint."""
from http import HTTPStatus

from tests.util import ADMIN_EMAIL, login_user, create_position, retrieve_position_list


NAMES = [
    "position1",
    "second_position",
    "position-thrice",
    "tetraPOS",
    "PENTA-pos-GON-et",
    "hexa_position",
    "sep7",
]


def test_retrieve_paginated_position_list(client, db, admin):
    response = login_user(client, email=ADMIN_EMAIL)
    assert "access_token" in response.json
    access_token = response.json["access_token"]

    # ADD SEVEN POSITION INSTANCES TO DATABASE
    for i in range(0, len(NAMES)):
        response = create_position(
            client,
            access_token,
            position_name=NAMES[i],
        )
        assert response.status_code == HTTPStatus.CREATED

    # REQUEST PAGINATED LIST OF POSITIONS: 5 PER PAGE, PAGE #1
    response = retrieve_position_list(client, access_token, page=1, per_page=5)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 2
    assert "items_per_page" in response.json and response.json["items_per_page"] == 5
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 5

    # VERIFY ATTRIBUTES OF POSITIONS #1-5
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF POSITIONS: 5 PER PAGE, PAGE #2
    response = retrieve_position_list(client, access_token, page=2, per_page=5)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #2
    assert "has_prev" in response.json and response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 2
    assert "total_pages" in response.json and response.json["total_pages"] == 2
    assert "items_per_page" in response.json and response.json["items_per_page"] == 5
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 2

    # VERIFY ATTRIBUTES OF POSITIONS #6-7
    for i in range(5, response.json["total_items"]):
        item = response.json["items"][i - 5]
        assert "name" in item and item["name"] == NAMES[i]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF POSITIONS: 10 PER PAGE, PAGE #1
    response = retrieve_position_list(client, access_token, page=1, per_page=10)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 1
    assert "items_per_page" in response.json and response.json["items_per_page"] == 10
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 7

    # VERIFY ATTRIBUTES OF POSITIONS #1-7
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL

    # REQUEST PAGINATED LIST OF POSITIONS: DEFAULT PARAMETERS
    response = retrieve_position_list(client, access_token)
    assert response.status_code == HTTPStatus.OK

    # VERIFY PAGINATION ATTRIBUTES FOR PAGE #1
    assert "has_prev" in response.json and not response.json["has_prev"]
    assert "has_next" in response.json and not response.json["has_next"]
    assert "page" in response.json and response.json["page"] == 1
    assert "total_pages" in response.json and response.json["total_pages"] == 1
    assert "items_per_page" in response.json and response.json["items_per_page"] == 10
    assert "total_items" in response.json and response.json["total_items"] == 7
    assert "items" in response.json and len(response.json["items"]) == 7

    # VERIFY ATTRIBUTES OF POSITIONS #1-7
    for i in range(0, len(response.json["items"])):
        item = response.json["items"][i]
        assert "name" in item and item["name"] == NAMES[i]
        assert "owner" in item and "email" in item["owner"]
        assert item["owner"]["email"] == ADMIN_EMAIL
