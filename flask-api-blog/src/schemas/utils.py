from src.app import ma

class MessageSchema(ma.Schema):
    message= ma.String(required=True)