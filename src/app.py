import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models.base import Base


db = SQLAlchemy(model_class=Base)


def create_app(environment=os.environ["FLASK_ENV"]):
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists("instance"):
        os.makedirs("instance")
    config_path = f"instance.config.{environment.title()}Config".replace('"', "")
    app.config.from_object(config_path)

    # Init apps
    db.init_app(app)

    # Register bluprints
    from src.blueprints import docs

    app.register_blueprint(docs.json.app)
    app.register_blueprint(docs.ui.app)

    return app
