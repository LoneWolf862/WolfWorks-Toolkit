def format_engineering(value, unit="", precision=4):
    """
    Format a numeric value using engineering prefixes.

    Examples:
        0.004 A       -> 4 mA
        0.001221 V    -> 1.221 mV
        4700 ohms     -> 4.7 kΩ
        0.000036 W    -> 36 µW
    """

    if value == 0:
        return f"0 {unit}".strip()

    prefixes = [
        (1e12, "T"),
        (1e9, "G"),
        (1e6, "M"),
        (1e3, "k"),
        (1, ""),
        (1e-3, "m"),
        (1e-6, "µ"),
        (1e-9, "n"),
        (1e-12, "p"),
    ]

    absolute_value = abs(value)

    for scale, prefix in prefixes:
        if absolute_value >= scale:
            scaled_value = value / scale
            formatted_value = f"{scaled_value:.{precision}g}"

            return f"{formatted_value} {prefix}{unit}".strip()

    # Values smaller than 1 p-unit fall back to scientific notation.
    return f"{value:.{precision}e} {unit}".strip()