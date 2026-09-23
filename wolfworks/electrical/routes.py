from flask import render_template, request

from wolfworks.electrical import electrical_bp
from wolfworks.electrical.calculations import (
    calculate_ohms_law,
    calculate_voltage_divider,
    calculate_resistance,
    calculate_adc,
    calculate_dac,
    calculate_linear_scaling,
    calculate_period,
    calculate_frequency,
    calculate_cycles_to_time,
    calculate_time_to_cycles,
    calculate_clock_divider,
    calculate_timer,
    calculate_pwm,
    frequency_to_hz,
    time_to_seconds,
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
    
    
@electrical_bp.route("/analog-scaling/", methods=["GET", "POST"])
def analog_scaling():
    result = None
    error = None

    direction = "signal_to_engineering"
    signal_unit = ""
    engineering_unit = ""

    if request.method == "POST":
        try:
            direction = request.form.get(
                "direction",
                "signal_to_engineering",
            )

            value_to_convert = float(
                request.form["value_to_convert"]
            )

            signal_min = float(
                request.form["signal_min"]
            )

            signal_max = float(
                request.form["signal_max"]
            )

            engineering_min = float(
                request.form["engineering_min"]
            )

            engineering_max = float(
                request.form["engineering_max"]
            )

            signal_unit = request.form.get(
                "signal_unit",
                "",
            ).strip()

            engineering_unit = request.form.get(
                "engineering_unit",
                "",
            ).strip()

            if direction == "signal_to_engineering":
                result = calculate_linear_scaling(
                    value_to_convert,
                    signal_min,
                    signal_max,
                    engineering_min,
                    engineering_max,
                )

            elif direction == "engineering_to_signal":
                result = calculate_linear_scaling(
                    value_to_convert,
                    engineering_min,
                    engineering_max,
                    signal_min,
                    signal_max,
                )

            else:
                raise ValueError(
                    "Invalid scaling direction."
                )

        except (ValueError, KeyError) as exc:
            error = str(exc)

    return render_template(
        "electrical/analog_scaling.html",
        result=result,
        error=error,
        direction=direction,
        signal_unit=signal_unit,
        engineering_unit=engineering_unit,
    )
    
@electrical_bp.route(
    "/clock-timing/",
    methods=["GET", "POST"],
)
def clock_timing():
    result = None
    error = None

    if request.method == "POST":
        try:
            mode = request.form.get(
                "mode",
                "frequency_period",
            )

            # ------------------------------------------
            # Frequency / Period
            # ------------------------------------------

            if mode == "frequency_period":
                direction = request.form.get(
                    "direction",
                    "frequency_to_period",
                )

                if direction == "frequency_to_period":
                    value = float(
                        request.form.get("frequency", "")
                    )

                    unit = request.form.get(
                        "frequency_unit",
                        "Hz",
                    )

                    frequency = frequency_to_hz(
                        value,
                        unit,
                    )

                    result = {
                        "mode": mode,
                        "direction": direction,
                        "input_value": value,
                        "input_unit": unit,
                        "frequency": frequency,
                        "period": calculate_period(
                            frequency
                        ),
                    }

                elif direction == "period_to_frequency":
                    value = float(
                        request.form.get("period", "")
                    )

                    unit = request.form.get(
                        "period_unit",
                        "s",
                    )

                    period = time_to_seconds(
                        value,
                        unit,
                    )

                    result = {
                        "mode": mode,
                        "direction": direction,
                        "input_value": value,
                        "input_unit": unit,
                        "period": period,
                        "frequency": calculate_frequency(
                            period
                        ),
                    }

                else:
                    raise ValueError(
                        "Invalid conversion direction."
                    )

            # ------------------------------------------
            # Clock Cycles / Time
            # ------------------------------------------

            elif mode == "cycles_time":
                direction = request.form.get(
                    "direction",
                    "cycles_to_time",
                )

                clock_value = float(
                    request.form.get(
                        "clock_frequency",
                        "",
                    )
                )

                clock_unit = request.form.get(
                    "clock_frequency_unit",
                    "Hz",
                )

                clock_frequency = frequency_to_hz(
                    clock_value,
                    clock_unit,
                )

                if direction == "cycles_to_time":
                    cycles = float(
                        request.form.get("cycles", "")
                    )

                    result = {
                        "mode": mode,
                        "direction": direction,
                        "clock_frequency": clock_frequency,
                        "cycles": cycles,
                        "time": calculate_cycles_to_time(
                            clock_frequency,
                            cycles,
                        ),
                    }

                elif direction == "time_to_cycles":
                    time_value = float(
                        request.form.get("time", "")
                    )

                    time_unit = request.form.get(
                        "time_unit",
                        "s",
                    )

                    time = time_to_seconds(
                        time_value,
                        time_unit,
                    )

                    result = {
                        "mode": mode,
                        "direction": direction,
                        "clock_frequency": clock_frequency,
                        "time": time,
                        "cycles": calculate_time_to_cycles(
                            clock_frequency,
                            time,
                        ),
                    }

                else:
                    raise ValueError(
                        "Invalid conversion direction."
                    )

            # ------------------------------------------
            # Clock Divider
            # ------------------------------------------

            elif mode == "clock_divider":
                source_value = float(
                    request.form.get(
                        "source_frequency",
                        "",
                    )
                )

                source_unit = request.form.get(
                    "source_frequency_unit",
                    "Hz",
                )

                target_value = float(
                    request.form.get(
                        "target_frequency",
                        "",
                    )
                )

                target_unit = request.form.get(
                    "target_frequency_unit",
                    "Hz",
                )

                source_frequency = frequency_to_hz(
                    source_value,
                    source_unit,
                )

                target_frequency = frequency_to_hz(
                    target_value,
                    target_unit,
                )

                result = calculate_clock_divider(
                    source_frequency,
                    target_frequency,
                )

                result["mode"] = mode
                result["source_frequency"] = source_frequency
                result["target_frequency"] = target_frequency

            # ------------------------------------------
            # Counter / Timer
            # ------------------------------------------

            elif mode == "timer":
                clock_value = float(
                    request.form.get(
                        "clock_frequency",
                        "",
                    )
                )

                clock_unit = request.form.get(
                    "clock_frequency_unit",
                    "Hz",
                )

                time_value = float(
                    request.form.get(
                        "target_time",
                        "",
                    )
                )

                time_unit = request.form.get(
                    "target_time_unit",
                    "s",
                )

                clock_frequency = frequency_to_hz(
                    clock_value,
                    clock_unit,
                )

                target_time = time_to_seconds(
                    time_value,
                    time_unit,
                )

                result = calculate_timer(
                    clock_frequency,
                    target_time,
                )

                result["mode"] = mode
                result["clock_frequency"] = clock_frequency
                result["target_time"] = target_time
                result["terminal_count"] = (
                    result["cycles"] - 1
                )

            # ------------------------------------------
            # PWM
            # ------------------------------------------

            elif mode == "pwm":
                clock_value = float(
                    request.form.get(
                        "clock_frequency",
                        "",
                    )
                )

                clock_unit = request.form.get(
                    "clock_frequency_unit",
                    "Hz",
                )

                target_value = float(
                    request.form.get(
                        "target_frequency",
                        "",
                    )
                )

                target_unit = request.form.get(
                    "target_frequency_unit",
                    "Hz",
                )

                duty_cycle = float(
                    request.form.get(
                        "duty_cycle",
                        "",
                    )
                )

                clock_frequency = frequency_to_hz(
                    clock_value,
                    clock_unit,
                )

                target_frequency = frequency_to_hz(
                    target_value,
                    target_unit,
                )

                result = calculate_pwm(
                    clock_frequency,
                    target_frequency,
                    duty_cycle,
                )

                result["mode"] = mode
                result["clock_frequency"] = clock_frequency
                result["target_frequency"] = target_frequency
                result["target_duty_cycle"] = duty_cycle

            else:
                raise ValueError(
                    "Invalid clock calculation mode."
                )

        except ValueError as exc:
            error = str(exc)

    return render_template(
        "electrical/clock_timing.html",
        result=result,
        error=error,
    )