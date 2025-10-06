from http import HTTPStatus
from flask import Blueprint, request
from werkzeug.exceptions import NotFound
from marshmallow.exceptions import ValidationError
from src.services.role import RoleService
from src.schemas.role import RoleSchema, ListRolesSchema

app = Blueprint("roles", __name__, url_prefix="/roles")


@app.route("/", methods=["POST"])
def create_role():
    """Create a new role
    ---
    post:
      tags:
        - Role
      description: Create a new role
      summary: create role
      requestBody:
        content:
          application/json:
            schema: CreateOrUpdateRoleSchema
        description: request data
        required: true
      responses:
        201:
          description: Success Operation
          content:
            application/json:
              schema: MessageSchema
        400:
          description: Bad Request
          content:
            application/json:
              schema: ValidationErrorSchema
        500:
          description: Internal Server Error
          content:
            application/json:
              schema: InternalServerErrorSchema
    """
    try:
        data = request.json
        RoleService.create_role(data)
        return {"message": "role created"}, HTTPStatus.CREATED

    except ValidationError as error:
        return {
            "message": "Required fields missing or invalid",
            "required_fields": list(error.messages.keys()),
        }, HTTPStatus.BAD_REQUEST

    except Exception as error:
        return {
            "message": "Internal Server Error",
            "exception": type(error).__name__,
        }, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/")
def get_all_roles():
    """Get all roles
    ---
    get:
      tags:
        - Role
      description: get all roles
      summary: get roles
      responses:
        200:
          description: Success Operation
          content:
            application/json:
              schema: ListRolesSchema
        500:
          description: Internal Server Error
          content:
            application/json:
              schema: InternalServerErrorSchema
    """
    try:
        roles = RoleService.get_all_roles()

        return ListRolesSchema().dump({"roles": roles}), HTTPStatus.OK

    except Exception as error:
        return {
            "message": "Internal Server Error",
            "exception": type(error).__name__,
        }, HTTPStatus.INTERNAL_SERVER_ERROR


@app.route("/<int:role_id>")
def get_role_by_id(role_id: int):
    """Get role by ID
    ---
    get:
      tags:
        - Role
      description: get role by id
      summary: get role
      parameters:
        - in: path
          name: role_id
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Success Operation
          content:
            application/json:
              schema: RoleSchema
        404:
          description: Role Not Found
          content:
            application/json:
              schema: MessageSchema
        500:
          description: Internal Server Error
          content:
            application/json:
              schema: InternalServerErrorSchema
    """
    try:
        role = RoleService.get_role_by_id(role_id)
        return role, HTTPStatus.OK

    except NotFound:
        return {"message": "Role not found"}, HTTPStatus.NOT_FOUND

    except Exception as error:
        return {
            "message": "Internal Server Error",
            "exception": type(error).__name__,
        }, HTTPStatus.INTERNAL_SERVER_ERROR
