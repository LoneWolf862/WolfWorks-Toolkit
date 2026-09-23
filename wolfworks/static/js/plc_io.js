document.addEventListener("DOMContentLoaded", function () {
    const ioType = document.getElementById("io_type");
    const analogFields = document.getElementById("analog-fields");

    function updateAnalogFields() {
        const isAnalog =
            ioType.value === "AI" ||
            ioType.value === "AO";

        analogFields.style.display =
            isAnalog ? "block" : "none";
    }

    ioType.addEventListener(
        "change",
        updateAnalogFields
    );

	const signalPreset =
		document.getElementById("signal_preset");

	const signalMin =
		document.getElementById("signal_min");

	const signalMax =
		document.getElementById("signal_max");

	const signalUnit =
		document.getElementById("signal_unit");


	const presets = {
		"4-20ma": {
			min: 4,
			max: 20,
			unit: "mA"
		},

		"0-20ma": {
			min: 0,
			max: 20,
			unit: "mA"
		},

		"0-10v": {
			min: 0,
			max: 10,
			unit: "V"
		},

		"0-5v": {
			min: 0,
			max: 5,
			unit: "V"
		},

		"1-5v": {
			min: 1,
			max: 5,
			unit: "V"
		},

		"-10-10v": {
			min: -10,
			max: 10,
			unit: "V"
		}
	};


	signalPreset.addEventListener("change", function () {
		const preset = presets[signalPreset.value];

		if (!preset) {
			return;
		}

		signalMin.value = preset.min;
		signalMax.value = preset.max;
		signalUnit.value = preset.unit;
	});


    updateAnalogFields();
});