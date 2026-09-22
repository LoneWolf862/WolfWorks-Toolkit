from flask import render_template, request

from wolfworks.electrical import electrical_bp
from wolfworks.electrical.calculations import calculate_ohms_law


@electrical_bp.route("/")
def index():
    return render_template("electrical/index.html")


@electrical_bp.route("/ohms-law/", methods=["GET", "POST"])
def ohms_law():
    result = None
    error = None

    if request.method == "POST":
        try:
            values = {}

            for field in ["voltage", "current", "resistance", "power"]:
                raw_value = request.form.get(field, "").strip()

                if raw_value:
                    values[field] = float(raw_value)
                else:
                    values[field] = None

            result = calculate_ohms_law(**values)

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "electrical/ohms_law.html",
        result=result,
        error=error,
    )