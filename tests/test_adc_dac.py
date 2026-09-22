import pytest

from wolfworks.electrical.calculations import (
    calculate_adc,
    calculate_dac,
)


def test_adc_midpoint():
    result = calculate_adc(2.5, 0, 5, 8)

    assert result["digital_count"] == 128
    assert result["max_count"] == 255
    assert result["lsb"] == pytest.approx(5 / 255)
    assert result["quantized_voltage"] == pytest.approx(128 / 255 * 5)


def test_adc_minimum():
    result = calculate_adc(0, 0, 5, 12)

    assert result["digital_count"] == 0
    assert result["quantized_voltage"] == pytest.approx(0)


def test_adc_maximum():
    result = calculate_adc(5, 0, 5, 12)

    assert result["digital_count"] == 4095
    assert result["quantized_voltage"] == pytest.approx(5)


def test_adc_rejects_out_of_range_voltage():
    with pytest.raises(ValueError):
        calculate_adc(6, 0, 5, 12)


def test_adc_rejects_invalid_voltage_range():
    with pytest.raises(ValueError):
        calculate_adc(2.5, 5, 0, 12)


def test_adc_rejects_invalid_resolution():
    with pytest.raises(ValueError):
        calculate_adc(2.5, 0, 5, 0)


def test_dac_midpoint():
    result = calculate_dac(128, 0, 5, 8)

    assert result["max_count"] == 255
    assert result["output_voltage"] == pytest.approx(128 / 255 * 5)


def test_dac_minimum():
    result = calculate_dac(0, -10, 10, 16)

    assert result["output_voltage"] == pytest.approx(-10)


def test_dac_maximum():
    result = calculate_dac(65535, -10, 10, 16)

    assert result["output_voltage"] == pytest.approx(10)


def test_dac_rejects_count_above_maximum():
    with pytest.raises(ValueError):
        calculate_dac(4096, 0, 5, 12)


def test_dac_rejects_negative_count():
    with pytest.raises(ValueError):
        calculate_dac(-1, 0, 5, 12)


def test_dac_rejects_invalid_voltage_range():
    with pytest.raises(ValueError):
        calculate_dac(1000, 5, 0, 12)