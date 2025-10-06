from src.app import ma
from src.models.role import Role


class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role

    id = ma.Integer()
    name = ma.String()
    

class ListRolesSchema(ma.SQLAlchemySchema):
    class meta:
        model = Role
    
    roles = ma.List(ma.Nested(RoleSchema))

class CreateOrUpdateRoleSchema(ma.SQLAlchemySchema):
    class Meta:
        Role

    name = ma.String(required=True)
