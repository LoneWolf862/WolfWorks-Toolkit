import pytest

from wolfworks.electrical.calculations import calculate_ohms_law


def test_voltage_and_current():
    result = calculate_ohms_law(
        voltage=12,
        current=2
    )

    assert result["resistance"] == pytest.approx(6)
    assert result["power"] == pytest.approx(24)


def test_voltage_and_resistance():
    result = calculate_ohms_law(
        voltage=12,
        resistance=6
    )

    assert result["current"] == pytest.approx(2)
    assert result["power"] == pytest.approx(24)


def test_current_and_resistance():
    result = calculate_ohms_law(
        current=2,
        resistance=6
    )

    assert result["voltage"] == pytest.approx(12)
    assert result["power"] == pytest.approx(24)


def test_resistance_and_power():
    result = calculate_ohms_law(
        resistance=100,
        power=4
    )

    assert result["voltage"] == pytest.approx(20)
    assert result["current"] == pytest.approx(0.2)


def test_requires_exactly_two_values():
    with pytest.raises(ValueError):
        calculate_ohms_law(voltage=12)


def test_rejects_three_values():
    with pytest.raises(ValueError):
        calculate_ohms_law(
            voltage=12,
            current=2,
            resistance=6
        )


def test_rejects_zero_current():
    with pytest.raises(ValueError):
        calculate_ohms_law(
            current=0,
            resistance=10
        )


def test_rejects_negative_resistance():
    with pytest.raises(ValueError):
        calculate_ohms_law(
            voltage=12,
            resistance=-10
        )


def test_rejects_zero_voltage_with_power():
    with pytest.raises(ValueError):
        calculate_ohms_law(
            voltage=0,
            power=10
        )