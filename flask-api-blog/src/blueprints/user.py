from http import HTTPStatus
from flask import Blueprint, request
from src.repositories.user import UserRepository as repo
from src.schemas.user import CreateUserSchema


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
    """
    data = request.json
    repo.save_user(data)
    return {"message": "user created"}, HTTPStatus.CREATED
