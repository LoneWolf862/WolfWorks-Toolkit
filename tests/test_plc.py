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
    data = {
        "tag_name": f"Test_{io_type}",
        "io_type": io_type,
        "address": f"Test:{io_type}",
        "description": "",
    }

    if io_type in {"AI", "AO"}:
        data.update({
            "signal_min": "4",
            "signal_max": "20",
            "signal_unit": "mA",
            "engineering_min": "0",
            "engineering_max": "100",
            "engineering_unit": "%",
        })

    client.post(
        "/plc/",
        data=data,
    )

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name=f"Test_{io_type}"
        ).first()

        assert point is not None
        assert point.io_type == io_type

        if io_type in {"AI", "AO"}:
            assert point.signal_min == 4
            assert point.signal_max == 20
            assert point.signal_unit == "mA"
            assert point.engineering_min == 0
            assert point.engineering_max == 100
            assert point.engineering_unit == "%"
        else:
            assert point.signal_min is None
            assert point.signal_max is None
            assert point.signal_unit is None
            assert point.engineering_min is None
            assert point.engineering_max is None
            assert point.engineering_unit is None


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
        



def test_create_analog_io_point(client, app):
    client.post(
        "/plc/",
        data={
            "tag_name": "Pressure_01",
            "io_type": "AI",
            "address": "Local:3:I.Ch00Data",
            "description": "Tank pressure",
            "signal_min": "4",
            "signal_max": "20",
            "signal_unit": "mA",
            "engineering_min": "0",
            "engineering_max": "300",
            "engineering_unit": "PSI",
        },
    )

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name="Pressure_01"
        ).first()

        assert point is not None
        assert point.io_type == "AI"

        assert point.signal_min == 4
        assert point.signal_max == 20
        assert point.signal_unit == "mA"

        assert point.engineering_min == 0
        assert point.engineering_max == 300
        assert point.engineering_unit == "PSI"


def test_edit_analog_io_point(client, app):
    with app.app_context():
        point = IOPoint(
            tag_name="Pressure_01",
            io_type="AI",
            address="Local:3:I.Ch00Data",
            description="Tank pressure",
            signal_min=4,
            signal_max=20,
            signal_unit="mA",
            engineering_min=0,
            engineering_max=300,
            engineering_unit="PSI",
        )

        db.session.add(point)
        db.session.commit()

        point_id = point.id

    client.post(
        f"/plc/point/{point_id}/edit/",
        data={
            "tag_name": "Pressure_01",
            "io_type": "AI",
            "address": "Local:3:I.Ch00Data",
            "description": "Tank pressure",
            "signal_min": "4",
            "signal_max": "20",
            "signal_unit": "mA",
            "engineering_min": "0",
            "engineering_max": "500",
            "engineering_unit": "PSI",
        },
    )

    with app.app_context():
        point = db.session.get(
            IOPoint,
            point_id,
        )

        assert point.engineering_max == 500
        assert point.signal_min == 4
        assert point.signal_max == 20
        assert point.signal_unit == "mA"


def test_analog_to_digital_clears_ranges(client, app):
    with app.app_context():
        point = IOPoint(
            tag_name="Pressure_01",
            io_type="AI",
            address="Local:3:I.Ch00Data",
            description="Tank pressure",
            signal_min=4,
            signal_max=20,
            signal_unit="mA",
            engineering_min=0,
            engineering_max=300,
            engineering_unit="PSI",
        )

        db.session.add(point)
        db.session.commit()

        point_id = point.id

    client.post(
        f"/plc/point/{point_id}/edit/",
        data={
            "tag_name": "Pressure_01",
            "io_type": "DI",
            "address": "Local:3:I.Data.0",
            "description": "Digital pressure switch",
        },
    )

    with app.app_context():
        point = db.session.get(
            IOPoint,
            point_id,
        )

        assert point.io_type == "DI"

        assert point.signal_min is None
        assert point.signal_max is None
        assert point.signal_unit is None

        assert point.engineering_min is None
        assert point.engineering_max is None
        assert point.engineering_unit is None


def test_equal_signal_limits_rejected(client, app):
    client.post(
        "/plc/",
        data={
            "tag_name": "Bad_AI",
            "io_type": "AI",
            "address": "Local:3:I.Ch01Data",
            "description": "",
            "signal_min": "4",
            "signal_max": "4",
            "signal_unit": "mA",
            "engineering_min": "0",
            "engineering_max": "100",
            "engineering_unit": "%",
        },
    )

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name="Bad_AI"
        ).first()

        assert point is None


def test_equal_engineering_limits_rejected(client, app):
    client.post(
        "/plc/",
        data={
            "tag_name": "Bad_AI",
            "io_type": "AI",
            "address": "Local:3:I.Ch01Data",
            "description": "",
            "signal_min": "4",
            "signal_max": "20",
            "signal_unit": "mA",
            "engineering_min": "100",
            "engineering_max": "100",
            "engineering_unit": "%",
        },
    )

    with app.app_context():
        point = IOPoint.query.filter_by(
            tag_name="Bad_AI"
        ).first()

        assert point is None