from flask import abort, render_template

from . import file_formats_bp
from .formats import FILE_FORMATS


@file_formats_bp.route("/")
def index():
    return render_template(
        "file_formats/index.html"
    )


@file_formats_bp.route("/reference/")
def reference():
    return render_template(
        "file_formats/reference.html",
        file_formats=FILE_FORMATS,
    )


@file_formats_bp.route(
    "/reference/<format_id>/"
)
def format_detail(format_id):
    format_data = FILE_FORMATS.get(
        format_id.lower()
    )

    if format_data is None:
        abort(404)

    return render_template(
        "file_formats/format_detail.html",
        format_id=format_id,
        format_data=format_data,
    )