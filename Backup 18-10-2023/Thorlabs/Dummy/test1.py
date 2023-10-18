import thorlabs_apt as apt
import tkinter as tk

class PositionMonitor:
    def __init__(self, motor):
        self.motor = motor
        
        # create a new Tkinter window
        self.window = tk.Tk()
        
        # create a label to display the current motor position
        self.position_label = tk.Label(self.window, text="Position: ")
        self.position_label.pack()
        
        # create a button to update the motor position
        self.update_button = tk.Button(self.window, text="Update", command=self.update_position)
        self.update_button.pack()
        
        # start the main event loop
        self.window.mainloop()
    
    def update_position(self):
        # get the current motor position
        position = self.motor.position
        
        # update the position label
        self.position_label.config(text="Position: {:.3f}".format(position))

if __name__ == "__main__":
    # create a new motor object
    motor_x = apt.Motor(90335875)
    
    # create a new position monitor object
    monitor = PositionMonitor(motor_x)
