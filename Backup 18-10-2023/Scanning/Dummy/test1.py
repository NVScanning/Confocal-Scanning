import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
import threading

class MotorizedStage:
    def __init__(self):
        self.y_pos = 0
        self.z_pos = 0

    def get_y_position(self):
        return self.y_pos

    def get_z_position(self):
        return self.z_pos

    def move_y(self, delta_y):
        self.y_pos += delta_y

    def move_z(self, delta_z):
        self.z_pos += delta_z

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2D Scanning Experiment")
        self.geometry("800x600")

        self.motorized_stage = MotorizedStage()

        self.create_widgets()
        self.scan_thread = None
        self.abort_scan_flag = False

    def create_widgets(self):
        # Real-time mapping graph
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().place(x=0, y=0, relwidth=0.6, relheight=0.6)

        # Motorized stage panel
        motorized_stage_frame = ttk.LabelFrame(self, text="Motorized Stage")
        motorized_stage_frame.place(x=480, y=0, relwidth=0.5, relheight=0.6)

        # Control panel
        control_frame = ttk.LabelFrame(self, text="Control Panel")
        control_frame.place(x=0, y=360, relwidth=1, relheight=0.4)

        # Current y, z positions
        ttk.Label(control_frame, text="Current y:").grid(column=0, row=0)
        self.y_position_var = tk.StringVar()
        ttk.Label(control_frame, textvariable=self.y_position_var).grid(column=1, row=0)

        ttk.Label(control_frame, text="Current z:").grid(column=0, row=1)
        self.z_position_var = tk.StringVar()
        ttk.Label(control_frame, textvariable=self.z_position_var).grid(column=1, row=1)

        # Current signal and averaged signal
        ttk.Label(control_frame, text="Current Signal:").grid(column=0, row=2)
        self.current_signal_var = tk.StringVar()
        ttk.Label(control_frame, textvariable=self.current_signal_var).grid(column=1, row=2)

        ttk.Label(control_frame, text="Averaged Signal:").grid(column=0, row=3)
        self.averaged_signal_var = tk.StringVar()
        ttk.Label(control_frame, textvariable=self.averaged_signal_var).grid(column=1, row=3)

        # Total average time
        ttk.Label(control_frame, text="Total Average Time:").grid(column=0, row=4)
        self.total_average_time_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.total_average_time_var).grid(column=1, row=4)

        # Total lengths of y, z
        ttk.Label(control_frame, text="Total Length of y:").grid(column=2, row=0)
        self.total_y_length_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.total_y_length_var).grid(column=3, row=0)

        ttk.Label(control_frame, text="Total Length of z:").grid(column=2, row=1)
        self.total_z_length_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.total_z_length_var).grid(column=3, row=1)

        # Step lengths of y, z
        ttk.Label(control_frame, text="Step Length of y:").grid(column=2, row=2)
        self.step_y_length_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.step_y_length_var).grid(column=3, row=2)

        ttk.Label(control_frame, text="Step Length of z:").grid(column=2, row=3)
        self.step_z_length_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.step_z_length_var).grid(column=3, row=3)

        # File name
        ttk.Label(control_frame, text="File Name:").grid(column=2, row=4)
        self.file_name_var = tk.StringVar()
        ttk.Entry(control_frame, textvariable=self.file_name_var).grid(column=3, row=4)

        # Scan start and abort buttons
        ttk.Button(control_frame, text="Start Scan", command=self.start_scan).grid(column=4, row=0)
        ttk.Button(control_frame, text="Abort Scan", command=self.abort_scan).grid(column=4, row=1)

    def start_scan(self):
        if self.scan_thread and self.scan_thread.is_alive():
            return

        self.abort_scan_flag = False
        self.scan_thread = threading.Thread(target=self.scan)
        self.scan_thread.start()

    def abort_scan(self):
        self.abort_scan_flag = True
        if self.scan_thread:
            self.scan_thread.join()

    def scan(self):
        # Initialize parameters
        y0, z0 = self.motorized_stage.get_current_position()
        y_f = float(self.total_y_length_var.get())
        z_f = float(self.total_z_length_var.get())
        delta_y = float(self.step_y_length_var.get())
        delta_z = float(self.step_z_length_var.get())
        delay_y = float(self.delay_y_var.get())
        delay_z = float(self.delay_z_var.get())
        ave_time = float(self.ave_time_var.get())
        file_name = self.file_name_var.get()

        # Create file for saving data
        with open(file_name, 'w') as f:
            f.write("y_position\tz_position\tAPD_number\n")

            z_position = z0
            while z_position <= z0 + z_f:
                y_position = y0
                while y_position <= y0 + y_f:
                    if self.abort_scan_flag:
                        break

                    # Move motorized stage to the current position
                    self.motorized_stage.move_to(y_position, z_position)

                    # Get APD signal
                    apd_signal = self.get_apd_signal(ave_time)

                    # Update displayed information
                    self.current_y_position_var.set(y_position)
                    self.current_z_position_var.set(z_position)
                    self.current_signal_var.set(apd_signal)

                    # Save data to the file
                    f.write(f"{y_position}\t{z_position}\t{apd_signal}\n")

                    # Update the real-time 2D map graph
                    self.update_graph(y_position, z_position, apd_signal)

                    # Move to the next position in the y direction
                    y_position += delta_y
                    time.sleep(delay_y)

                if self.abort_scan_flag:
                    break

                # Move to the next position in the z direction
                z_position += delta_z
                time.sleep(delay_z)

        # Move back to the original position
        self.motorized_stage.move_to(y0, z0)

    def get_apd_signal(self, ave_time):
        # Replace this function with the actual APD signal reading process
        # For now, we use a random signal generator for simulation
        time.sleep(ave_time)
        return random.random()

if __name__ == "__main__":
    app = App()
    app.mainloop()

