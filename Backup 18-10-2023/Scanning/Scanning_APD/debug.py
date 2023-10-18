
# Single QUA script generated at 2023-09-25 17:34:24.614161
# QUA library version: 1.1.3

from qm.qua import *

with program() as prog:
    a1 = declare(int, size=16000)
    v1 = declare(int, )
    v2 = declare(int, )
    with infinite_loop_():
        measure("readout", "SPCM", None, time_tagging.analog(a1, 60000000, v1, ""))
        r1 = declare_stream()
        save(v1, r1)
    with stream_processing():
        r1.with_timestamps().save("counts")


config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                "1": {
                    "offset": 0.0,
                },
                "2": {
                    "offset": 0.0,
                },
                "3": {
                    "offset": 0.0,
                },
                "4": {
                    "offset": 0.0,
                },
                "5": {
                    "offset": 0.0,
                },
            },
            "digital_outputs": {
                "1": {},
                "2": {},
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.0,
                },
            },
        },
    },
    "elements": {
        "spin1": {
            "singleInput": {
                "port": ('con1', 1),
            },
            "intermediate_frequency": 0.0,
            "operations": {
                "const": "constPulse",
                "gaussian": "gaussianPulse",
            },
        },
        "AOM": {
            "singleInput": {
                "port": ('con1', 5),
            },
            "intermediate_frequency": 0,
            "operations": {
                "const": "constPulse_AOM",
            },
        },
        "spin2": {
            "singleInput": {
                "port": ('con1', 2),
            },
            "intermediate_frequency": 20000000.0,
            "operations": {
                "const": "constPulse",
                "gaussian": "gaussianPulse",
            },
        },
        "spin3": {
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 1000000000.0,
            },
            "intermediate_frequency": 30000000.0,
            "hold_offset": {
                "duration": 1,
            },
            "operations": {
                "const": "constPulse_IQ",
                "gaussian": "gaussian_Pulse_IQ",
            },
        },
        "photon_source": {
            "singleInput": {
                "port": ('con1', 1),
            },
            "intermediate_frequency": 0,
            "operations": {
                "gauss": "nuclear_gauss_pulse",
            },
        },
        "digital1": {
            "digitalInputs": {
                "digital": {
                    "buffer": 0,
                    "delay": 0,
                    "port": ('con1', 1),
                },
            },
            "operations": {
                "ON": "digital_ON",
            },
        },
        "SPCM": {
            "singleInput": {
                "port": ('con1', 1),
            },
            "digitalInputs": {
                "marker": {
                    "port": ('con1', 2),
                    "delay": 80,
                    "buffer": 0,
                },
            },
            "operations": {
                "readout": "readout_pulse",
                "long_readout": "long_readout_pulse",
            },
            "outputs": {
                "out1": ('con1', 1),
            },
            "outputPulseParameters": {
                "signalThreshold": -500,
                "signalPolarity": "Descending",
                "derivativeThreshold": 1023,
                "derivativePolarity": "Descending",
            },
            "time_of_flight": 80,
            "smearing": 0,
        },
    },
    "pulses": {
        "constPulse": {
            "operation": "control",
            "length": 100,
            "waveforms": {
                "single": "const_wf",
            },
        },
        "constPulse_IQ": {
            "operation": "control",
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
        },
        "constPulse_AOM": {
            "operation": "control",
            "length": 1000,
            "waveforms": {
                "single": "AOM_const_wf",
            },
        },
        "nuclear_gauss_pulse": {
            "operation": "control",
            "length": 80,
            "waveforms": {
                "single": "gauss_wf",
            },
        },
        "gaussian_Pulse_IQ": {
            "operation": "control",
            "length": 80,
            "waveforms": {
                "I": "gauss_wf",
                "Q": "zero_wf",
            },
        },
        "gaussianPulse": {
            "operation": "control",
            "length": 80,
            "waveforms": {
                "single": "gauss_wf",
            },
        },
        "laser_on": {
            "digital_marker": "ON",
            "operation": "measurement",
            "length": 1000,
            "waveforms": {
                "single": "zero_wf",
            },
        },
        "digital_ON": {
            "digital_marker": "ON",
            "length": 100,
            "operation": "control",
        },
        "readout_pulse": {
            "operation": "measurement",
            "length": 5000,
            "digital_marker": "ON",
            "waveforms": {
                "single": "zero_wf",
            },
        },
        "long_readout_pulse": {
            "operation": "measurement",
            "length": 1000,
            "digital_marker": "ON",
            "waveforms": {
                "single": "zero_wf",
            },
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
        "short": {
            "samples": [(1, 8), (0, 8)],
        },
    },
    "waveforms": {
        "const_wf": {
            "type": "constant",
            "sample": 0.2,
        },
        "zero_wf": {
            "type": "constant",
            "sample": 0.0,
        },
        "gauss_wf": {
            "type": "arbitrary",
            "samples": [6.709252558050238e-05, 9.95910843006547e-05, 0.00014636048377609457, 0.0002129532473335841, 0.0003067621358648926, 0.00043749822363657706, 0.0006177430816473538, 0.0008635680015266156, 0.0011952045790011886, 0.0016377402028748167, 0.0022217993076484614, 0.0029841572138135687, 0.003968218948874057, 0.005224281970783647, 0.006809490946919869, 0.008787386724681484, 0.011226952566826745, 0.014201070747927397, 0.01778432349187727, 0.022050105060897045, 0.027067056647322542, 0.03289489131543098, 0.039579739816722935, 0.04714921531117271, 0.05560746009063883, 0.06493049347166995, 0.07506221977027992, 0.08591147164214784, 0.09735045119199434, 0.10921488532794188, 0.1213061319425267, 0.13339536217169487, 0.1452298074147382, 0.15654090764837364, 0.1670540422822544, 0.1764993805169191, 0.18462326927732717, 0.19119949636662, 0.19603973466135105, 0.19900249583853646, 0.2, 0.19900249583853646, 0.19603973466135105, 0.19119949636662, 0.18462326927732717, 0.1764993805169191, 0.1670540422822544, 0.15654090764837364, 0.1452298074147382, 0.13339536217169487, 0.1213061319425267, 0.10921488532794188, 0.09735045119199434, 0.08591147164214784, 0.07506221977027992, 0.06493049347166995, 0.05560746009063883, 0.04714921531117271, 0.039579739816722935, 0.03289489131543098, 0.027067056647322542, 0.022050105060897045, 0.01778432349187727, 0.014201070747927397, 0.011226952566826745, 0.008787386724681484, 0.006809490946919869, 0.005224281970783647, 0.003968218948874057, 0.0029841572138135687, 0.0022217993076484614, 0.0016377402028748167, 0.0011952045790011886, 0.0008635680015266156, 0.0006177430816473538, 0.00043749822363657706, 0.0003067621358648926, 0.0002129532473335841, 0.00014636048377609457, 9.95910843006547e-05],
        },
        "AOM_const_wf": {
            "type": "constant",
            "sample": 0.5,
        },
    },
}

