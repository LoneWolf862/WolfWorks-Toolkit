import pytest

from wolfworks.electrical.calculations import calculate_voltage_divider


def test_equal_resistors():
    result = calculate_voltage_divider(12, 1000, 1000)

    assert result["output_voltage"] == pytest.approx(6)
    assert result["current"] == pytest.approx(0.006)
    assert result["total_resistance"] == pytest.approx(2000)


def test_unequal_resistors():
    result = calculate_voltage_divider(12, 1000, 2000)

    assert result["output_voltage"] == pytest.approx(8)
    assert result["voltage_r1"] == pytest.approx(4)
    assert result["voltage_r2"] == pytest.approx(8)
    assert result["current"] == pytest.approx(0.004)


def test_rejects_zero_resistance():
    with pytest.raises(ValueError):
        calculate_voltage_divider(12, 0, 1000)


def test_rejects_negative_resistance():
    with pytest.raises(ValueError):
        calculate_voltage_divider(12, 1000, -100)