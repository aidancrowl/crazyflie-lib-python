# This program implements a path-planning algorithm based on the acceleration equation 
# used to model a desired trajectory for the Crazyflie.

import scipy.integrate as integrate
# import array as arr
import numpy as np

# r_o = []
# v_o = []
# r_f = []
# v_f = []
# t_o = 0
# t_f = 0

class PathPlanner:

    def __init__(self, r_o, v_o, r_f, v_f, t_o, t_f):
        self.r_o = r_o
        self.v_o = v_o
        self.r_f = r_f
        self.v_f = v_f
        self.t_o = t_o
        self.t_f = t_f

    def get_inputs(self):
        
        r_x_o = int(input('Enter initial x position: '))
        # self.r_o.append(r_x_o)
        # np.append(self.r_o, r_x_o)
        self.r_o[0] = r_x_o
        r_y_o = int(input('Enter initial y position: '))
        # self.r_o.append(r_y_o)
        # np.append(self.r_o, r_y_o)
        self.r_o[1] = r_y_o
        r_z_o = int(input('Enter initial z position: '))
        # self.r_o.append(r_z_o)
        # np.append(self.r_o, r_z_o)
        self.r_o[2] = r_z_o
        print

        v_x_o = int(input('Enter initial x velocity: '))
        # self.v_o.append(v_x_o)
        # np.append(self.v_o, v_x_o)
        self.v_o[0] = v_x_o
        v_y_o = int(input('Enter initial y velocity: '))
        # self.v_o.append(v_y_o)
        # np.append(self.v_o, v_y_o)
        self.v_o[1] = v_y_o
        v_z_o = int(input('Enter initial z velocity: '))
        # self.v_o.append(v_z_o)
        # np.append(self.v_o, v_z_o)
        self.v_o[2] = v_z_o
        print

        r_x_f = int(input('Enter final x position: '))
        # self.r_f.append(r_x_f)
        # np.append(self.r_f, r_x_f)
        self.r_f[0] = r_x_f
        r_y_f = int(input('Enter final y position: '))
        # self.r_f.append(r_y_f)
        # np.append(self.r_f, r_y_f)
        self.r_f[1] = r_y_f
        r_z_f = int(input('Enter final z position: '))
        # self.r_f.append(r_z_f)
        # np.append(self.r_f, r_z_f)
        self.r_f[2] = r_z_f
        print

        v_x_f = int(input('Enter final x velocity: '))
        # self.v_f.append(v_x_f)
        # np.append(self.v_f, v_x_f)
        self.v_f[0] = v_x_f
        v_y_f = int(input('Enter final y velocity: '))
        # self.v_f.append(v_y_f)
        # np.append(self.v_f, v_y_f)
        self.v_f[1] = v_y_f
        v_z_f = int(input('Enter final z velocity: '))
        # self.v_f.append(v_z_f)
        # np.append(self.v_f, v_z_f)
        self.v_f[2] = v_z_f
        print

        self.t_f = int(input('Enter time to fly path (sec): '))
        print(self.t_f)
        print

    def print_inputs(self):

        print(self.r_o)
        print(self.v_o)
        print(self.r_f)
        print(self.v_f)
        print(self.t_o)
        print(self.t_f)

    def find_trajectory(self, t):

        vel_t = self.v_o + ((6*self.r_o - 6*self.r_f + 6*self.v_f*(self.t_f - self.t_o))/(self.t_f - self.t_o)**3 - (3*self.v_f - 3*self.v_o)/(self.t_f - self.t_o)**2)*t**2 + (((4*self.t_f + 2*self.t_o)*(self.v_f - self.v_o))/(self.t_f - self.t_o)**2 - ((6*self.t_f + 6*self.t_o)*(self.r_o - self.r_f + self.v_f*(self.t_f - self.t_o)))/(self.t_f - self.t_o)**3)*t
        
        print(vel_t)


if __name__ == '__main__':

    pp = PathPlanner(np.zeros(3, dtype=int),np.zeros(3, dtype=int),np.zeros(3, dtype=int),np.zeros(3, dtype=int),0,0)

    pp.get_inputs() 
    pp.print_inputs()
    pp.find_trajectory(5)

