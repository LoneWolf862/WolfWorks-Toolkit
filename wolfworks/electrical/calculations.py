from math import sqrt
import math

#----# Ohm's Law #----#
def calculate_ohms_law(voltage=None, current=None, resistance=None, power=None):
    values = {
        "voltage": voltage,
        "current": current,
        "resistance": resistance,
        "power": power,
    }

    known = [name for name, value in values.items() if value is not None]

    if len(known) != 2:
        raise ValueError("Exactly two values are required.")

    if current is not None and current == 0:
        raise ValueError("Current must not be zero.")

    if resistance is not None and resistance <= 0:
        raise ValueError("Resistance must be greater than zero.")

    if power is not None and power < 0:
        raise ValueError("Power must not be negative.")

    if voltage is not None and voltage == 0 and power is not None:
        raise ValueError(
            "Voltage must not be zero when calculating from power."
        )

    if voltage is not None and current is not None:
        resistance = voltage / current
        power = voltage * current

    elif voltage is not None and resistance is not None:
        current = voltage / resistance
        power = voltage * current

    elif voltage is not None and power is not None:
        current = power / voltage
        resistance = voltage / current

    elif current is not None and resistance is not None:
        voltage = current * resistance
        power = voltage * current

    elif current is not None and power is not None:
        voltage = power / current
        resistance = voltage / current

    elif resistance is not None and power is not None:
        voltage = sqrt(power * resistance)
        current = voltage / resistance

    return {
        "voltage": voltage,
        "current": current,
        "resistance": resistance,
        "power": power,
    }
    
#----# Voltage Devider #----#
def calculate_voltage_divider(input_voltage, resistor_1, resistor_2):
    if input_voltage < 0:
        raise ValueError("Input voltage must not be negative.")

    if resistor_1 <= 0 or resistor_2 <= 0:
        raise ValueError("Resistor values must be greater than zero.")

    total_resistance = resistor_1 + resistor_2
    current = input_voltage / total_resistance

    voltage_r1 = current * resistor_1
    voltage_r2 = current * resistor_2

    power_r1 = current ** 2 * resistor_1
    power_r2 = current ** 2 * resistor_2

    return {
        "input_voltage": input_voltage,
        "resistor_1": resistor_1,
        "resistor_2": resistor_2,
        "total_resistance": total_resistance,
        "current": current,
        "voltage_r1": voltage_r1,
        "voltage_r2": voltage_r2,
        "output_voltage": voltage_r2,
        "power_r1": power_r1,
        "power_r2": power_r2,
    }
    
#----# Series / Parallel Resistance #----#
def calculate_resistance(resistors, configuration):
    if len(resistors) < 2:
        raise ValueError("Enter at least two resistor values.")

    if any(resistance <= 0 for resistance in resistors):
        raise ValueError("All resistor values must be greater than zero.")

    if configuration == "series":
        equivalent_resistance = sum(resistors)

    elif configuration == "parallel":
        reciprocal_sum = sum(1 / resistance for resistance in resistors)
        equivalent_resistance = 1 / reciprocal_sum

    else:
        raise ValueError("Invalid resistor configuration.")

    return {
        "resistors": resistors,
        "configuration": configuration,
        "equivalent_resistance": equivalent_resistance,
    }
    
#----# ADC calculation #----#    
def calculate_adc(input_voltage, min_voltage, max_voltage, bits):
    if bits <= 0:
        raise ValueError("Resolution must be greater than zero bits.")

    if not isinstance(bits, int):
        raise ValueError("Resolution must be a whole number of bits.")

    if max_voltage <= min_voltage:
        raise ValueError(
            "Maximum voltage must be greater than minimum voltage."
        )

    if input_voltage < min_voltage or input_voltage > max_voltage:
        raise ValueError(
            "Input voltage must be within the configured voltage range."
        )

    max_count = (2 ** bits) - 1
    voltage_range = max_voltage - min_voltage
    lsb = voltage_range / max_count

    normalized_voltage = input_voltage - min_voltage
    ideal_count = normalized_voltage / voltage_range * max_count

    digital_count = round(ideal_count)

    quantized_voltage = (
        min_voltage
        + (digital_count / max_count) * voltage_range
    )

    quantization_error = quantized_voltage - input_voltage

    return {
        "input_voltage": input_voltage,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage,
        "bits": bits,
        "max_count": max_count,
        "digital_count": digital_count,
        "lsb": lsb,
        "quantized_voltage": quantized_voltage,
        "quantization_error": quantization_error,
    }

