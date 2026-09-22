from flask import render_template, request

from wolfworks.electrical import electrical_bp
from wolfworks.electrical.calculations import (
    calculate_ohms_law,
    calculate_voltage_divider,
    calculate_resistance,
)


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
    
    
@electrical_bp.route("/voltage-divider/", methods=["GET", "POST"])
def voltage_divider():
    result = None
    error = None

    if request.method == "POST":
        try:
            input_voltage = float(request.form["input_voltage"])
            resistor_1 = float(request.form["resistor_1"])
            resistor_2 = float(request.form["resistor_2"])

            result = calculate_voltage_divider(
                input_voltage,
                resistor_1,
                resistor_2,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "electrical/voltage_divider.html",
        result=result,
        error=error,
    )
    
    
@electrical_bp.route("/resistance/", methods=["GET", "POST"])
def resistance():
    result = None
    error = None

    if request.method == "POST":
        try:
            raw_resistors = request.form.get("resistors", "")
            configuration = request.form.get("configuration", "")

            # Allow commas, spaces, or new lines between values.
            resistor_text = raw_resistors.replace(",", " ")
            resistor_values = resistor_text.split()

            resistors = [
                float(value)
                for value in resistor_values
            ]

            result = calculate_resistance(
                resistors,
                configuration,
            )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "electrical/resistance.html",
        result=result,
        error=error,
    )