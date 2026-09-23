import pytest

from wolfworks.electrical.calculations import (
    calculate_period,
    calculate_frequency,
    calculate_cycles_to_time,
    calculate_time_to_cycles,
    calculate_clock_divider,
    calculate_timer,
    calculate_pwm,
    frequency_to_hz,
    time_to_seconds,
)


# --------------------------------------------------
# Frequency / Period
# --------------------------------------------------

def test_frequency_to_period():
    period = calculate_period(50_000_000)

    assert period == pytest.approx(20e-9)


def test_period_to_frequency():
    frequency = calculate_frequency(20e-9)

    assert frequency == pytest.approx(50_000_000)


def test_frequency_rejects_zero():
    with pytest.raises(ValueError):
        calculate_period(0)


def test_period_rejects_zero():
    with pytest.raises(ValueError):
        calculate_frequency(0)


# --------------------------------------------------
# Clock Cycles / Time
# --------------------------------------------------

def test_cycles_to_time():
    time = calculate_cycles_to_time(
        50_000_000,
        12_500,
    )

    assert time == pytest.approx(250e-6)


def test_time_to_cycles():
    cycles = calculate_time_to_cycles(
        50_000_000,
        250e-6,
    )

    assert cycles == pytest.approx(12_500)


def test_cycles_reject_negative():
    with pytest.raises(ValueError):
        calculate_cycles_to_time(
            50_000_000,
            -1,
        )


def test_time_reject_negative():
    with pytest.raises(ValueError):
        calculate_time_to_cycles(
            50_000_000,
            -0.001,
        )


# --------------------------------------------------
# Clock Divider
# --------------------------------------------------

def test_exact_clock_divider():
    result = calculate_clock_divider(
        50_000_000,
        1_000,
    )

    assert result["ideal_divider"] == pytest.approx(50_000)
    assert result["divider"] == 50_000
    assert result["actual_frequency"] == pytest.approx(1_000)
    assert result["error_hz"] == pytest.approx(0)
    assert result["error_percent"] == pytest.approx(0)
    assert result["error_ppm"] == pytest.approx(0)


def test_clock_divider_rounding():
    result = calculate_clock_divider(
        50_000_000,
        44_100,
    )

    assert result["divider"] == round(
        50_000_000 / 44_100
    )

    assert result["actual_frequency"] == pytest.approx(
        50_000_000 / result["divider"]
    )


def test_clock_divider_rejects_zero_source():
    with pytest.raises(ValueError):
        calculate_clock_divider(
            0,
            1_000,
        )


def test_clock_divider_rejects_zero_target():
    with pytest.raises(ValueError):
        calculate_clock_divider(
            50_000_000,
            0,
        )


def test_clock_divider_rejects_target_above_source():
    with pytest.raises(ValueError):
        calculate_clock_divider(
            50_000_000,
            100_000_000,
        )


# --------------------------------------------------
# Counter / Timer
# --------------------------------------------------

def test_timer_exact_delay():
    result = calculate_timer(
        100_000_000,
        10e-3,
    )

    assert result["ideal_cycles"] == pytest.approx(
        1_000_000
    )

    assert result["cycles"] == 1_000_000

    assert result["actual_time"] == pytest.approx(
        10e-3
    )

    assert result["error_seconds"] == pytest.approx(0)
    assert result["error_percent"] == pytest.approx(0)

    assert result["counter_bits"] == 20


def test_timer_rounds_to_whole_clock_cycles():
    result = calculate_timer(
        1_000_000,
        10.4e-6,
    )

    assert result["ideal_cycles"] == pytest.approx(10.4)
    assert result["cycles"] == 10

    assert result["actual_time"] == pytest.approx(
        10e-6
    )


def test_timer_counter_width():
    result = calculate_timer(
        50_000_000,
        1e-3,
    )

    # 50,000 cycles require 16 bits.
    assert result["cycles"] == 50_000
    assert result["counter_bits"] == 16


