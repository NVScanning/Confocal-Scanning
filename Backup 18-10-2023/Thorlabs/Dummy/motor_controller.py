import tkinter as tk
import thorlabs_apt as apt
import time

# Initialize motors
apt.list_available_devices()
motor_x = apt.Motor(90335875)
motor_y = apt.Motor(90335876)
motor_z = apt.Motor(90335877)


def update_positions():
    x_pos = motor_x.position
    y_pos = motor_y.position
    z_pos = motor_z.position

    x_label.config(text=f'X position: {x_pos}')
    y_label.config(text=f'Y position: {y_pos}')
    z_label.config(text=f'Z position: {z_pos}')

    root.after(100, update_positions)  # Refresh positions every 100 milliseconds

# Create the tkinter window
root = tk.Tk()
root.title('Motor Positions')

x_label = tk.Label(root, text='', font=('Arial', 14))
x_label.pack(pady=10)

y_label = tk.Label(root, text='', font=('Arial', 14))
y_label.pack(pady=10)

z_label = tk.Label(root, text='', font=('Arial', 14))
z_label.pack(pady=10)

update_positions()  # Start updating positions

root.mainloop()  # Run the tkinter main loop
