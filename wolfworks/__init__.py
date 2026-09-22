from flask import Flask

from wolfworks.extensions import db
from wolfworks.electrical.formatting import format_engineering


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wolfworks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.jinja_env.filters["engineering"] = format_engineering

    from wolfworks.core import core_bp
    app.register_blueprint(core_bp)

    from wolfworks.electrical import electrical_bp
    app.register_blueprint(electrical_bp)

    return app
