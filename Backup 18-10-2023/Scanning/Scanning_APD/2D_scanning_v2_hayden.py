import tkinter as tk
from tkinter import ttk
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from motorized_stage import MotorizedStageApp
import threading

from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
import matplotlib.pyplot as plt
from configuration import *
from qm import LoopbackInterface

###################
# The QUA program #
###################

total_integration_time = int(1000 * u.ms)  # 100ms
single_integration_time_ns = int(1000 * u.us)  # 500us
single_integration_time_cycles = single_integration_time_ns // 4
n_count = int(total_integration_time / single_integration_time_ns)


with program() as counter:
    times = declare(int, size=100)
    counts = declare(int)
    total_counts = declare(int)
    n = declare(int)
    m = declare(int)
    counts_st = declare_stream()
#    with infinite_loop_():
#        with for_(m, 0, m < 10, m + 1):
#            play("gauss", "photon_source", condition= Random().rand_fixed() > 0.95)  # plays single_photon operation on qubit
#            wait(100, "photon_source")  # qubit waits 4 clock cycles (16 ns)

#    with infinite_loop_():
#        with for_(n, 0, n < n_count, n + 1):
#            measure("readout", "SPCM", None, time_tagging.analog(times, single_integration_time_ns, counts))
#            assign(total_counts, total_counts + counts)
#        save(total_counts, counts_st)
#        assign(total_counts, 0)


    measure("readout", "SPCM", None, time_tagging.analog(times, single_integration_time_ns, counts))
    save(total_counts, counts_st)
    with stream_processing():
        counts_st.with_timestamps().save("counts")

#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host='192.168.88.10', port='80')



qm = qmm.open_qm(config)

job = qm.execute(counter)
# Get results from QUA program
res_handles = job.result_handles
counts_handle = res_handles.get("counts")
counts_handle.wait_for_values(1)

# new_counts = counts_handle.fetch("counts")["value"] # counts exports
# print(new_counts)

class ScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2D Photoluminescence Scanner")
        self.my_app = MotorizedStageApp()
    
        # Set velocity parameters for the motors
        self.my_app.motor_x.set_velocity_parameters(0, 1, 0.5)
        self.my_app.motor_y.set_velocity_parameters(0, 1, 0.5)
        self.my_app.motor_z.set_velocity_parameters(0, 1, 0.5)
        
        # Add this line to define the scanning attribute
        self.scanning = False
        
        # Configure main window weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
    
        # Graph Frame
        self.graph_frame = ttk.Frame(self)
        self.graph_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
    
        # Motorized Stage App Frame
        self.motorized_stage_frame = ttk.Frame(self)
        self.motorized_stage_frame.grid(row=0, column=1, sticky="nsew")
    
        self.motorized_stage_app = MotorizedStageApp(self.motorized_stage_frame)
        self.motorized_stage_app.grid(column=0, row=0, sticky="nsew")
    
        # Control Panel Frame
        self.control_frame = ttk.Frame(self)
        self.control_frame.grid(row=1, column=1, sticky="nsew")
    
        # Graph
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
        # Control Panel
        self.create_control_panel()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)



    def on_close(self):
        # Your closing logic here
        self.destroy()

    def create_control_panel(self):
        control_frame = self.control_frame

        style = ttk.Style()
        style.configure('Large.TButton', font=("Helvetica", 12, "bold"), padding=(20, 10))

        # Create a new frame for the control panel elements
        scanning_control_frame = ttk.Frame(control_frame)
        scanning_control_frame.grid(row=1, column=1, sticky="nsew")

        ttk.Label(scanning_control_frame, text="Total Length_Y (mm)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.total_y_length = ttk.Entry(scanning_control_frame, width=10)
        self.total_y_length.insert(0, "0.1")
        self.total_y_length.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Total Length_Z (mm)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.total_z_length = ttk.Entry(scanning_control_frame, width=10)
        self.total_z_length.insert(0, "0.1")
        self.total_z_length.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Step Length_Y (mm)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.delta_y = ttk.Entry(scanning_control_frame, width=10)
        self.delta_y.insert(0, "0.001")
        self.delta_y.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Step Length_Z (mm)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.delta_z = ttk.Entry(scanning_control_frame, width=10)
        self.delta_z.insert(0, "0.001")
        self.delta_z.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Delay_Y (sec)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.delay_y = ttk.Entry(scanning_control_frame, width=10)
        self.delay_y.insert(0, "0.1")
        self.delay_y.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Delay_Z (sec)").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.delay_z = ttk.Entry(scanning_control_frame, width=10)
        self.delay_z.insert(0, "0.1")
        self.delay_z.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="File Name").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.file_name = ttk.Entry(scanning_control_frame, width=20)
        self.file_name.insert(0, "test.txt")
        self.file_name.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(scanning_control_frame, text="Integration Time (sec)").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.integration_time = ttk.Entry(scanning_control_frame, width=10)
        self.integration_time.insert(0, "0.1")
        self.integration_time.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        
        self.start_button = ttk.Button(scanning_control_frame, text="Start Scan", command=self.start_scan, style='Large.TButton')
        self.start_button.grid(row=4, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

        self.abort_button = ttk.Button(scanning_control_frame, text="Abort Scan", command=self.abort_scan, style='Large.TButton')
        self.abort_button.grid(row=4, column=2, columnspan=1, padx=10, pady=10, sticky="ew")

        self.take_measure = ttk.Button(scanning_control_frame, text="Measure", command=self.measure_one)
        self.take_measure.grid(row=4, column=3, columnspan=1, padx=10, pady=10, sticky="ew")      
        
       # Add a label for the APD signal value
        
        status_frame = ttk.Frame(control_frame)
        status_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        ttk.Label(status_frame, text="APD Signal", font=("Helvetica", 20)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.apd_signal_label = ttk.Label(status_frame, text="N/A", font=("Helvetica", 24), foreground="#0077FF", background="black", width=15)
        self.apd_signal_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        ttk.Label(status_frame, text="Status", font=("Helvetica", 20)).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.status_label = ttk.Label(status_frame, text="Idle", font=("Helvetica", 24), foreground="#0077FF", background="black", width=15)
        self.status_label.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.initialize_graph()
        # Add other text boxes and labels as needed
    
    def measure_one(self):
        with program() as counter:
            print(counts)
            counts_st = declare_stream()
            measure("readout", "SPCM", None, time_tagging.analog(times, 1000, counts))
            with stream_processing():
                counts_st.save("counts")
            print(counts)
            #self.apd_signal_label.config(text="{:.3f}".format(counts))
    
    def start_scan(self):
        
        # Start a new thread for scanning
        scanning_thread = threading.Thread(target=self.scan_loop)
        scanning_thread.start()
        self.status_label.config(text="Scanning")


    # Add this function to initialize the graph and colorbar
    
    def initialize_graph(self):
        self.ax.clear()
        self.im = self.ax.imshow(np.zeros((1, 1)), cmap='viridis', interpolation='nearest', aspect='auto', origin='lower')
        
        # Get the color limits based on the data
        data_min = 0
        data_max = 1
        self.im.set_clim(data_min, data_max)
        
        self.colorbar = self.fig.colorbar(self.im, ax=self.ax)




    def update_graph(self, data):
        data = np.array(data)
    
        # Get the unique y and z values and the number of steps
        y_values = np.unique(data[:, 0])
        z_values = np.unique(data[:, 1])
        y_steps = len(y_values)
        z_steps = len(z_values)
        
        
        
        # Create a 2D array for the heatmap data
        heatmap_data = np.zeros((z_steps, y_steps))
    
        # Replace the existing values with new values
        for d in data:
            y_idx = np.where(y_values == d[0])[0][0]
            z_idx = np.where(z_values == d[1])[0][0]
            heatmap_data[z_idx, y_idx] = d[2]
    
        # Update the heatmap data
        self.im.set_data(heatmap_data)
    
        # Get the minimum and maximum values of the heatmap data
        data_min = np.nanmin(heatmap_data)
        data_max = np.nanmax(heatmap_data)
    
        # Update the color limits of the color bar
        self.im.set_clim(data_min, data_max)
    
        # Update the color bar based on the data range
        self.update_colorbar(data_min, data_max)
    
        # Update the APD signal value
        apd_signal = data[-1, 2]
        self.apd_signal_label.config(text="{:.3f}".format(apd_signal))
    
        # Update the canvas
        self.canvas.draw_idle()
        self.update_idletasks()
    
    def update_colorbar(self, vmin, vmax):
        # Remove the existing color bar
        self.colorbar.remove()
    
        # Create new color bar with the updated range
        self.colorbar = self.fig.colorbar(self.im, ax=self.ax, boundaries=np.linspace(vmin, vmax, 256))
        self.colorbar.set_clim(vmin, vmax)
    



    def scan_loop(self):
        
        times = declare(int, size=100)
        counts = declare(int)
        total_counts = declare(int)
        n = declare(int)
        m = declare(int)
        counts_st = declare_stream()
        
        
        # Get the parameters from the control panel
        total_y_length = float(self.total_y_length.get())
        total_z_length = float(self.total_z_length.get())
        delta_y = float(self.delta_y.get())
        delta_z = float(self.delta_z.get())
        delay_y = float(self.delay_y.get())
        delay_z = float(self.delay_z.get())
        file_name = self.file_name.get()
        integration_time = float(self.integration_time.get())
        

        
        # Initialize the scanning process
        self.scanning = True
    
        # Save the initial positions
        y0, z0 = self.my_app.get_yz_position()
    
        # Calculate the number of steps
        y_steps = int(total_y_length / delta_y)
        z_steps = int(total_z_length / delta_z)
    
        # Initialize the heatmap data array
        heatmap_data = np.zeros((z_steps, y_steps))
    
        # Scan loop
        for i in range(z_steps):
            for j in range(y_steps):
                # Check if scanning process is aborted
                if not self.scanning:
                    break
    
                # Move the stage
                y = y0 + j * delta_y
                self.my_app.motor_y.move_to(y)
                

                time.sleep(delay_y)
    
                # APD signal
                #apd_signal = counts_handle.fetch("counts")["value"]
                measure("readout", "SPCM", None, time_tagging.analog(times, single_integration_time_ns, counts))
                save(counts, apd_signal)

                
                time.sleep(0.5)
                # Update the heatmap data
                y_idx = j
                z_idx = i
                heatmap_data[z_idx, y_idx] = apd_signal
    
                # Update the graph
                self.im.set_data(heatmap_data)
    
                # Update the color limits of the color bar
                data_min = np.min(heatmap_data)
                data_max = np.max(heatmap_data)
                self.im.set_clim(data_min, data_max)
    
                # Update the APD signal value
                self.apd_signal_label.config(text="{:.3f}".format(apd_signal))
    
                # Update the canvas
                self.canvas.draw_idle()
                self.update_idletasks()
    
            # Check if scanning process is aborted
            if not self.scanning:
                break
            
            z = z0 + i * delta_z            
            self.my_app.motor_z.move_to(z)
            time.sleep(delay_z)
            
        # Save the data to a file
        np.savetxt(file_name, heatmap_data)
    
        # Move the stage back to the initial position
        self.my_app.motor_y.move_to(y0)
        self.my_app.motor_z.move_to(z0)
    
        # Set scanning to False
        self.scanning = False
        self.status_label.config(text="Idle")

    
           


    def abort_scan(self):
        self.scanning = False
        self.status_label.config(text="Idle")


    def display_current_position(self):
        y, z = self.my_app.get_yz_position()
        current_position_label = ttk.Label(self.control_frame, text="Current Position: Y = {:.2f}, Z = {:.2f}".format(y, z))
        current_position_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        return current_position_label

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()


