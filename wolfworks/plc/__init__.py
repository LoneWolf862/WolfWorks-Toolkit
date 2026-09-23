from flask import Blueprint


plc_bp = Blueprint(
    "plc",
    __name__,
    url_prefix="/plc",
)

from . import models
from . import routes