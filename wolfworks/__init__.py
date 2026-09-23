from flask import Flask

from wolfworks.extensions import db, migrate
from wolfworks.electrical.formatting import format_engineering


def create_app(test_config=None):
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wolfworks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Allow configuration overrides for testing
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Jinja filters
    app.jinja_env.filters["engineering"] = format_engineering

    # Blueprints
    from wolfworks.core import core_bp
    app.register_blueprint(core_bp)

    from wolfworks.electrical import electrical_bp
    app.register_blueprint(electrical_bp)

    from wolfworks.plc import plc_bp
    app.register_blueprint(plc_bp)

    return app