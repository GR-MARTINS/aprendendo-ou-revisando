from flask import Blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

spec = APISpec(
    title="DIO Blog API",
    version="0.1.0",
    openapi_version="3.0.4",
    info=dict(description="Blog RestFull API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

app = Blueprint("api_spec", __name__, url_prefix="/docs")


@app.route("/swagger.json")
def api_spec_json():
    return {}
