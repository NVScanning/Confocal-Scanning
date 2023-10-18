# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:22:22 2023

@author: nvcryo
"""

import thorlabs_apt as apt
import time

# Define motor IDs
motor_ids = [90335875, 90335876, 90335877]

# Initialize motors
motors = [apt.Motor(motor_id) for motor_id in motor_ids]

# Print current positions in a loop
while True:
    positions = [motor.position for motor in motors]
    print("Current positions:", positions)
    time.sleep(0.1)  # wait 0.1 seconds before checking again
