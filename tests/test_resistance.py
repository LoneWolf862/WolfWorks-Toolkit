import pytest

from wolfworks.electrical.calculations import calculate_resistance


def test_series_resistance():
    result = calculate_resistance(
        [100, 220, 470],
        "series",
    )

    assert result["equivalent_resistance"] == pytest.approx(790)


def test_parallel_equal_resistors():
    result = calculate_resistance(
        [100, 100],
        "parallel",
    )

    assert result["equivalent_resistance"] == pytest.approx(50)


def test_parallel_unequal_resistors():
    result = calculate_resistance(
        [100, 200],
        "parallel",
    )

    assert result["equivalent_resistance"] == pytest.approx(66.6666667)


def test_requires_two_resistors():
    with pytest.raises(ValueError):
        calculate_resistance([100], "series")


def test_rejects_zero_resistance():
    with pytest.raises(ValueError):
        calculate_resistance([100, 0], "parallel")


def test_rejects_negative_resistance():
    with pytest.raises(ValueError):
        calculate_resistance([100, -220], "series")


def test_rejects_invalid_configuration():
    with pytest.raises(ValueError):
        calculate_resistance([100, 220], "banana")