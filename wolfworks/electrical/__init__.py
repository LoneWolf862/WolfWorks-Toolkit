from flask import Blueprint


electrical_bp = Blueprint(
    "electrical",
    __name__,
    url_prefix="/electrical"
)

from wolfworks.electrical import routes