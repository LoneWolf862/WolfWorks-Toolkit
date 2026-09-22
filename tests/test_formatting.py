from wolfworks.electrical.formatting import format_engineering


def test_base_unit():
    assert format_engineering(12, "V") == "12 V"


def test_milli():
    assert format_engineering(0.004, "A") == "4 mA"


def test_micro():
    assert format_engineering(0.000150, "A") == "150 µA"


def test_kilo():
    assert format_engineering(4700, "Ω") == "4.7 kΩ"


def test_mega():
    assert format_engineering(1_000_000, "Ω") == "1 MΩ"


def test_milliwatts():
    assert format_engineering(0.036, "W") == "36 mW"


def test_zero():
    assert format_engineering(0, "V") == "0 V"


def test_negative():
    assert format_engineering(-0.010, "V") == "-10 mV"