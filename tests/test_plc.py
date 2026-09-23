import pytest

from wolfworks.extensions import db
from wolfworks.plc.models import IOPoint


def test_plc_page_loads(client):
    response = client.get("/plc/")

    assert response.status_code == 200
    assert b"PLC I/O Configurator" in response.data


def test_create_io_point(client, app):
    response = client.post(
        "/plc/",
        data={
            "tag_name": "Test_DI",
            "io_type": "DI",
            "address": "Local:1:I.Data.1",
            "description": "Test digital input",
        },
    )

    assert response.status_code == 200

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name="Test_DI"
        ).first()

        assert point is not None
        assert point.io_type == "DI"
        assert point.address == "Local:1:I.Data.1"
        assert point.description == "Test digital input"


@pytest.mark.parametrize(
    "io_type",
    ["DI", "DO", "AI", "AO"],
)
def test_valid_io_types(client, app, io_type):
    client.post(
        "/plc/",
        data={
            "tag_name": f"Test_{io_type}",
            "io_type": io_type,
            "address": f"Test:{io_type}",
            "description": "",
        },
    )

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name=f"Test_{io_type}"
        ).first()

        assert point is not None
        assert point.io_type == io_type


def test_duplicate_tag_rejected(client, app):
    client.post(
        "/plc/",
        data={
            "tag_name": "Duplicate_Tag",
            "io_type": "DI",
            "address": "Address:1",
            "description": "",
        },
    )

    response = client.post(
        "/plc/",
        data={
            "tag_name": "Duplicate_Tag",
            "io_type": "DO",
            "address": "Address:2",
            "description": "",
        },
    )

    assert b"already in use" in response.data

    with app.app_context():
        count = IOPoint.query.filter_by(
            tag_name="Duplicate_Tag"
        ).count()

        assert count == 1


def test_duplicate_address_rejected(client, app):
    client.post(
        "/plc/",
        data={
            "tag_name": "Point_One",
            "io_type": "DI",
            "address": "Same:Address",
            "description": "",
        },
    )

    response = client.post(
        "/plc/",
        data={
            "tag_name": "Point_Two",
            "io_type": "DO",
            "address": "Same:Address",
            "description": "",
        },
    )

    assert b"already assigned" in response.data

    with app.app_context():
        count = IOPoint.query.filter_by(
            address="Same:Address"
        ).count()

        assert count == 1
        




def test_edit_io_point(client, app):
    with app.app_context():
        point = IOPoint(
            tag_name="Old_Tag",
            io_type="DI",
            address="Old:Address",
            description="Old description",
        )

        db.session.add(point)
        db.session.commit()

        point_id = point.id

    response = client.post(
        f"/plc/point/{point_id}/edit/",
        data={
            "tag_name": "New_Tag",
            "io_type": "DO",
            "address": "New:Address",
            "description": "New description",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        point = db.session.get(IOPoint, point_id)

        assert point.tag_name == "New_Tag"
        assert point.io_type == "DO"
        assert point.address == "New:Address"
        assert point.description == "New description"
        
        
        
        
        
        
def test_edit_duplicate_tag_rejected(client, app):
    with app.app_context():
        first = IOPoint(
            tag_name="First_Point",
            io_type="DI",
            address="Address:1",
        )

        second = IOPoint(
            tag_name="Second_Point",
            io_type="DO",
            address="Address:2",
        )

        db.session.add_all([first, second])
        db.session.commit()

        second_id = second.id

    response = client.post(
        f"/plc/point/{second_id}/edit/",
        data={
            "tag_name": "First_Point",
            "io_type": "DO",
            "address": "Address:2",
            "description": "",
        },
    )

    assert b"already in use" in response.data

    with app.app_context():
        second = db.session.get(IOPoint, second_id)

        assert second.tag_name == "Second_Point"
        
        
        
        
        
        
def test_delete_io_point(client, app):
    with app.app_context():
        point = IOPoint(
            tag_name="Delete_Me",
            io_type="DO",
            address="Delete:Address",
        )

        db.session.add(point)
        db.session.commit()

        point_id = point.id

    response = client.post(
        f"/plc/point/{point_id}/delete/",
        follow_redirects=True,
    )

    assert response.status_code == 200

    with app.app_context():
        point = db.session.get(IOPoint, point_id)

        assert point is None