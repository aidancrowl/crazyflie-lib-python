# This program implements a path-planning algorithm based on the acceleration equation 
# used to model a desired trajectory for the Crazyflie.

import scipy.integrate as integrate
#test comment for Bryan
pos_init = []
vel_init = []
pos_final = []
vel_final = []
time = 0

def get_inputs(): # pos_init, vel_init, pos_final, vel_final, time):
        
    pos_x_init = int(input('Enter initial x position: '))
    pos_init.append(pos_x_init)
    pos_y_init = int(input('Enter initial y position: '))
    pos_init.append(pos_y_init)
    pos_z_init = int(input('Enter initial z position: '))
    pos_init.append(pos_z_init)
    print

    vel_x_init = int(input('Enter initial x velocity: '))
    vel_init.append(vel_x_init)
    vel_y_init = int(input('Enter initial y velocity: '))
    vel_init.append(vel_y_init)
    vel_z_init = int(input('Enter initial z velocity: '))
    vel_init.append(vel_z_init)
    print

    pos_x_final = int(input('Enter final x position: '))
    pos_final.append(pos_x_final)
    pos_y_final = int(input('Enter final y position: '))
    pos_final.append(pos_y_final)
    pos_z_final = int(input('Enter final z position: '))
    pos_final.append(pos_z_final)
    print

    vel_x_final = int(input('Enter final x velocity: '))
    vel_final.append(vel_x_final)
    vel_y_final = int(input('Enter final y velocity: '))
    vel_final.append(vel_y_final)
    vel_z_final = int(input('Enter final z velocity: '))
    vel_final.append(vel_z_final)
    print

    time = int(input('Enter time to fly path (sec): '))
    print

def print_inputs(): # pos_init, vel_init, pos_final, vel_final, time):

    print(pos_init)
    print(vel_init)
    print(pos_final)
    print(vel_final)
    print(time)


if __name__ == '__main__':
    get_inputs() # pos_init, vel_init, pos_final, vel_final, time)
    print_inputs() # pos_init, vel_init, pos_final, vel_final, time)
