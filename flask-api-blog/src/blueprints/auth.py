from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.services.auth import AuthService

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
        logged_in, access_token = AuthService.login(data)

        if logged_in:
            return {"access_token": access_token}, HTTPStatus.OK
        
        else:
            return {"message": "Invalid username or password!"}, HTTPStatus.BAD_REQUEST
        
    except Exception as error:
        return {
            "message": "Internal server error",
            "exception": type(error).__name__,
        }, HTTPStatus.INTERNAL_SERVER_ERROR
