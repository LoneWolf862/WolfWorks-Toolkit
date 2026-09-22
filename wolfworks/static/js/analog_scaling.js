document.addEventListener("DOMContentLoaded", function () {

    const preset = document.getElementById("signal_preset");
    const signalMin = document.getElementById("signal_min");
    const signalMax = document.getElementById("signal_max");
    const signalUnit = document.getElementById("signal_unit");


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
        },

        "0-4095": {
            min: 0,
            max: 4095,
            unit: "counts"
        },

        "0-32767": {
            min: 0,
            max: 32767,
            unit: "counts"
        },

        "0-65535": {
            min: 0,
            max: 65535,
            unit: "counts"
        }

    };


    preset.addEventListener("change", function () {

        const selectedPreset = presets[preset.value];

        if (!selectedPreset) {
            return;
        }

        signalMin.value = selectedPreset.min;
        signalMax.value = selectedPreset.max;
        signalUnit.value = selectedPreset.unit;

    });

});