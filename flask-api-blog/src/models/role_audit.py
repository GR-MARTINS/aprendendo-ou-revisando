from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app import db

class RoleAudit(db.Model):
    __tablename__ = "roles_audits"

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True, autoincrement=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("roles.id"), nullable=False)
    action: Mapped[str] = mapped_column(sa.String(), nullable=False)
    old_data: Mapped[str] = mapped_column(sa.String(), nullable=True)
    new_data: Mapped[str] = mapped_column(sa.String(), nullable=True)
    modified_role: Mapped["Role"] = relationship(
        "Role",
        foreign_keys=[role_id],
        back_populates="audits"
    )
    modified_by_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("users.id"), nullable=True)
    operation_metadata: Mapped[dict] = mapped_column(sa.JSON(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )

