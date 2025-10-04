from src.app import db
from src.models.role import Role

class UserRepository:

    @classmethod
    def save(cls, data: dict):
        try:
            role = Role(
                name=data.get("name")
            )
            db.session.add(role)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise