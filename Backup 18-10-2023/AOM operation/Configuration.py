import numpy as np


def gauss(amplitude, mu, sigma, length):
    t = np.linspace(-length / 2, length / 2 - 1, length)
    gauss_wave = amplitude * np.exp(-((t - mu) ** 2) / (2 * sigma ** 2))
    return [float(x) for x in gauss_wave]

# Readout parameters
signal_threshold = -500

# Delays
detection_delay = 80

short_pulse = []
for i in range(1):
    for i in range(2):
        short_pulse.append(0.2)
    for i in range(14):
        short_pulse.append(0.0)

short_pulse_length = 16
pulse_len = 80
gauss_pulse = gauss(0.2, 0, 10, pulse_len)
meas_len = 100
long_meas_len = 1000
# AOM parameters
AOM_amp = 0.5  # Volts
AOM_frequency = 0  # Hz
AOM_pulse_length = 1e6 # ns
config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                1: {"offset": +0.0},
                2: {"offset": +0.0},
                3: {"offset": +0.0},
                4: {"offset": +0.0},
            },
            "digital_outputs": {
                1: {},
                2: {},
            },
            "analog_inputs": {
                1: {"offset": 0.0},
            },
        }
    },
    "elements": {
        "spin1": {
            "singleInput": {"port": ("con1", 1)},
            "digitalInputs": {
                "laser": {"buffer": 0, "delay": 0, "port": ("con1", 1)},
            },
            "outputs": {"out1": ("con1", 1)},
            "time_of_flight": 28,
            "smearing": 0,
            "intermediate_frequency": 0e6,
            # "hold_offset": {"duration": 16},
            "operations": {
                "const": "constPulse",
                "short": "shortPulse",
                "gaussian": "gaussianPulse",
                "readout": "laser_on",
            },
        },
        "AOM": {
            "singleInput": {"port": ("con1", 1)},
            "intermediate_frequency": AOM_frequency,
            "operations": {
                "const": "constPulse_AOM",
            },
        },

        "spin2": {
            "singleInput": {"port": ("con1", 2)},
            "digitalInputs": {
                "laser": {"buffer": 0, "delay": 0, "port": ("con1", 2)},
            },
            "outputs": {"out1": ("con1", 1)},
            "time_of_flight": 28,
            "smearing": 0,
            "intermediate_frequency": 20e6,
            # "hold_offset": {"duration": 16},
            "operations": {
                "const": "constPulse",
                "gaussian": "gaussianPulse",
                "readout": "laser_on",
            },
        },

        "spin3": {
            "mixInputs": {
                "I": ("con1", 3),
                "Q": ("con1", 4),
                "lo_frequency": 1e9,
            },
            "intermediate_frequency": 30e6,
            "hold_offset": {"duration": 1},
            "operations": {
                "const": "constPulse_IQ",
                "gaussian": "gaussian_Pulse_IQ",
            },
        },

        "digital1": {
            "digitalInputs": {
                "digital": {"buffer": 0, "delay": 0, "port": ("con1", 1)},
            },
            "operations": {
                "ON": "digital_ON",
                "short": "digital_short",
            },
        },

        "SPCM": {
            "singleInput": {"port": ("con1", 1)},  # not used
            "digitalInputs": {
                "marker": {
                    "port": ("con1", 2),
                    "delay": detection_delay,
                    "buffer": 0,
                },
            },
            "operations": {
                "readout": "readout_pulse",
                "long_readout": "long_readout_pulse",
            },
            "outputs": {"out1": ("con1", 1)},
            "outputPulseParameters": {
                "signalThreshold": signal_threshold,
                "signalPolarity": "Descending",
                "derivativeThreshold": 1023,
                "derivativePolarity": "Descending",
            },
            "time_of_flight": detection_delay,
            "smearing": 0,
        },
    },
    "pulses": {
        "constPulse": {
            "operation": "control",
            "length": 100,  # in ns
            "waveforms": {"single": "const_wf"},
        },
        "constPulse_AOM": {
            "operation": "control",
            "length": AOM_pulse_length,  # in ns
            "waveforms": {"single": "AOM_const_wf"},
        },
        "shortPulse": {
            "operation": "control",
            "length": short_pulse_length,  # in ns
            "waveforms": {"single": "short_wf"},
        },
        "constPulse_IQ": {
            "operation": "control",
            "length": 100,  # in ns
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "gaussian_Pulse_IQ": {
            "operation": "control",
            "length": pulse_len,  # in ns
            "waveforms": {
                "I": "gauss_wf",
                "Q": "zero_wf",
            },
        },
        "gaussianPulse": {
            "operation": "control",
            "length": pulse_len,  # in ns
            "waveforms": {"single": "gauss_wf"},
        },
        "laser_on": {
            "digital_marker": "ON",
            "operation": "measurement",
            "length": 1000,  # in ns
            "waveforms": {"single": "zero_wf"},
        },
        "digital_ON": {
            "digital_marker": "ON",
            "length": 100,
            "operation": "control",
        },
        "digital_short": {
            "digital_marker": "short",
            "length": 1e5,
            "operation": "control",
        },
        "readout_pulse": {
            "operation": "measurement",
            "length": meas_len,
            "digital_marker": "ON",
            "waveforms": {"single": "zero_wf"},
        },
        "long_readout_pulse": {
            "operation": "measurement",
            "length": long_meas_len,
            "digital_marker": "ON",
            "waveforms": {"single": "zero_wf"},
        },
    },
    "digital_waveforms": {
        "ON": {"samples": [(1, 0)]},
        "short": {"samples": [(1, 0.5*1e5),(0, 0.5*1e5)]},
    },
    "waveforms": {
        "const_wf": {"type": "constant", "sample": 0.2},
        "AOM_const_wf": {"type": "constant", "sample": AOM_amp},
        "zero_wf": {"type": "constant", "sample": 0.0},
        "gauss_wf": {"type": "arbitrary", "samples": gauss_pulse},
        "short_wf": {"type": "arbitrary", "samples": short_pulse},
    },
}