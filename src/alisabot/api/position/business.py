"""Business logic for /positions API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import marshal

from alisabot import db
from alisabot.api.auth.decorators import token_required, admin_token_required
from alisabot.api.position.dto import pagination_model
from alisabot.models.user import User
from alisabot.models.position import Position
from alisabot.models.service import Service


@admin_token_required
def create_position(position_dict):
    name = position_dict["name"]
    position = Position(**position_dict)
    owner = User.find_by_public_id(create_position.public_id)
    position.owner_id = owner.id
    db.session.add(position)
    db.session.commit()
    db.session.refresh(position)
    response = jsonify(status="success", message=f"New position added: {name}.", id=position.id)
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.position", id=position.id)
    return response


@token_required
def retrieve_position_list(page, per_page):
    pagination = Position.query.paginate(page, per_page, error_out=False)
    response_data = marshal(pagination, pagination_model)
    response_data["links"] = _pagination_nav_links(pagination)
    response = jsonify(response_data)
    response.headers["Link"] = _pagination_nav_header_links(pagination)
    response.headers["Total-Count"] = pagination.total
    return response


def _pagination_nav_links(pagination):
    nav_links = {}
    per_page = pagination.per_page
    this_page = pagination.page
    last_page = pagination.pages
    nav_links["self"] = url_for("api.position_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.position_list", page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for("api.position_list", page=this_page - 1, per_page=per_page)
    if pagination.has_next:
        nav_links["next"] = url_for("api.position_list", page=this_page + 1, per_page=per_page)
    nav_links["last"] = url_for("api.position_list", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")


@token_required
def retrieve_position(id):
    return Position.query.filter_by(id=id).first_or_404(description="Position not found in database.")


@admin_token_required
def update_position(id, position_dict):
    position = Position.find_by_id(id)
    if position:
        for k, v in position_dict.items():
            setattr(position, k, v)
        db.session.commit()
        position_name = position_dict["name"]
        message = f"'{position_name}' was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    return "", HTTPStatus.NOT_FOUND


@admin_token_required
def delete_position(id):
    position = Position.query.filter_by(id=id).first_or_404(description="Position not found in database.")
    db.session.delete(position)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT


@admin_token_required
def append_service(id, service_id_dict):
    service_id = service_id_dict["service_id"]
    position = Position.query.filter_by(id=id).first_or_404(description="Position not found in database.")
    service = Service.query.filter_by(id=service_id).first_or_404(description="Service not found in database.")
    if service in position.services:
        return "", HTTPStatus.OK
    position.services.append(service)
    db.session.commit()
    return "", HTTPStatus.OK


@admin_token_required
def remove_service(id, service_id_dict):
    service_id = service_id_dict["service_id"]
    position = Position.query.filter_by(id=id).first_or_404(description="Position not found in database.")
    service = Service.query.filter_by(id=service_id).first_or_404(description="Service not found in database.")
    if not service in position.services:
        return "", HTTPStatus.OK
    position.services.remove(service)
    db.session.commit()
    return "", HTTPStatus.OK
