from src.app import db
from src.models.role import Role
from src.repositories.utils import update


class RoleRepository:

    @classmethod
    def save(cls, data: dict):
        try:
            role = Role(name=data.get("name"))
            db.session.add(role)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_all_roles(cls):
        try:
            query = db.select(Role)
            roles = db.session.execute(query).scalars()
            return roles
        except Exception:
            db.session.rollback()
            raise

    @classmethod
    def get_role_by_id(cls, role_id: int):
        try:
            role = db.get_or_404(Role, role_id)
            return role
        except Exception:
            db.session.rollback()
            raise
