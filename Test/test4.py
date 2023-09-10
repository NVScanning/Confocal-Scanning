import tkinter as tk
import thorlabs_apt as apt

class MotorizedStageApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Motorized Stage Simulator")
        self.x_pos = 0
        self.y_pos = 0

        self.label = tk.Label(self, text=f"X: {self.x_pos}, Y: {self.y_pos}", font=("Helvetica", 24))
        self.label.pack()

        self.entry_x = tk.Entry(self)
        self.entry_x.pack()

        self.move_x_button = tk.Button(self, text="Move X", command=self.move_x)
        self.move_x_button.pack()

        self.entry_y = tk.Entry(self)
        self.entry_y.pack()

        self.move_y_button = tk.Button(self, text="Move Y", command=self.move_y)
        self.move_y_button.pack()

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.closed = False

        self.motor_x = apt.Motor(90335875)
        self.motor_y = apt.Motor(90335876)

        self.x_pos = self.motor_x.position
        self.y_pos = self.motor_y.position

        self.periodic_position_update()

    def move_x(self):
        try:
            x_movement = round(float(self.entry_x.get()),5)
            self.x_pos = round(float(self.x_pos) + x_movement,5)
            self.motor_x.move_by(x_movement)
        except ValueError:
            pass

    def move_y(self):
        try:
            y_movement = round(float(self.entry_y.get()),5)
            self.y_pos = round(float(self.y_pos) + y_movement,5)
            self.motor_y.move_by(y_movement)
        except ValueError:
            pass

    def on_close(self):
        self.closed = True
        self.destroy()

    def periodic_position_update(self):
        if not self.closed:
            self.label.config(text=f"X: {self.x_pos}, Y: {self.y_pos}")
            self.after(100, self.periodic_position_update)

if __name__ == "__main__":
    app = MotorizedStageApp()
    app.mainloop()
