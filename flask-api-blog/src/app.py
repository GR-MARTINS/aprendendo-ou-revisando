import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models.base import Base
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
ma = Marshmallow()
jwt = JWTManager()

def create_app(environment=os.environ["FLASK_ENV"]):
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.exists("instance"):
        os.makedirs("instance")
    config_path = f"instance.config.{environment.title()}Config".replace('"', "")
    app.config.from_object(config_path)

    # Init apps
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # import listeners
    import src.audits

    # Register bluprints
    from src.blueprints import docs, user, role, auth

    app.register_blueprint(docs.json.app)
    app.register_blueprint(docs.ui.app)
    app.register_blueprint(user.app)
    app.register_blueprint(role.app)
    app.register_blueprint(auth.app)

    return app
