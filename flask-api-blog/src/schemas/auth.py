from src.app import ma
from src.models.user import User


class LoginSchema(ma.SQLAlchemySchema):
    class Meta: User
    username = ma.String(required=True)
    password = ma.String(required=True)


class AccessTokenSchema(ma.Schema):
    access_token = ma.String()