from flask_jwt_extended import create_access_token
from src.repositories.user import UserRepository as repo
from src.app import bcrypt


class AuthService:

    @classmethod
    def login(cls, data: dict):
        try:
            user = repo.get_user_by_username(data.get("username"))
            checked_password = bcrypt.check_password_hash(
                user.password,
                data.get("password"),
            )

            if user and checked_password:
                return True, create_access_token(str(user.id))

            else:
                return False, None

        except Exception:
            raise
