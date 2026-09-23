from wolfworks.extensions import db


class IOPoint(db.Model):
    __tablename__ = "io_points"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    tag_name = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )

    io_type = db.Column(
        db.String(2),
        nullable=False,
    )

    address = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    description = db.Column(
        db.String(255),
        nullable=True,
    )

    signal_min = db.Column(
        db.Float,
        nullable=True,
    )

    signal_max = db.Column(
        db.Float,
        nullable=True,
    )

    engineering_min = db.Column(
        db.Float,
        nullable=True,
    )

    engineering_max = db.Column(
        db.Float,
        nullable=True,
    )

    engineering_unit = db.Column(
        db.String(20),
        nullable=True,
    )

    def __repr__(self):
        return (
            f"<IOPoint "
            f"{self.tag_name} "
            f"{self.io_type} "
            f"{self.address}>"
        )