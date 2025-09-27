import json
from sqlalchemy import event
from src.models.role import Role
from src.models.role_audit import RoleAudit

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
            new_data=json.dumps(_serialize(target))
        )
    )

@event.listens_for(Role, "after_update")
def audit_update(mapper, connection, target):
    connection.execute(
        RoleAudit.__table__.insert().values(
            role_id=target.id,
            action="UPDATE",
            old_data=None,  # se quiser, pode capturar snapshot anterior
            new_data=json.dumps(_serialize(target))
        )
    )

@event.listens_for(Role, "after_delete")
def audit_delete(mapper, connection, target):
    connection.execute(
        RoleAudit.__table__.insert().values(
            role_id=target.id,
            action="DELETE",
            old_data=json.dumps(_serialize(target)),
            new_data=None
        )
    )