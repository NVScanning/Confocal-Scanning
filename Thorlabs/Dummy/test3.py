import thorlabs_apt as apt
motor_x = apt.Motor(90335875)
xx = motor_x.position
print(xx)