#----# DAC calculation #----#
def calculate_dac(digital_count, min_voltage, max_voltage, bits):
    if bits <= 0:
        raise ValueError("Resolution must be greater than zero bits.")

    if not isinstance(bits, int):
        raise ValueError("Resolution must be a whole number of bits.")

    if max_voltage <= min_voltage:
        raise ValueError(
            "Maximum voltage must be greater than minimum voltage."
        )

    max_count = (2 ** bits) - 1

    if digital_count < 0 or digital_count > max_count:
        raise ValueError(
            f"Digital count must be between 0 and {max_count}."
        )

    voltage_range = max_voltage - min_voltage
    lsb = voltage_range / max_count

    output_voltage = (
        min_voltage
        + (digital_count / max_count) * voltage_range
    )

    return {
        "digital_count": digital_count,
        "min_voltage": min_voltage,
        "max_voltage": max_voltage,
        "bits": bits,
        "max_count": max_count,
        "lsb": lsb,
        "output_voltage": output_voltage,
    }
    
#----# Analog Scaling #----#    
def calculate_linear_scaling(
    input_value,
    input_min,
    input_max,
    output_min,
    output_max,
):
    if input_max == input_min:
        raise ValueError(
            "Input maximum and minimum cannot be equal."
        )

    if input_value < min(input_min, input_max) or \
       input_value > max(input_min, input_max):
        raise ValueError(
            "Input value must be within the configured input range."
        )

    input_span = input_max - input_min
    output_span = output_max - output_min

    normalized_value = (
        (input_value - input_min) / input_span
    )

    output_value = (
        output_min
        + normalized_value * output_span
    )

    percentage = normalized_value * 100

    return {
        "input_value": input_value,
        "input_min": input_min,
        "input_max": input_max,
        "output_min": output_min,
        "output_max": output_max,
        "output_value": output_value,
        "percentage": percentage,
    }
    
#----# digital clock #----#     
def calculate_period(frequency):
    if frequency <= 0:
        raise ValueError(
            "Frequency must be greater than zero."
        )

    return 1 / frequency


def calculate_frequency(period):
    if period <= 0:
        raise ValueError(
            "Period must be greater than zero."
        )

    return 1 / period


def calculate_cycles_to_time(
    frequency,
    cycles,
):
    if frequency <= 0:
        raise ValueError(
            "Frequency must be greater than zero."
        )

    if cycles < 0:
        raise ValueError(
            "Clock cycles cannot be negative."
        )

    return cycles / frequency


def calculate_time_to_cycles(
    frequency,
    time,
):
    if frequency <= 0:
        raise ValueError(
            "Frequency must be greater than zero."
        )

    if time < 0:
        raise ValueError(
            "Time cannot be negative."
        )

    return frequency * time
    
def calculate_clock_divider(
    source_frequency,
    target_frequency,
):
    if source_frequency <= 0:
        raise ValueError(
            "Source frequency must be greater than zero."
        )

    if target_frequency <= 0:
        raise ValueError(
            "Target frequency must be greater than zero."
        )

    if target_frequency > source_frequency:
        raise ValueError(
            "Target frequency cannot exceed "
            "the source frequency."
        )

    ideal_divider = (
        source_frequency / target_frequency
    )

    divider = max(1, round(ideal_divider))

    actual_frequency = (
        source_frequency / divider
    )

    error_hz = (
        actual_frequency - target_frequency
    )

    error_percent = (
        error_hz / target_frequency
    ) * 100

    error_ppm = (
        error_hz / target_frequency
    ) * 1_000_000

    return {
        "ideal_divider": ideal_divider,
        "divider": divider,
        "actual_frequency": actual_frequency,
        "error_hz": error_hz,
        "error_percent": error_percent,
        "error_ppm": error_ppm,
    }
    
