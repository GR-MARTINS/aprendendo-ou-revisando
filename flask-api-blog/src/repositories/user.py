from datetime import date, datetime
from src.models.user import User, UserGender
from src.app import db, bcrypt


class UserRepository:

    @classmethod
    def _parse_gender(cls, data: dict):
        gender_map = {
            "male": UserGender.male,
            "female": UserGender.female,
            "non-binary": UserGender.non_binary,
        }

        return gender_map.get(data.get("gender"), UserGender.prefer_not_to_say)

    @classmethod
    def save(cls, data: dict):
        try:
            user = User(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=data.get("username"),
                email=data.get("email"),
                password=bcrypt.generate_password_hash(data.get("password")),
                date_of_birth=datetime.strptime(data.get("date_of_birth"), "%Y-%m-%d"),
                gender=cls._parse_gender(data),
                updated_at=datetime.now(),
                role_id=data.get("role_id"),
            )
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        
    @classmethod
    def get_user_by_username(cls, username: str):
        query = db.select(User).where(User.username == username)
        user = db.session.execute(query).scalar()
        return user
