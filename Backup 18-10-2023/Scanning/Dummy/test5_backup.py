import tkinter as tk
from tkinter import ttk
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from motorized_stage import MotorizedStageApp
import threading


class ScannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2D Photoluminescence Scanner")
        self.my_app = MotorizedStageApp()
    
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

        # Create a new frame for the control panel elements
        scanning_control_frame = ttk.Frame(control_frame)
        scanning_control_frame.grid(row=1, column=4, sticky="nsew")

        ttk.Label(scanning_control_frame, text="Total Length (Y)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.total_y_length = ttk.Entry(scanning_control_frame, width=10)
        self.total_y_length.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Total Length (Z)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.total_z_length = ttk.Entry(scanning_control_frame, width=10)
        self.total_z_length.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Step Length (Y)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.delta_y = ttk.Entry(scanning_control_frame, width=10)
        self.delta_y.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Step Length (Z)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.delta_z = ttk.Entry(scanning_control_frame, width=10)
        self.delta_z.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Delay (Y)").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.delay_y = ttk.Entry(scanning_control_frame, width=10)
        self.delay_y.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(scanning_control_frame, text="Delay (Z)").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.delay_z = ttk.Entry(scanning_control_frame, width=10)
        self.delay_z.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        self.start_button = ttk.Button(scanning_control_frame, text="Start Scan", command=self.start_scan)
        self.start_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.abort_button = ttk.Button(scanning_control_frame, text="Abort Scan", command=self.abort_scan)
        self.abort_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        ttk.Label(scanning_control_frame, text="File Name").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.file_name = ttk.Entry(scanning_control_frame, width=20)
        self.file_name.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        
        # Add a label for the APD signal value
        self.apd_signal_label = ttk.Label(self.control_frame, text="APD Signal: N/A", foreground="#0077FF", background="black")
        self.apd_signal_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.initialize_graph()
        # Add other text boxes and labels as needed
    
    def start_scan(self):
        
        # Start a new thread for scanning
        scanning_thread = threading.Thread(target=self.scan_loop)
        scanning_thread.start()

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
    
        # Fill the heatmap data array
        for d in data:
            y_idx = np.where(y_values == d[0])[0][0]
            z_idx = np.where(z_values == d[1])[0][0]
            heatmap_data[z_idx, y_idx] = d[2]
    
        # Update the heatmap data
        self.im.set_data(heatmap_data)
            
        # Get the minimum and maximum values of the heatmap data
        data_min = np.min(heatmap_data)
        data_max = np.max(heatmap_data)
            
        # Update the color limits of the color bar
        self.im.set_clim(data_min, data_max)
            
        # Update the APD signal value
        apd_signal = data[-1, 2]
        self.apd_signal_label.config(text="APD Signal: {:.3f}".format(apd_signal))
            
        # Update the canvas
        self.canvas.draw_idle()
        self.update_idletasks()

    
        # Update the APD signal value
        apd_signal = data[-1, 2]
        self.apd_signal_label.config(text="APD Signal: {:.3f}".format(apd_signal))
    
        # Update the canvas
        self.canvas.draw_idle()
        self.update_idletasks()






    def scan_loop(self):
        # Get the parameters from the control panel
        total_y_length = float(self.total_y_length.get())
        total_z_length = float(self.total_z_length.get())
        delta_y = float(self.delta_y.get())
        delta_z = float(self.delta_z.get())
        delay_y = float(self.delay_y.get())
        delay_z = float(self.delay_z.get())
        file_name = self.file_name.get()
    
        # Initialize the scanning process
        self.scanning = True
    
        # Save the initial positions
        y0, z0 = self.my_app.get_yz_position()
    
        # Calculate the number of steps
        y_steps = int(total_y_length / delta_y)
        z_steps = int(total_z_length / delta_z)
    
        # Initialize the data array
        data = []
    
        # Scan loop
        for i in range(z_steps):
            for j in range(y_steps):
                # Check if scanning process is aborted
                if not self.scanning:
                    break
    
                # Move the stage
                y = y0 + j * delta_y
                z = z0 + i * delta_z
                self.my_app.motor_y.move_to(y)
                self.my_app.motor_z.move_to(z)
    
                time.sleep(delay_y)
    
                # Simulate the APD signal
                apd_signal = np.random.random()
    
                # Append the data
                data.append([y, z, apd_signal])
    
                # Update the graph
                self.update_graph(data)
    
            # Check if scanning process is aborted
            if not self.scanning:
                break
    
            time.sleep(delay_z)
    
        # Save the data to a file
        np.savetxt(file_name, data)
    
        # Move the stage back to the initial position
        self.my_app.motor_y.move_to(y0)
        self.my_app.motor_z.move_to(z0)
    
        # Set scanning to False
        self.scanning = False
       


    def abort_scan(self):
        self.scanning = False

    def display_current_position(self):
        y, z = self.my_app.get_yz_position()
        current_position_label = ttk.Label(self.control_frame, text="Current Position: Y = {:.2f}, Z = {:.2f}".format(y, z))
        current_position_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        return current_position_label

if __name__ == "__main__":
    app = ScannerApp()
    app.mainloop()


