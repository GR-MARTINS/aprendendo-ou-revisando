import enum
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app import db


class UserAudit(db.Model):
    __tablename__ = "users_audits"

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id"), nullable=False
    )  # usuário alvo
    action: Mapped[str] = mapped_column(sa.String(), nullable=False)
    old_data: Mapped[str] = mapped_column(sa.String(), nullable=True)
    new_data: Mapped[str] = mapped_column(sa.String(), nullable=True)

    modified_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[user_id],          # <- especifica qual FK usar
        back_populates="audits"
    )

    # Usuário que fez a modificação
    modified_by_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    modifying_user: Mapped["User"] = relationship(
        "User",
        foreign_keys=[modified_by_id],   # <- especifica qual FK usar
        back_populates="modifications"
    )
    operation_metadata: Mapped[dict] = mapped_column(sa.JSON(), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