def calculate_timer(
    clock_frequency,
    target_time,
):
    if clock_frequency <= 0:
        raise ValueError(
            "Clock frequency must be greater than zero."
        )

    if target_time <= 0:
        raise ValueError(
            "Target time must be greater than zero."
        )

    ideal_cycles = (
        clock_frequency * target_time
    )

    cycles = max(1, round(ideal_cycles))

    actual_time = (
        cycles / clock_frequency
    )

    error_seconds = (
        actual_time - target_time
    )

    error_percent = (
        error_seconds / target_time
    ) * 100

    counter_bits = max(
        1,
        math.ceil(math.log2(cycles)),
    )

    return {
        "ideal_cycles": ideal_cycles,
        "cycles": cycles,
        "counter_bits": counter_bits,
        "actual_time": actual_time,
        "error_seconds": error_seconds,
        "error_percent": error_percent,
    }
    
def calculate_pwm(
    clock_frequency,
    target_frequency,
    duty_cycle,
):
    if clock_frequency <= 0:
        raise ValueError(
            "Clock frequency must be greater than zero."
        )

    if target_frequency <= 0:
        raise ValueError(
            "PWM frequency must be greater than zero."
        )

    if target_frequency > clock_frequency:
        raise ValueError(
            "PWM frequency cannot exceed "
            "the clock frequency."
        )

    if duty_cycle < 0 or duty_cycle > 100:
        raise ValueError(
            "Duty cycle must be between 0 and 100."
        )

    ideal_period_counts = (
        clock_frequency / target_frequency
    )

    period_counts = max(
        1,
        round(ideal_period_counts),
    )

    actual_frequency = (
        clock_frequency / period_counts
    )

    high_counts = round(
        period_counts * duty_cycle / 100
    )

    high_counts = max(
        0,
        min(period_counts, high_counts),
    )

    low_counts = period_counts - high_counts

    actual_duty_cycle = (
        high_counts / period_counts
    ) * 100

    frequency_error = (
        actual_frequency - target_frequency
    )

    frequency_error_percent = (
        frequency_error / target_frequency
    ) * 100

    duty_error = (
        actual_duty_cycle - duty_cycle
    )

    counter_bits = max(
        1,
        math.ceil(math.log2(period_counts)),
    )

    return {
        "ideal_period_counts": ideal_period_counts,
        "period_counts": period_counts,
        "high_counts": high_counts,
        "low_counts": low_counts,
        "actual_frequency": actual_frequency,
        "actual_duty_cycle": actual_duty_cycle,
        "frequency_error": frequency_error,
        "frequency_error_percent": frequency_error_percent,
        "duty_error": duty_error,
        "counter_bits": counter_bits,
    }
    
FREQUENCY_UNITS = {
    "Hz": 1,
    "kHz": 1e3,
    "MHz": 1e6,
    "GHz": 1e9,
}

TIME_UNITS = {
    "s": 1,
    "ms": 1e-3,
    "us": 1e-6,
    "ns": 1e-9,
    "ps": 1e-12,
}


def frequency_to_hz(value, unit):
    if unit not in FREQUENCY_UNITS:
        raise ValueError("Invalid frequency unit.")

    return value * FREQUENCY_UNITS[unit]


def time_to_seconds(value, unit):
    if unit not in TIME_UNITS:
        raise ValueError("Invalid time unit.")

    return value * TIME_UNITS[unit]