def test_timer_rejects_zero_clock():
    with pytest.raises(ValueError):
        calculate_timer(
            0,
            1e-3,
        )


def test_timer_rejects_zero_time():
    with pytest.raises(ValueError):
        calculate_timer(
            50_000_000,
            0,
        )
        
# --------------------------------------------------
# PWM
# --------------------------------------------------

def test_pwm_exact():
    result = calculate_pwm(
        50_000_000,
        20_000,
        25,
    )

    assert result["period_counts"] == 2500
    assert result["high_counts"] == 625
    assert result["low_counts"] == 1875

    assert result["actual_frequency"] == pytest.approx(
        20_000
    )

    assert result["actual_duty_cycle"] == pytest.approx(
        25
    )

    assert result["frequency_error"] == pytest.approx(0)
    assert result["duty_error"] == pytest.approx(0)

    assert result["counter_bits"] == 12


def test_pwm_quantized_duty_cycle():
    result = calculate_pwm(
        1_000_000,
        100_000,
        33,
    )

    # 10 counts per period.
    assert result["period_counts"] == 10

    # 33% cannot be represented exactly with 10 counts.
    assert result["high_counts"] == 3
    assert result["low_counts"] == 7

    assert result["actual_duty_cycle"] == pytest.approx(
        30
    )

    assert result["duty_error"] == pytest.approx(
        -3
    )


def test_pwm_zero_percent_duty():
    result = calculate_pwm(
        1_000_000,
        1_000,
        0,
    )

    assert result["high_counts"] == 0
    assert result["low_counts"] == 1000
    assert result["actual_duty_cycle"] == pytest.approx(0)


def test_pwm_one_hundred_percent_duty():
    result = calculate_pwm(
        1_000_000,
        1_000,
        100,
    )

    assert result["high_counts"] == 1000
    assert result["low_counts"] == 0
    assert result["actual_duty_cycle"] == pytest.approx(100)


def test_pwm_rejects_negative_duty():
    with pytest.raises(ValueError):
        calculate_pwm(
            1_000_000,
            1_000,
            -1,
        )


def test_pwm_rejects_duty_above_100():
    with pytest.raises(ValueError):
        calculate_pwm(
            1_000_000,
            1_000,
            101,
        )


def test_pwm_rejects_zero_clock():
    with pytest.raises(ValueError):
        calculate_pwm(
            0,
            1_000,
            50,
        )


def test_pwm_rejects_zero_frequency():
    with pytest.raises(ValueError):
        calculate_pwm(
            1_000_000,
            0,
            50,
        )


def test_pwm_rejects_frequency_above_clock():
    with pytest.raises(ValueError):
        calculate_pwm(
            1_000_000,
            2_000_000,
            50,
        )
        
# --------------------------------------------------
# Unit Conversion
# --------------------------------------------------

@pytest.mark.parametrize(
    "value, unit, expected",
    [
        (50, "Hz", 50),
        (50, "kHz", 50_000),
        (50, "MHz", 50_000_000),
        (2.5, "GHz", 2_500_000_000),
    ],
)
def test_frequency_to_hz(value, unit, expected):
    assert frequency_to_hz(
        value,
        unit,
    ) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value, unit, expected",
    [
        (2, "s", 2),
        (20, "ms", 20e-3),
        (250, "us", 250e-6),
        (20, "ns", 20e-9),
        (500, "ps", 500e-12),
    ],
)
def test_time_to_seconds(value, unit, expected):
    assert time_to_seconds(
        value,
        unit,
    ) == pytest.approx(expected)


def test_frequency_to_hz_rejects_invalid_unit():
    with pytest.raises(
        ValueError,
        match="Invalid frequency unit",
    ):
        frequency_to_hz(
            50,
            "bananas",
        )


def test_time_to_seconds_rejects_invalid_unit():
    with pytest.raises(
        ValueError,
        match="Invalid time unit",
    ):
        time_to_seconds(
            20,
            "minutes",
        )