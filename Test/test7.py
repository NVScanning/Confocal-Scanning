import tkinter as tk
import thorlabs_apt as apt
import threading

class MotorizedStageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motorized Stage Simulator")

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
        self.label.pack()

        self.entry_x = tk.Entry(self)
        self.entry_x.pack()

        self.move_x_button = tk.Button(self, text="Move X", command=self.move_x)
        self.move_x_button.pack()

        self.home_x_button = tk.Button(self, text="Home X", command=self.home_x)
        self.home_x_button.pack()

        self.entry_y = tk.Entry(self)
        self.entry_y.pack()

        self.move_y_button = tk.Button(self, text="Move Y", command=self.move_y)
        self.move_y_button.pack()

        self.home_y_button = tk.Button(self, text="Home Y", command=self.home_y)
        self.home_y_button.pack()
        
        self.entry_z = tk.Entry(self)
        self.entry_z.pack()

        self.move_z_button = tk.Button(self, text="Move Z", command=self.move_z)
        self.move_z_button.pack()

        self.home_z_button = tk.Button(self, text="Home Z", command=self.home_z)
        self.home_z_button.pack()
        
        

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False

        self.periodic_position_update()

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
        self.motor_x.poll_until_idle()
        self.x_pos = self.motor_x.position

    def home_y(self):
        threading.Thread(target=self.home_y_thread).start()

    def home_y_thread(self):
        self.motor_y.move_home(True)
        self.motor_y.poll_until_idle()
        self.y_pos = self.motor_y.position
        
    def home_z(self):
        threading.Thread(target=self.home_z_thread).start()

    def home_z_thread(self):
        self.motor_z.move_home(True)
        self.motor_z.poll_until_idle()
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
