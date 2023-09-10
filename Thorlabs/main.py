from motorized_stage import MotorizedStageApp
import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main App")

        # Create an instance of MotorizedStageApp
        self.motorized_stage_app = MotorizedStageApp()

        # Create a button to update the label with the current position of the motors
        self.update_button = tk.Button(self, text="Update Position", command=self.update_position_label)
        self.update_button.grid(row=0, column=0, padx=10, pady=10)

        # Create a label to display the current position of the motors
        self.position_label = tk.Label(self, text="Position: ", font=("Helvetica", 16))
        self.position_label.grid(row=1, column=0, padx=10, pady=10)

    def update_position_label(self):
        x_pos = self.motorized_stage_app.x_pos
        y_pos = self.motorized_stage_app.y_pos
        z_pos = self.motorized_stage_app.z_pos
        self.position_label.config(text=f"Position: X: {x_pos:.5f}, Y: {y_pos:.5f}, Z: {z_pos:.5f}")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = MainApp()
    app.run()
