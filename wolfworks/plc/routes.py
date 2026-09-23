from flask import render_template, request, redirect, url_for

from wolfworks.extensions import db

from . import plc_bp
from .models import IOPoint


VALID_IO_TYPES = {"DI", "DO", "AI", "AO"}


@plc_bp.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        try:
            tag_name = request.form.get("tag_name", "").strip()
            io_type = request.form.get("io_type", "").strip().upper()
            address = request.form.get("address", "").strip()
            description = request.form.get("description", "").strip()

            # Basic validation
            if not tag_name:
                raise ValueError("Tag name is required.")

            if io_type not in VALID_IO_TYPES:
                raise ValueError("Invalid I/O type.")

            if not address:
                raise ValueError("Address is required.")

            # Analog fields default to None for digital I/O
            signal_min = None
            signal_max = None
            signal_unit = None
            engineering_min = None
            engineering_max = None
            engineering_unit = None

            # Analog configuration
            if io_type in {"AI", "AO"}:
                try:
                    signal_min = float(
                        request.form.get("signal_min", "")
                    )
                    signal_max = float(
                        request.form.get("signal_max", "")
                    )
                    engineering_min = float(
                        request.form.get("engineering_min", "")
                    )
                    engineering_max = float(
                        request.form.get("engineering_max", "")
                    )
                except ValueError:
                    raise ValueError(
                        "Analog minimum and maximum values "
                        "must be valid numbers."
                    )

                signal_unit = request.form.get(
                    "signal_unit",
                    "",
                ).strip()

                engineering_unit = request.form.get(
                    "engineering_unit",
                    "",
                ).strip()

                if signal_min == signal_max:
                    raise ValueError(
                        "Signal minimum and maximum cannot be equal."
                    )

                if engineering_min == engineering_max:
                    raise ValueError(
                        "Engineering minimum and maximum "
                        "cannot be equal."
                    )

                if not signal_unit:
                    raise ValueError(
                        "Signal unit is required."
                    )

                if not engineering_unit:
                    raise ValueError(
                        "Engineering unit is required."
                    )

            # Duplicate validation
            if IOPoint.query.filter_by(
                tag_name=tag_name
            ).first():
                raise ValueError(
                    f'Tag name "{tag_name}" is already in use.'
                )

            if IOPoint.query.filter_by(
                address=address
            ).first():
                raise ValueError(
                    f'Address "{address}" is already assigned.'
                )

            # Create point
            point = IOPoint(
                tag_name=tag_name,
                io_type=io_type,
                address=address,
                description=description or None,
                signal_min=signal_min,
                signal_max=signal_max,
                signal_unit=signal_unit,
                engineering_min=engineering_min,
                engineering_max=engineering_max,
                engineering_unit=engineering_unit,
            )

            db.session.add(point)
            db.session.commit()

        except ValueError as exc:
            error = str(exc)

    io_points = IOPoint.query.order_by(IOPoint.id).all()

    return render_template(
        "plc/index.html",
        io_points=io_points,
        error=error,
    )


@plc_bp.route(
    "/point/<int:point_id>/edit/",
    methods=["GET", "POST"],
)
def edit_point(point_id):
    point = db.get_or_404(IOPoint, point_id)
    error = None

    if request.method == "POST":
        try:
            tag_name = request.form.get("tag_name", "").strip()
            io_type = request.form.get("io_type", "").strip().upper()
            address = request.form.get("address", "").strip()
            description = request.form.get("description", "").strip()

            # Basic validation
            if not tag_name:
                raise ValueError("Tag name is required.")

            if io_type not in VALID_IO_TYPES:
                raise ValueError("Invalid I/O type.")

            if not address:
                raise ValueError("Address is required.")

            # Analog fields default to None for digital I/O.
            # This also clears old analog configuration if an
            # AI/AO point is changed to DI/DO.
            signal_min = None
            signal_max = None
            signal_unit = None
            engineering_min = None
            engineering_max = None
            engineering_unit = None

            # Analog configuration
            if io_type in {"AI", "AO"}:
                try:
                    signal_min = float(
                        request.form.get("signal_min", "")
                    )
                    signal_max = float(
                        request.form.get("signal_max", "")
                    )
                    engineering_min = float(
                        request.form.get("engineering_min", "")
                    )
                    engineering_max = float(
                        request.form.get("engineering_max", "")
                    )
                except ValueError:
                    raise ValueError(
                        "Analog minimum and maximum values "
                        "must be valid numbers."
                    )

                signal_unit = request.form.get(
                    "signal_unit",
                    "",
                ).strip()

                engineering_unit = request.form.get(
                    "engineering_unit",
                    "",
                ).strip()

                if signal_min == signal_max:
                    raise ValueError(
                        "Signal minimum and maximum cannot be equal."
                    )

                if engineering_min == engineering_max:
                    raise ValueError(
                        "Engineering minimum and maximum "
                        "cannot be equal."
                    )

                if not signal_unit:
                    raise ValueError(
                        "Signal unit is required."
                    )

                if not engineering_unit:
                    raise ValueError(
                        "Engineering unit is required."
                    )

            # Duplicate validation
            duplicate_tag = IOPoint.query.filter(
                IOPoint.tag_name == tag_name,
                IOPoint.id != point.id,
            ).first()

            if duplicate_tag:
                raise ValueError(
                    f'Tag name "{tag_name}" is already in use.'
                )

            duplicate_address = IOPoint.query.filter(
                IOPoint.address == address,
                IOPoint.id != point.id,
            ).first()

            if duplicate_address:
                raise ValueError(
                    f'Address "{address}" is already assigned.'
                )

            # Update point
            point.tag_name = tag_name
            point.io_type = io_type
            point.address = address
            point.description = description or None

            point.signal_min = signal_min
            point.signal_max = signal_max
            point.signal_unit = signal_unit

            point.engineering_min = engineering_min
            point.engineering_max = engineering_max
            point.engineering_unit = engineering_unit

            db.session.commit()

            return redirect(url_for("plc.index"))

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "plc/edit_point.html",
        point=point,
        error=error,
    )


@plc_bp.route(
    "/point/<int:point_id>/delete/",
    methods=["POST"],
)
def delete_point(point_id):
    point = db.get_or_404(IOPoint, point_id)

    db.session.delete(point)
    db.session.commit()

    return redirect(url_for("plc.index"))