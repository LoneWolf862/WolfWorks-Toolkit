import pytest

from wolfworks.electrical.calculations import calculate_linear_scaling


def test_4_20ma_to_0_300psi():
    result = calculate_linear_scaling(
        14,
        4,
        20,
        0,
        300,
    )

    assert result["output_value"] == pytest.approx(187.5)
    assert result["percentage"] == pytest.approx(62.5)


def test_0_10v_to_0_100_percent():
    result = calculate_linear_scaling(
        5,
        0,
        10,
        0,
        100,
    )

    assert result["output_value"] == pytest.approx(50)
    assert result["percentage"] == pytest.approx(50)


def test_zero_percent():
    result = calculate_linear_scaling(
        4,
        4,
        20,
        0,
        300,
    )

    assert result["output_value"] == pytest.approx(0)
    assert result["percentage"] == pytest.approx(0)


def test_one_hundred_percent():
    result = calculate_linear_scaling(
        20,
        4,
        20,
        0,
        300,
    )

    assert result["output_value"] == pytest.approx(300)
    assert result["percentage"] == pytest.approx(100)


def test_reverse_scaling():
    result = calculate_linear_scaling(
        187.5,
        0,
        300,
        4,
        20,
    )

    assert result["output_value"] == pytest.approx(14)
    assert result["percentage"] == pytest.approx(62.5)


def test_negative_range():
    result = calculate_linear_scaling(
        0,
        -10,
        10,
        0,
        100,
    )

    assert result["output_value"] == pytest.approx(50)
    assert result["percentage"] == pytest.approx(50)


def test_raw_plc_counts():
    result = calculate_linear_scaling(
        16383.5,
        0,
        32767,
        0,
        100,
    )

    assert result["output_value"] == pytest.approx(50)
    assert result["percentage"] == pytest.approx(50)


def test_below_range_raises_error():
    with pytest.raises(
        ValueError,
        match="Input value must be within",
    ):
        calculate_linear_scaling(
            2,
            4,
            20,
            0,
            100,
        )


def test_above_range_raises_error():
    with pytest.raises(
        ValueError,
        match="Input value must be within",
    ):
        calculate_linear_scaling(
            22,
            4,
            20,
            0,
            100,
        )


def test_equal_input_limits_raise_error():
    with pytest.raises(ValueError):
        calculate_linear_scaling(
            5,
            10,
            10,
            0,
            100,
        )