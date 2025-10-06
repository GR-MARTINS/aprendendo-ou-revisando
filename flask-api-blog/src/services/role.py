from src.repositories.role import RoleRepository as repo
from src.schemas.role import CreateOrUpdateRoleSchema, RoleSchema


class RoleService:

    @classmethod
    def create_role(cls, data: dict):
        try:
            data_validated = CreateOrUpdateRoleSchema().load(data)
            repo.save(data_validated)
        except Exception:
            raise

    @classmethod
    def get_all_roles(cls):
        try:
            schema = RoleSchema(many=True)
            roles = repo.get_all_roles()
            roles_validated = schema.dump(roles)
            return roles_validated
        except Exception:
            raise

    @classmethod
    def get_role_by_id(cls, role_id: int):
        try:
            schema = RoleSchema()
            role = repo.get_role_by_id(role_id)
            role_validated = schema.dump(role)
            return role_validated
        except Exception:
            raise
