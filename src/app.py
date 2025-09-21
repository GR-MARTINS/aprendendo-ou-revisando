import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models.base import Base
from flask_bcrypt import Bcrypt

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()

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

    import src.audits
    
    # Register bluprints
    from src.blueprints import docs, user

    app.register_blueprint(docs.json.app)
    app.register_blueprint(docs.ui.app)
    app.register_blueprint(user.app)

    return app
