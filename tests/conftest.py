import pytest

from wolfworks import create_app
from wolfworks.extensions import db


@pytest.fixture()
def app(tmp_path):
    database_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": (
            f"sqlite:///{database_path.as_posix()}"
        ),
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()