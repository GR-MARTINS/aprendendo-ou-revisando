import enum
from datetime import datetime, date
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from src.app import db


class UserGender(enum.Enum):
    male = "Male"
    female = "Female"
    non_binary = "Non-binary"
    prefer_not_to_say = "Prefer not to say"


class User(db.model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(sa.String(), nullable=False)
    last_name: Mapped[str] = mapped_column(sa.String(), nullable=False)
    username: Mapped[str] = mapped_column(sa.String(), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(sa.String(), nullable=False)
    password: Mapped[str] = mapped_column(sa.String(), nullable=False)
    gender: Mapped[str] = mapped_column(sa.Enum(UserGender, name="user_gender_enum"))
    active: Mapped[bool] = mapped_column(sa.Boolean(), default=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), updated_at=sa.func.now
    )
    date_of_birth: Mapped[date] = mapped_column(sa.Date, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"