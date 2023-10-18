    import thorlabs_apt as apt
    apt.list_available_devices()
    motor_x = apt.Motor(90335875)
    motor_y = apt.Motor(90335876)
    motor_z = apt.Motor(90335877)
    
    motor_x.move_home(True)
    motor_y.move_home(True)
    motor_z.move_home(True)
    
    motor_x.get_velocity_parameters
    
    motor_x.position
    motor_x.move_by(0.5)
