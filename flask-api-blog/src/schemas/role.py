from src.app import ma
from src.models.role import Role


class CreateRoleSchema(ma.SQLAlchemySchema):
    class Meta: Role

    name = ma.String(required=True)