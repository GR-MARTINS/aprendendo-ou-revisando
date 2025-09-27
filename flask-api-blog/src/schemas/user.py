from src.app import ma
from src.models.user import User


class CreateUserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    username = ma.String(required=True)
    email = ma.String(required=True)
    password = ma.String(required=True)
    date_of_birth = ma.String(required=True)
    role_id = ma.Integer(required=True)
