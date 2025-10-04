from src.repositories.user import UserRepository as repo
from src.schemas.user import CreateUserSchema

class UserService:

    @classmethod
    def create_user(cls, data: dict):
        try:
            data_validated = CreateUserSchema().load(data)
            repo.save(data_validated)
        except Exception:
            raise