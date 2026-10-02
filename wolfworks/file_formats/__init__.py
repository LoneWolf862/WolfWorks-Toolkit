from flask import Blueprint


file_formats_bp = Blueprint(
    "file_formats",
    __name__,
    url_prefix="/file-formats",
)


from . import routes