from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
import matplotlib.pyplot as plt
from configuration import *

###################
# The QUA program #
###################


with program() as TimeTagging_calibration:
    raw_adc_st = declare_stream(adc_trace=True)
    j = declare(int)
    measure("long_readout", "SPCM", raw_adc_st)
    wait(1000, "SPCM")

    with stream_processing():
        raw_adc_st.input1().save("raw_adc")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port)

qm = qmm.open_qm(config)

job = qm.execute(TimeTagging_calibration)
job.result_handles.wait_for_all_values()
res_handles = job.result_handles
raw_data = res_handles.get("raw_adc").fetch_all()
plt.plot(raw_data)
plt.title("ADC Trace Check ADCs saturation and define threshold")

