from http import HTTPStatus
from flask import Blueprint, request
from src.repositories.role import UserRepository as repo
from src.schemas.role import CreateRoleSchema

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
      reponses:
        201:
          description: Success Operation
          content:
            application/json:
              schema: MessageSchema
    """
    data = request.json
    repo.save_role(data)
    return {"message": "role created"}, HTTPStatus.CREATED