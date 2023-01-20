"""Business logic for /services API endpoints."""
from http import HTTPStatus

from flask import jsonify, url_for
from flask_restx import marshal

from alisabot import db
from alisabot.api.auth.decorators import token_required, admin_token_required
from alisabot.api.service.dto import pagination_model
from alisabot.models.service import Service


@admin_token_required
def create_service(service_dict):
    name = service_dict["name"]
    service = Service(**service_dict)
    db.session.add(service)
    db.session.commit()
    db.session.refresh(service)
    response = jsonify(status="success", message=f"New service added: {name}.", id=service.id)
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for("api.service", id=service.id)
    return response


@token_required
def retrieve_service_list(page, per_page):
    pagination = Service.query.paginate(page, per_page, error_out=False)
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
    nav_links["self"] = url_for("api.service_list", page=this_page, per_page=per_page)
    nav_links["first"] = url_for("api.service_list", page=1, per_page=per_page)
    if pagination.has_prev:
        nav_links["prev"] = url_for("api.service_list", page=this_page - 1, per_page=per_page)
    if pagination.has_next:
        nav_links["next"] = url_for("api.service_list", page=this_page + 1, per_page=per_page)
    nav_links["last"] = url_for("api.service_list", page=last_page, per_page=per_page)
    return nav_links


def _pagination_nav_header_links(pagination):
    url_dict = _pagination_nav_links(pagination)
    link_header = ""
    for rel, url in url_dict.items():
        link_header += f'<{url}>; rel="{rel}", '
    return link_header.strip().strip(",")


@token_required
def retrieve_service(id):
    return Service.query.filter_by(id=id).first_or_404(description="Service not found in database.")


@admin_token_required
def update_service(id, service_dict):
    service = Service.find_by_id(id)
    if service:
        for k, v in service_dict.items():
            setattr(service, k, v)
        db.session.commit()
        service_name = service_dict["name"]
        message = f"'{service_name}' was successfully updated"
        response_dict = dict(status="success", message=message)
        return response_dict, HTTPStatus.OK
    return "", HTTPStatus.NOT_FOUND


@admin_token_required
def delete_service(id):
    service = Service.query.filter_by(id=id).first_or_404(description="Service not found in database.")
    db.session.delete(service)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
