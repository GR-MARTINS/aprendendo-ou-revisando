from flask_swagger_ui import get_swaggerui_blueprint

API_SPEC_URL = "/docs/swagger.json"
SWAGGER_UI_URL = "/docs"

app = get_swaggerui_blueprint(
    base_url=SWAGGER_UI_URL,
    api_url=API_SPEC_URL,
    config={"app_name": "DIO Blog API"},
)
