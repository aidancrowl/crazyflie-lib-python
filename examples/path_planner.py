# This program implements a path-planning algorithm based on the acceleration equation 
# used to model a desired trajectory for the Crazyflie.

import scipy.integrate as integrate

r_o = []
v_o = []
r_f = []
v_f = []
t_o = 0
t_f = 0

def get_inputs(r_o, v_o, r_f, v_f, t_o, t_f): # pos_init, vel_init, pos_final, vel_final, time):
        
    r_x_o = int(input('Enter initial x position: '))
    r_o.append(r_x_o)
    r_y_o = int(input('Enter initial y position: '))
    r_o.append(r_y_o)
    r_z_o = int(input('Enter initial z position: '))
    r_o.append(r_z_o)
    print

    v_x_o = int(input('Enter initial x velocity: '))
    v_o.append(v_x_o)
    v_y_o = int(input('Enter initial y velocity: '))
    v_o.append(v_y_o)
    v_z_o = int(input('Enter initial z velocity: '))
    v_o.append(v_z_o)
    print

    r_x_f = int(input('Enter final x position: '))
    r_f.append(r_x_f)
    r_y_f = int(input('Enter final y position: '))
    r_f.append(r_y_f)
    r_z_f = int(input('Enter final z position: '))
    r_f.append(r_z_f)
    print

    v_x_f = int(input('Enter final x velocity: '))
    v_f.append(v_x_f)
    v_y_f = int(input('Enter final y velocity: '))
    v_f.append(v_y_f)
    v_z_f = int(input('Enter final z velocity: '))
    v_f.append(v_z_f)
    print

    t_f = int(input('Enter time to fly path (sec): '))
    print

def print_inputs(r_o, v_o, r_f, v_f, t_o, t_f): # pos_init, vel_init, pos_final, vel_final, time):

    print(r_o)
    print(v_o)
    print(r_f)
    print(v_f)
    print(t_o)
    print(t_f)

def find_trajectory(r_o, v_o, r_f, v_f, t_o, t_f):

    vel_t = vel_init + ((6*r_o - 6*r_f + 6*v_f*(t_f - t_o))/(t_f - t_o)^3 - (3*v_f - 3*v_o)/(t_f - t_o)^2)*t^2 + (((4*t_f + 2*t_o)*(v_f - v_o))/(t_f - t_o)^2 - ((6*t_f + 6*t_o)*(r_o - r_f + v_f*(t_f - t_o)))/(t_f - t_o)^3)*t



if __name__ == '__main__':
    get_inputs(r_o, v_o, r_f, v_f, t_o, t_f) # pos_init, vel_init, pos_final, vel_final, time)
    print_inputs(r_o, v_o, r_f, v_f, t_o, t_f) # pos_init, vel_init, pos_final, vel_final, time)
#big dick adian
