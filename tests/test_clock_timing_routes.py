# --------------------------------------------------
# Page
# --------------------------------------------------

def test_clock_timing_page_loads(client):
    response = client.get(
        "/electrical/clock-timing/"
    )

    assert response.status_code == 200
    assert b"Digital Clock & Timing" in response.data


# --------------------------------------------------
# Frequency / Period
# --------------------------------------------------

def test_route_frequency_to_period(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "frequency_period",
            "direction": "frequency_to_period",
            "frequency": "50",
            "frequency_unit": "MHz",
        },
    )

    assert response.status_code == 200

    # 50 MHz = 20 ns
    assert b"50 MHz" in response.data
    assert b"20 ns" in response.data


def test_route_period_to_frequency(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "frequency_period",
            "direction": "period_to_frequency",
            "period": "20",
            "period_unit": "ns",
        },
    )

    assert response.status_code == 200

    # 20 ns = 50 MHz
    assert b"50 MHz" in response.data
    assert b"20 ns" in response.data


# --------------------------------------------------
# Cycles / Time
# --------------------------------------------------

def test_route_cycles_to_time(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "cycles_time",
            "direction": "cycles_to_time",
            "clock_frequency": "50",
            "clock_frequency_unit": "MHz",
            "cycles": "12500",
        },
    )

    assert response.status_code == 200

    # 12,500 cycles at 50 MHz = 250 us
    assert b"12500" in response.data
    assert b"250" in response.data


def test_route_time_to_cycles(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "cycles_time",
            "direction": "time_to_cycles",
            "clock_frequency": "50",
            "clock_frequency_unit": "MHz",
            "time": "250",
            "time_unit": "us",
        },
    )

    assert response.status_code == 200
    assert b"12500" in response.data


# --------------------------------------------------
# Clock Divider
# --------------------------------------------------

def test_route_clock_divider(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "clock_divider",
            "source_frequency": "50",
            "source_frequency_unit": "MHz",
            "target_frequency": "1",
            "target_frequency_unit": "kHz",
        },
    )

    assert response.status_code == 200

    assert b"50000" in response.data
    assert b"1 kHz" in response.data


# --------------------------------------------------
# Counter / Timer
# --------------------------------------------------

def test_route_timer(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "timer",
            "clock_frequency": "100",
            "clock_frequency_unit": "MHz",
            "target_time": "10",
            "target_time_unit": "ms",
        },
    )

    assert response.status_code == 200

    assert b"1000000" in response.data
    assert b"999999" in response.data
    assert b"20 bits" in response.data


# --------------------------------------------------
# PWM
# --------------------------------------------------

def test_route_pwm(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "pwm",
            "clock_frequency": "50",
            "clock_frequency_unit": "MHz",
            "target_frequency": "20",
            "target_frequency_unit": "kHz",
            "duty_cycle": "25",
        },
    )

    assert response.status_code == 200

    assert b"2500" in response.data
    assert b"625" in response.data
    assert b"1875" in response.data
    assert b"12 bits" in response.data


# --------------------------------------------------
# Validation
# --------------------------------------------------

def test_route_rejects_invalid_mode(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "warp_drive",
        },
    )

    assert response.status_code == 200
    assert b"Invalid clock calculation mode." in response.data


def test_route_rejects_invalid_frequency_unit(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "frequency_period",
            "direction": "frequency_to_period",
            "frequency": "50",
            "frequency_unit": "bananas",
        },
    )

    assert response.status_code == 200
    assert b"Invalid frequency unit." in response.data


def test_route_rejects_invalid_time_unit(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "frequency_period",
            "direction": "period_to_frequency",
            "period": "20",
            "period_unit": "minutes",
        },
    )

    assert response.status_code == 200
    assert b"Invalid time unit." in response.data


def test_route_rejects_zero_frequency(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "frequency_period",
            "direction": "frequency_to_period",
            "frequency": "0",
            "frequency_unit": "Hz",
        },
    )

    assert response.status_code == 200
    assert b"Error:" in response.data
    
    
    
    
def test_route_preserves_pwm_form_values(client):
    response = client.post(
        "/electrical/clock-timing/",
        data={
            "mode": "pwm",
            "clock_frequency": "73.5",
            "clock_frequency_unit": "MHz",
            "target_frequency": "17.25",
            "target_frequency_unit": "kHz",
            "duty_cycle": "37.5",
        },
    )

    assert response.status_code == 200

    html = response.get_data(as_text=True)

    assert 'value="73.5"' in html
    assert 'value="17.25"' in html
    assert 'value="37.5"' in html

    assert 'value="pwm"' in html