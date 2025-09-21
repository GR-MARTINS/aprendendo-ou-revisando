from flask import Blueprint, request
from src.repositories.user import UserRepository as repo
app = Blueprint("users", __name__, url_prefix="/users")

@app.route("/", methods=["POST"])
def create_user():

    data = request.json
    repo.save_user(data)
    return {"message": "user created"}