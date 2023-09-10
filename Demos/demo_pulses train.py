"""calling function libraries"""
import math

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from Configuration import *
import matplotlib.pyplot as plt


def test(element):
    i = declare(int)
    with for_(i, 0, i < 5, i+1):
        play('gaussian', element)
        wait(50, element)

"""The QUA program"""
with program() as prog:
    counts = declare(int)
    time_stamps = declare(int,size=100)
    wait_time = declare(int)
    update_frequency('spin1', 50e6)
    #with for_(wait_time, 100, wait_time < 100, wait_time + 100):
    with infinite_loop_():
        play('gaussian'*amp(0.5),'spin1',duration=200)
        wait(1000,'spin1')
        # play('gaussian'*amp(0.5),'spin1',duration=200)
        # align('spin1','SPCM')
        # measure('readout', 'SPCM', None,time_tagging.analog(time_stamps,300,counts))
"""Manual Output Control"""
#from qualang_tools.control_panel import ManualOutputControl
#manual_output_control = ManualOutputControl.ports(analog_ports=[1],digital_ports=[1])
#manual_output_control.set_frequency(1,3*10^3)
#manual_output_control.set_amplitude(1,0.25)

"""defining a quantum machine"""
QMm = QuantumMachinesManager(host='192.168.88.10', port='80')

QM1 = QMm.open_qm(config)  # calling the configuration file
job = QM1.simulate(
    prog, SimulationConfig(int(5000))
)  # running a simulation for a specific time in clock cycles, 4 ns

"""getting the simulated samples of the OPX output and plotting them"""
samples = job.get_simulated_samples()
samples.con1.plot()

job = QM1.execute(prog)

