import tkinter as tk
import thorlabs_apt as apt
import threading
import time

class MotorizedStageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Initialization of the motors
        self.title("Motorized Stage Controll")

        self.motor_x = apt.Motor(90335875)
        self.motor_y = apt.Motor(90335876)
        self.motor_z = apt.Motor(90335877)

        self.motor_x.set_velocity_parameters(0, 1, 0.5)
        self.motor_y.set_velocity_parameters(0, 1, 0.5)
        self.motor_z.set_velocity_parameters(0, 1, 0.5)

        self.x_pos = self.motor_x.position
        self.y_pos = self.motor_y.position
        self.z_pos = self.motor_z.position
        
        self.label = tk.Label(self, text=f"X: {self.x_pos}, Y: {self.y_pos},  Z: {self.z_pos}", font=("Helvetica", 24))
        self.label.grid(row=0, column=0, columnspan=3)
        
        # Set a minimum window size
        self.minsize(800, 400)

        # Create a font for the Entry widgets
        entry_font = ("Helvetica", 18)

        # X-axis frame
        x_frame = tk.Frame(self)
        x_frame.grid(row=1, column=0, padx=20, pady=10)

        self.entry_x = tk.Entry(x_frame, font=entry_font, fg="green", bg="black", justify="right")
        self.entry_x.insert(0, f"{self.x_pos:0.5f}")
        self.entry_x.grid(row=0, column=0)

        self.move_x_button = tk.Button(x_frame, text="Move X", command=self.move_x)
        self.move_x_button.grid(row=0, column=1)

        self.home_x_button = tk.Button(x_frame, text="Home X", command=self.home_x)
        self.home_x_button.grid(row=2, column=0)        

        # Y-axis frame
        y_frame = tk.Frame(self)
        y_frame.grid(row=1, column=1, padx=20, pady=10)

        self.entry_y = tk.Entry(y_frame, font=entry_font, fg="green", bg="black", justify="right")
        self.entry_y.insert(0, f"{self.y_pos:0.5f}")
        self.entry_y.grid(row=0, column=0)

        self.move_y_button = tk.Button(y_frame, text="Move Y", command=self.move_y)
        self.move_y_button.grid(row=0, column=1)

        self.home_y_button = tk.Button(y_frame, text="Home Y", command=self.home_y)
        self.home_y_button.grid(row=2, column=0)

        # Z-axis frame
        z_frame = tk.Frame(self)
        z_frame.grid(row=1, column=2, padx=20, pady=10)

        self.entry_z = tk.Entry(z_frame, font=entry_font, fg="blue", bg="black", justify="right")
        self.entry_z.insert(0, f"{self.z_pos:0.5f}")
        self.entry_z.grid(row=0, column=0)

        self.move_z_button = tk.Button(z_frame, text="Move Z", command=self.move_z)
        self.move_z_button.grid(row=0, column=1)

        self.home_z_button = tk.Button(z_frame, text="Home Z", command=self.home_z)
        self.home_z_button.grid(row=2, column=0)

        # Up and Down buttons
        # X-axis
        self.up_button_x = tk.Button(x_frame, text="X Up")
        self.up_button_x.grid(row=1, column=0)
        self.up_button_x.bind("<ButtonPress>", self.move_x_up_press)
        self.up_button_x.bind("<ButtonRelease>", self.move_x_up_release)

        self.down_button_x = tk.Button(x_frame, text="X Down")
        self.down_button_x.grid(row=1, column=1)
        self.down_button_x.bind("<ButtonPress>", self.move_x_down_press)
        self.down_button_x.bind("<ButtonRelease>", self.move_x_down_release)
        # Y-axis        
        self.up_button_y = tk.Button(y_frame, text="Y Up")
        self.up_button_y.grid(row=1, column=0)
        self.up_button_y.bind("<ButtonPress>", self.move_y_up_press)
        self.up_button_y.bind("<ButtonRelease>", self.move_y_up_release)

        self.down_button_y = tk.Button(y_frame, text="Y Down")
        self.down_button_y.grid(row=1, column=1)
        self.down_button_y.bind("<ButtonPress>", self.move_y_down_press)
        self.down_button_y.bind("<ButtonRelease>", self.move_y_down_release)
        # Z-axis        
        self.up_button_z = tk.Button(z_frame, text="Z Up")
        self.up_button_z.grid(row=1, column=0)
        self.up_button_z.bind("<ButtonPress>", self.move_z_up_press)
        self.up_button_z.bind("<ButtonRelease>", self.move_z_up_release)

        self.down_button_z = tk.Button(z_frame, text="Z Down")
        self.down_button_z.grid(row=1, column=1)
        self.down_button_z.bind("<ButtonPress>", self.move_z_down_press)
        self.down_button_z.bind("<ButtonRelease>", self.move_z_down_release)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False

        self.periodic_position_update()

    def move_x_to(self):
        try:
            x_target = round(float(self.entry_x_to.get()), 5)
            self.motor_x.move_to(x_target)
        except ValueError:
            pass

    def move_y_to(self):
        try:
            y_target = round(float(self.entry_y_to.get()), 5)
            self.motor_y.move_to(y_target)
        except ValueError:
            pass

    def move_z_to(self):
        try:
            z_target = round(float(self.entry_z_to.get()), 5)
            self.motor_z.move_to(z_target)
        except ValueError:
            pass

    # X-button actions
    def move_x_up_press(self, event):
        self.move_x_up_active = True
        threading.Thread(target=self.move_x_up_continuous).start()

    def move_x_up_release(self, event):
        self.move_x_up_active = False

    def move_x_down_press(self, event):
        self.move_x_down_active = True
        threading.Thread(target=self.move_x_down_continuous).start()

    def move_x_down_release(self, event):
        self.move_x_down_active = False

    def move_x_up_continuous(self):
        while self.move_x_up_active:
            self.motor_x.move_by(0.001)
            time.sleep(0.1)
            while self.motor_x.is_in_motion:
                time.sleep(0.1)

    def move_x_down_continuous(self):
        while self.move_x_down_active:
            self.motor_x.move_by(-0.001)
            time.sleep(0.1)
            while self.motor_x.is_in_motion:
                time.sleep(0.1)
                
    # Y-button actions
    def move_y_up_press(self, event):
        self.move_y_up_active = True
        threading.Thread(target=self.move_y_up_continuous).start()

    def move_y_up_release(self, event):
        self.move_y_up_active = False

    def move_y_down_press(self, event):
        self.move_y_down_active = True
        threading.Thread(target=self.move_y_down_continuous).start()

    def move_y_down_release(self, event):
        self.move_y_down_active = False

    def move_y_up_continuous(self):
        while self.move_y_up_active:
            self.motor_y.move_by(0.001)
            time.sleep(0.1)
            while self.motor_y.is_in_motion:
                time.sleep(0.1)

    def move_y_down_continuous(self):
        while self.move_y_down_active:
            self.motor_y.move_by(-0.001)
            time.sleep(0.1)
            while self.motor_y.is_in_motion:
                time.sleep(0.1)                

    # Z-button actions
    def move_z_up_press(self, event):
        self.move_z_up_active = True
        threading.Thread(target=self.move_z_up_continuous).start()

    def move_z_up_release(self, event):
        self.move_z_up_active = False

    def move_z_down_press(self, event):
        self.move_z_down_active = True
        threading.Thread(target=self.move_z_down_continuous).start()

    def move_z_down_release(self, event):
        self.move_z_down_active = False

    def move_z_up_continuous(self):
        while self.move_z_up_active:
            self.motor_z.move_by(0.001)
            time.sleep(0.1)
            while self.motor_z.is_in_motion:
                time.sleep(0.1)

    def move_z_down_continuous(self):
        while self.move_z_down_active:
            self.motor_z.move_by(-0.001)
            time.sleep(0.1)
            while self.motor_z.is_in_motion:
                time.sleep(0.1)

    def move_x(self):
        try:
            x_movement = round(float(self.entry_x.get()),5)
            self.motor_x.move_by(x_movement)
        except ValueError:
            pass

    def move_y(self):
        try:
            y_movement = round(float(self.entry_y.get()),5)
            self.motor_y.move_by(y_movement)
        except ValueError:
            pass

    def move_z(self):
        try:
            z_movement = round(float(self.entry_z.get()),5)
            self.motor_z.move_by(z_movement)
        except ValueError:
            pass

    def home_x(self):
        threading.Thread(target=self.home_x_thread).start()

    def home_x_thread(self):
        self.motor_x.move_home(True)
        self.x_pos = self.motor_x.position

    def home_y(self):
        threading.Thread(target=self.home_y_thread).start()

    def home_y_thread(self):
        self.motor_y.move_home(True)
        self.y_pos = self.motor_y.position
        
    def home_z(self):
        threading.Thread(target=self.home_z_thread).start()

    def home_z_thread(self):
        self.motor_z.move_home(True)
        self.z_pos = self.motor_z.position
        
        
    def on_close(self):
        self.closed = True
        self.destroy()

    def periodic_position_update(self):
        if not self.closed:
            self.x_pos = round(self.motor_x.position,5)
            self.y_pos = round(self.motor_y.position,5)
            self.z_pos = round(self.motor_z.position,5)
            self.label.config(text=f"X: {self.x_pos}, Y: {self.y_pos}, Z: {self.z_pos}")
            self.after(100, self.periodic_position_update)

if __name__ == "__main__":
    app = MotorizedStageApp()
    app.mainloop()
