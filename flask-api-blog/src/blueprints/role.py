from http import HTTPStatus
from flask import Blueprint, request
from marshmallow.exceptions import ValidationError
from src.services.role import RoleService

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
            schema: CreateRoleSchema
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
