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

            if not tag_name:
                raise ValueError("Tag name is required.")

            if io_type not in VALID_IO_TYPES:
                raise ValueError("Invalid I/O type.")

            if not address:
                raise ValueError("Address is required.")

            if IOPoint.query.filter_by(tag_name=tag_name).first():
                raise ValueError(
                    f'Tag name "{tag_name}" is already in use.'
                )

            if IOPoint.query.filter_by(address=address).first():
                raise ValueError(
                    f'Address "{address}" is already assigned.'
                )

            point = IOPoint(
                tag_name=tag_name,
                io_type=io_type,
                address=address,
                description=description or None,
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
    
@plc_bp.route("/point/<int:point_id>/edit/", methods=["GET", "POST"])
def edit_point(point_id):
    point = db.get_or_404(IOPoint, point_id)
    error = None

    if request.method == "POST":
        try:
            tag_name = request.form.get("tag_name", "").strip()
            io_type = request.form.get("io_type", "").strip().upper()
            address = request.form.get("address", "").strip()
            description = request.form.get("description", "").strip()

            if not tag_name:
                raise ValueError("Tag name is required.")

            if io_type not in VALID_IO_TYPES:
                raise ValueError("Invalid I/O type.")

            if not address:
                raise ValueError("Address is required.")

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

            point.tag_name = tag_name
            point.io_type = io_type
            point.address = address
            point.description = description or None

            db.session.commit()

            return redirect(url_for("plc.index"))

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "plc/edit_point.html",
        point=point,
        error=error,
    )
    
@plc_bp.route("/point/<int:point_id>/delete/", methods=["POST"])
def delete_point(point_id):
    point = db.get_or_404(IOPoint, point_id)

    db.session.delete(point)
    db.session.commit()

    return redirect(url_for("plc.index"))