loaded_config = {
    "version": 1,
    "controllers": {
        "con1": {
            "type": "opx1",
            "analog_outputs": {
                "1": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "2": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "3": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "4": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
                "5": {
                    "offset": 0.0,
                    "delay": 0,
                    "shareable": False,
                },
            },
            "analog_inputs": {
                "1": {
                    "offset": 0.0,
                    "gain_db": 0,
                    "shareable": False,
                },
            },
            "digital_outputs": {
                "1": {
                    "shareable": False,
                    "inverted": False,
                },
                "2": {
                    "shareable": False,
                    "inverted": False,
                },
            },
        },
    },
    "oscillators": {},
    "elements": {
        "spin1": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 0.0,
            "operations": {
                "const": "constPulse",
                "gaussian": "gaussianPulse",
            },
            "singleInput": {
                "port": ('con1', 1),
            },
        },
        "AOM": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 0.0,
            "operations": {
                "const": "constPulse_AOM",
            },
            "singleInput": {
                "port": ('con1', 5),
            },
        },
        "spin2": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 20000000.0,
            "operations": {
                "const": "constPulse",
                "gaussian": "gaussianPulse",
            },
            "singleInput": {
                "port": ('con1', 2),
            },
        },
        "spin3": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 30000000.0,
            "operations": {
                "const": "constPulse_IQ",
                "gaussian": "gaussian_Pulse_IQ",
            },
            "mixInputs": {
                "I": ('con1', 3),
                "Q": ('con1', 4),
                "lo_frequency": 1000000000.0,
            },
            "sticky": {
                "analog": True,
                "digital": False,
                "duration": 1,
            },
        },
        "photon_source": {
            "digitalInputs": {},
            "digitalOutputs": {},
            "intermediate_frequency": 0.0,
            "operations": {
                "gauss": "nuclear_gauss_pulse",
            },
            "singleInput": {
                "port": ('con1', 1),
            },
        },
        "digital1": {
            "digitalInputs": {
                "digital": {
                    "delay": 0,
                    "buffer": 0,
                    "port": ('con1', 1),
                },
            },
            "digitalOutputs": {},
            "operations": {
                "ON": "digital_ON",
            },
        },
        "SPCM": {
            "digitalInputs": {
                "marker": {
                    "delay": 80,
                    "buffer": 0,
                    "port": ('con1', 2),
                },
            },
            "digitalOutputs": {},
            "outputs": {
                "out1": ('con1', 1),
            },
            "time_of_flight": 80,
            "smearing": 0,
            "operations": {
                "readout": "readout_pulse",
                "long_readout": "long_readout_pulse",
            },
            "singleInput": {
                "port": ('con1', 1),
            },
        },
    },
    "pulses": {
        "constPulse": {
            "length": 100,
            "waveforms": {
                "single": "const_wf",
            },
            "operation": "control",
        },
        "constPulse_IQ": {
            "length": 100,
            "waveforms": {
                "I": "const_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "constPulse_AOM": {
            "length": 1000,
            "waveforms": {
                "single": "AOM_const_wf",
            },
            "operation": "control",
        },
        "nuclear_gauss_pulse": {
            "length": 80,
            "waveforms": {
                "single": "gauss_wf",
            },
            "operation": "control",
        },
        "gaussian_Pulse_IQ": {
            "length": 80,
            "waveforms": {
                "I": "gauss_wf",
                "Q": "zero_wf",
            },
            "operation": "control",
        },
        "gaussianPulse": {
            "length": 80,
            "waveforms": {
                "single": "gauss_wf",
            },
            "operation": "control",
        },
        "laser_on": {
            "length": 1000,
            "waveforms": {
                "single": "zero_wf",
            },
            "digital_marker": "ON",
            "operation": "measurement",
        },
        "digital_ON": {
            "length": 100,
            "digital_marker": "ON",
            "operation": "control",
        },
        "readout_pulse": {
            "length": 5000,
            "waveforms": {
                "single": "zero_wf",
            },
            "digital_marker": "ON",
            "operation": "measurement",
        },
        "long_readout_pulse": {
            "length": 1000,
            "waveforms": {
                "single": "zero_wf",
            },
            "digital_marker": "ON",
            "operation": "measurement",
        },
    },
    "waveforms": {
        "const_wf": {
            "sample": 0.2,
            "type": "constant",
        },
        "zero_wf": {
            "sample": 0.0,
            "type": "constant",
        },
        "gauss_wf": {
            "samples": [6.709252558050238e-05, 9.95910843006547e-05, 0.00014636048377609457, 0.0002129532473335841, 0.0003067621358648926, 0.00043749822363657706, 0.0006177430816473538, 0.0008635680015266156, 0.0011952045790011886, 0.0016377402028748167, 0.0022217993076484614, 0.0029841572138135687, 0.003968218948874057, 0.005224281970783647, 0.006809490946919869, 0.008787386724681484, 0.011226952566826745, 0.014201070747927397, 0.01778432349187727, 0.022050105060897045, 0.027067056647322542, 0.03289489131543098, 0.039579739816722935, 0.04714921531117271, 0.05560746009063883, 0.06493049347166995, 0.07506221977027992, 0.08591147164214784, 0.09735045119199434, 0.10921488532794188, 0.1213061319425267, 0.13339536217169487, 0.1452298074147382, 0.15654090764837364, 0.1670540422822544, 0.1764993805169191, 0.18462326927732717, 0.19119949636662, 0.19603973466135105, 0.19900249583853646, 0.2, 0.19900249583853646, 0.19603973466135105, 0.19119949636662, 0.18462326927732717, 0.1764993805169191, 0.1670540422822544, 0.15654090764837364, 0.1452298074147382, 0.13339536217169487, 0.1213061319425267, 0.10921488532794188, 0.09735045119199434, 0.08591147164214784, 0.07506221977027992, 0.06493049347166995, 0.05560746009063883, 0.04714921531117271, 0.039579739816722935, 0.03289489131543098, 0.027067056647322542, 0.022050105060897045, 0.01778432349187727, 0.014201070747927397, 0.011226952566826745, 0.008787386724681484, 0.006809490946919869, 0.005224281970783647, 0.003968218948874057, 0.0029841572138135687, 0.0022217993076484614, 0.0016377402028748167, 0.0011952045790011886, 0.0008635680015266156, 0.0006177430816473538, 0.00043749822363657706, 0.0003067621358648926, 0.0002129532473335841, 0.00014636048377609457, 9.95910843006547e-05],
            "type": "arbitrary",
            "is_overridable": False,
            "max_allowed_error": 0.0001,
        },
        "AOM_const_wf": {
            "sample": 0.5,
            "type": "constant",
        },
    },
    "digital_waveforms": {
        "ON": {
            "samples": [(1, 0)],
        },
        "short": {
            "samples": [(1, 8), (0, 8)],
        },
    },
    "integration_weights": {},
    "mixers": {},
}


