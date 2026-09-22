from flask import render_template, request

from wolfworks.electrical import electrical_bp
from wolfworks.electrical.calculations import (
    calculate_ohms_law,
    calculate_voltage_divider,
    calculate_resistance,
    calculate_adc,
    calculate_dac,
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
    

@electrical_bp.route("/adc-dac/", methods=["GET", "POST"])
def adc_dac():
    result = None
    error = None
    calculation_type = None

    if request.method == "POST":
        try:
            calculation_type = request.form.get("calculation_type")

            if calculation_type == "adc":
                input_voltage = float(
                    request.form["adc_input_voltage"]
                )

                min_voltage = float(
                    request.form["adc_min_voltage"]
                )

                max_voltage = float(
                    request.form["adc_max_voltage"]
                )

                bits = int(
                    request.form["adc_bits"]
                )

                result = calculate_adc(
                    input_voltage,
                    min_voltage,
                    max_voltage,
                    bits,
                )

            elif calculation_type == "dac":
                digital_count = int(
                    request.form["dac_digital_count"]
                )

                min_voltage = float(
                    request.form["dac_min_voltage"]
                )

                max_voltage = float(
                    request.form["dac_max_voltage"]
                )

                bits = int(
                    request.form["dac_bits"]
                )

                result = calculate_dac(
                    digital_count,
                    min_voltage,
                    max_voltage,
                    bits,
                )

            else:
                raise ValueError("Invalid calculation type.")

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "electrical/adc_dac.html",
        result=result,
        error=error,
        calculation_type=calculation_type,
    )