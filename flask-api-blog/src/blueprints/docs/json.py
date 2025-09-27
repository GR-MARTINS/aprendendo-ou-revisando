from flask import Blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from src.schemas.utils import MessageSchema
import src.blueprints as bp

spec = APISpec(
    title="DIO Blog API",
    version="0.1.0",
    openapi_version="3.0.4",
    info=dict(description="Blog RestFull API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("MessageSchema", schema=MessageSchema)

app = Blueprint("api_spec", __name__, url_prefix="/docs")


@app.route("/swagger.json")
def api_spec_json():
    return (
        spec.path(view=bp.user.create_user)
        .path(view=bp.role.create_role)
        .to_dict()
        )
