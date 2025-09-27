from src.app import db
from src.models.role import Role

class UserRepository:

    @classmethod
    def save_role(cls, data: dict):
        role = Role(
            name=data.get("name")
        )
        db.session.add(role)
        db.session.commit()