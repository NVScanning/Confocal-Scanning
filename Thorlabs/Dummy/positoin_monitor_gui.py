import thorlabs_apt as apt
import tkinter as tk

# Define motor IDs
motor_ids = [90335875, 90335876, 90335877]

# Initialize motors
motors = [apt.Motor(motor_id) for motor_id in motor_ids]

class PositionMonitor:
    def __init__(self, motors):
        self.motors = motors

        # create a new Tkinter window
        self.window = tk.Tk()
        self.window.title("Motor Positions")

        # create a label to display the current motor positions
        self.position_label = tk.Label(self.window, text="Current Positions:")
        self.position_label.pack()

        # create a label for each motor position
        self.position_labels = []
        for i in range(len(self.motors)):
            label = tk.Label(self.window, text="Motor {}: {:.3f}".format(i+1, self.motors[i].position))
            label.pack()
            self.position_labels.append(label)

        # start the main event loop
        self.update_positions()

    def update_positions(self):
        # update the position labels with the current positions
        for i in range(len(self.motors)):
            self.position_labels[i].config(text="Motor {}: {:.3f}".format(i+1, self.motors[i].position))

        # call this method again after a short delay
        self.window.after(100, self.update_positions)

if __name__ == "__main__":
    # create a new position monitor object
    monitor = PositionMonitor(motors)

    # start the main event loop for the GUI
    monitor.window.mainloop()
