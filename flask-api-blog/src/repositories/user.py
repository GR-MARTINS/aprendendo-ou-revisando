from datetime import date, datetime
from src.models.user import User, UserGender
from src.app import db, bcrypt


class UserRepository:

    @classmethod
    def save_user(cls, data: dict):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            email=data.get("email"),
            password=bcrypt.generate_password_hash(data.get("password")),
            date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d"),
            gender=UserGender.male,
            updated_at=datetime.now(),
            role_id=data.get("role_id")
        )
        db.session.add(user)
        db.session.commit()