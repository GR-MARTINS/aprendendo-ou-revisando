import json
from sqlalchemy import event
from src.models.user import User
from src.models.user_audit import UserAudit

def _serialize(user: User):
    """Converte User em dict para salvar no log"""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
        "active": user.active
    }

@event.listens_for(User, "after_insert")
def audit_insert(mapper, connection, target):
    connection.execute(
        UserAudit.__table__.insert().values(
            user_id=target.id,
            action="INSERT",
            old_data=None,
            new_data=json.dumps(_serialize(target))
        )
    )

@event.listens_for(User, "after_update")
def audit_update(mapper, connection, target):
    connection.execute(
        UserAudit.__table__.insert().values(
            user_id=target.id,
            action="UPDATE",
            old_data=None,  # se quiser, pode capturar snapshot anterior
            new_data=json.dumps(_serialize(target))
        )
    )

@event.listens_for(User, "after_delete")
def audit_delete(mapper, connection, target):
    connection.execute(
        UserAudit.__table__.insert().values(
            user_id=target.id,
            action="DELETE",
            old_data=json.dumps(_serialize(target)),
            new_data=None
        )
    )