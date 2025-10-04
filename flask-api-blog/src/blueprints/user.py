from http import HTTPStatus
from flask import Blueprint, request
from marshmallow.exceptions import ValidationError
from src.services.user import UserService

app = Blueprint("users", __name__, url_prefix="/users")


@app.route("/", methods=["POST"])
def create_user():
    """Create a new user
    ---
    post:
      tags:
        - User
      description: Create a new user
      summary: create user
      requestBody:
        content:
          application/json:
            schema: CreateUserSchema
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
        UserService.create_user(data)
        return {"message": "user created"}, HTTPStatus.CREATED

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
