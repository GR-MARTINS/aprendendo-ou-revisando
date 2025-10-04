from src.repositories.role import UserRepository as repo
from src.schemas.role import CreateRoleSchema


class RoleService:

    @classmethod
    def create_role(cls, data: dict):
        try:
            data_validated = CreateRoleSchema().load(data)
            repo.save(data_validated)
        except Exception:
            raise
