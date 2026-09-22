from math import sqrt

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