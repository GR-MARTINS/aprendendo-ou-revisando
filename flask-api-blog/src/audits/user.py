import json
from sqlalchemy import event, inspect
from src.models.user import User
from src.models.user_audit import UserAudit
from src.audits.utils import get_changes_from_states

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

@event.listens_for(User, "before_update")
def audit_before_update(mapper, connection, target):
    # Inspeciona o estado atual da instância
    state = inspect(target)

    old_data, new_data = get_changes_from_states(state, target)

    # Monta o registro de auditoria
    connection.execute(
        UserAudit.__table__.insert().values(
            user_id=target.id,
            action="UPDATE",
            old_data=json.dumps(old_data),
            new_data=json.dumps(new_data),
        )
    )


@event.listens_for(User, "before_delete")
def audit_delete(mapper, connection, target):
    state = inspect(target)

    old_data, new_data = get_changes_from_states(state, target)

    connection.execute(
        UserAudit.__table__.insert().values(
            role_id=target.id,
            action="DELETE",
            old_data=json.dumps(old_data),
            new_data=None,
        )
    )
