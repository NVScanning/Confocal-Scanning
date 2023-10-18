import random
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def generate_fake_data():
    return random.randint(0, 100)

def update(frame):
    x.append(frame)
    y.append(generate_fake_data())  # Replace this with the actual data acquisition function
    line.set_data(x, y)
    ax.relim()
    ax.autoscale_view()
    return line,

time_interval = 0.1  # Update plot every 1 second
time_duration = 30  # Duration of the plot in seconds

x = []
y = []

fig, ax = plt.subplots()
line, = ax.plot(x, y, linestyle='-', marker='o')
ax.set_ylim(0, 200)  # Set y-axis limits according to the expected range of photon counts
ax.set_xlim(0, time_duration)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Photocounting Rate')

ani = FuncAnimation(fig, update, frames=range(time_duration), interval=time_interval * 1000, blit=True, repeat=False)
plt.show()
