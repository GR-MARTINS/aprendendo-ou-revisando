import json
from sqlalchemy import event, inspect
import sqlalchemy as sa
from src.models.role import Role
from src.models.role_audit import RoleAudit
from src.audits.utils import get_changes_from_states


def _serialize(role: Role):
    """Converte Role em dict para salvar no log"""
    return {
        "id": role.id,
        "name": role.name,
    }


@event.listens_for(Role, "after_insert")
def audit_insert(mapper, connection, target):
    connection.execute(
        RoleAudit.__table__.insert().values(
            role_id=target.id,
            action="INSERT",
            old_data=None,
            new_data=json.dumps(_serialize(target)),
        )
    )


@event.listens_for(Role, "before_update")
def audit_before_update(mapper, connection, target):
    # Inspeciona o estado atual da instância
    state = inspect(target)

    old_data, new_data = get_changes_from_states(state, target)

    # Monta o registro de auditoria
    connection.execute(
        RoleAudit.__table__.insert().values(
            role_id=target.id,
            action="UPDATE",
            old_data=json.dumps(old_data),
            new_data=json.dumps(new_data),
        )
    )


@event.listens_for(Role, "before_delete")
def audit_delete(mapper, connection, target):
    state = inspect(target)

    old_data, new_data = get_changes_from_states(state, target)

    connection.execute(
        RoleAudit.__table__.insert().values(
            role_id=target.id,
            action="DELETE",
            old_data=json.dumps(old_data),
            new_data=None,
        )
    )
