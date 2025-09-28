from flask import Blueprint, request
from src.repositories.user import UserRepository as repo
from src.app import bcrypt
from flask_jwt_extended import create_access_token


app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    """JWT Auth
    ---
    post:
      tags:
        - Auth
      description: get access token
      summary: get access token
      requestBody:
        content:
          application/json:
            schema: LoginSchema
      responses:
        200:
          description: Success Operation
          content:
            application/json:
              schema: AccessTokenSchema
              
    """
    data = request.json
    user = repo.get_user_by_username(data.get("username"))
    checked_password = bcrypt.check_password_hash(user.password, data.get("password"))
    if user and checked_password:
        return {"access_token": create_access_token(str(user.id))}