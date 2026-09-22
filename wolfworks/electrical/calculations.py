from math import sqrt


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