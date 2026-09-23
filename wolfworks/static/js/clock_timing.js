document.addEventListener("DOMContentLoaded", () => {
    const modeSelect = document.getElementById("mode");

    const modes = {
        frequency_period:
            document.getElementById(
                "frequency-period-fields"
            ),

        cycles_time:
            document.getElementById(
                "cycles-time-fields"
            ),

        clock_divider:
            document.getElementById(
                "clock-divider-fields"
            ),

        timer:
            document.getElementById(
                "timer-fields"
            ),

        pwm:
            document.getElementById(
                "pwm-fields"
            ),
    };


    function setSectionEnabled(section, enabled) {
        section.style.display = enabled
            ? ""
            : "none";

        const fields = section.querySelectorAll(
            "input, select, textarea, button"
        );

        fields.forEach((field) => {
            field.disabled = !enabled;
        });
    }


    function updateMode() {
        const selectedMode = modeSelect.value;

        Object.entries(modes).forEach(
            ([modeName, section]) => {
                setSectionEnabled(
                    section,
                    modeName === selectedMode
                );
            }
        );

        updateDirection();
    }


    function updateDirection() {
        const selectedMode = modeSelect.value;

        if (selectedMode === "frequency_period") {
            updateFrequencyPeriod();
        }

        if (selectedMode === "cycles_time") {
            updateCyclesTime();
        }
    }


    function updateFrequencyPeriod() {
        const section = modes.frequency_period;

        if (section.style.display === "none") {
            return;
        }

        const direction = section.querySelector(
            'input[name="direction"]:checked'
        );

        if (!direction) {
            return;
        }

        const frequencyInput =
            document.getElementById(
                "frequency-input"
            );

        const periodInput =
            document.getElementById(
                "period-input"
            );

        const frequencySelected =
            direction.value ===
            "frequency_to_period";

        setSectionEnabled(
            frequencyInput,
            frequencySelected
        );

        setSectionEnabled(
            periodInput,
            !frequencySelected
        );
    }


    function updateCyclesTime() {
        const section = modes.cycles_time;

        if (section.style.display === "none") {
            return;
        }

        const direction = section.querySelector(
            'input[name="direction"]:checked'
        );

        if (!direction) {
            return;
        }

        const cyclesInput =
            document.getElementById(
                "cycles-input"
            );

        const timeInput =
            document.getElementById(
                "time-input"
            );

        const cyclesSelected =
            direction.value ===
            "cycles_to_time";

        setSectionEnabled(
            cyclesInput,
            cyclesSelected
        );

        setSectionEnabled(
            timeInput,
            !cyclesSelected
        );
    }


    modeSelect.addEventListener(
        "change",
        updateMode
    );


    document
        .querySelectorAll(
            'input[name="direction"]'
        )
        .forEach((radio) => {
            radio.addEventListener(
                "change",
                updateDirection
            );
        });


    updateMode();
});