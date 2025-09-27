import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.app import db


class Role(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(sa.Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(), nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="role")
    # Auditorias em que esta regra foi o alvo da modificação
    audits: Mapped[list["RoleAudit"]] = relationship(
        "RoleAudit",
        foreign_keys="RoleAudit.role_id",
        back_populates="modified_role"
    )
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"