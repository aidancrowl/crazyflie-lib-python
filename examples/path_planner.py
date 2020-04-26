# File: path_planner.py

# Authors: Aidan Crowl, Luke Harrison, Alexis Lanier, Bryan Long, Donovan Booker

# Description: This program defines and implements a PathPlanner class that uses the acceleration equation to model a desired trajectory for the
# Crazyflie. Parameters for the equation are input at the command line and the equation generates a series of velocity setpoints that are sent
# to the Crazyflie using the MotionCommander class. This set of velocities models the trajectory determined by the equation. It was written as
# part of the 2019-20 Ohio University EE Capstone UAV FMS project.

# Last Modified: April 23, 2020

import scipy.integrate as integrate
import sys
import time
import numpy as np
import struct
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

URI = 'radio://0/80/2M' # The Crazyradio address, used to pair the dongle and the Crazyflie

class PathPlanner:

    # Function: __init__
    # Parameters: 
    #   - self: PathPlanner object (represents the instance of the class that called function)​
    #   - r_o: Initial position vector (m) - [r_o_x r_o_y r_o_z]
    #   - v_o: Initial velocity vector (m/s) - [v_o_x v_o_y v_o_z]
    #   - r_f: Final position vector (m) - [r_f_x r_f_y r_f_z]
    #   - v_f: Final velocity vector (m/s) - [v_f_x v_f_y v_f_z]
    #   - t_o: Initial time (s) - always = 0
    #   - t_f: Final time (s) - time to fly trajectory
    #   - link_uri: Crazyradio dongle address
    # Description: Initializes PathPlanner object, pairs dongle and Crazyflie

    def __init__(self, r_o, v_o, r_f, v_f, t_o, t_f, link_uri):

        self.r_o = r_o
        self.v_o = v_o
        self.r_f = r_f
        self.v_f = v_f
        self.t_o = t_o
        self.t_f = t_f

        self._cf = Crazyflie(rw_cache='./cache') # Crazyflie object, used to pair dongle and Crazyflie
        self._scf = SyncCrazyflie(link_uri, self._cf) # SyncCrazyflie object, used to pair dongle and Crazyflie
        self._scf.open_link() # Opens links between dongle and Crazyflie

        self._mc = MotionCommander(self._scf) # MotionCommander object, used to send velocity setpoints to Crazyflie

    # Function: get_inputs
    # Parameters: 
    #   - self: PathPlanner object (represents the instance of the class that called function)​
    #   - wp: Number of waypoints in trajectory
    # Description: Gets trajectory equation parameters (r_o, v_o, etc.) from user

    def get_inputs(self, wp):

        for i in range(wp): # Loops wp times, creating arrays of position and velocity vectors so all waypoints are pre-loaded instead of input mid-flight

            if(i == 0): # If this is the first waypoint, enter all parameters (i.e. r_o, v_o, r_f, v_f, t_f)
                
                self.r_o[i][0] = float(input('Enter initial x position: '))
                self.r_o[i][1] = float(input('Enter initial y position: '))
                self.r_o[i][2] = float(input('Enter initial z position: '))
                print

                self.v_o[i][0] = float(input('Enter initial x velocity: '))
                self.v_o[i][1] = float(input('Enter initial y velocity: '))
                self.v_o[i][2] = float(input('Enter initial z velocity: '))
                print

                self.r_f[i][0] = float(input('Enter final x position: '))
                self.r_f[i][1] = float(input('Enter final y position: '))
                self.r_f[i][2] = float(input('Enter final z position: '))
                print

                self.v_f[i][0] = float(input('Enter final x velocity: '))
                self.v_f[i][1] = float(input('Enter final y velocity: '))
                self.v_f[i][2] = float(input('Enter final z velocity: '))
                print

                self.t_f[i] = float(input('Enter time to fly path (sec): '))
                # print(self.t_f)
                print

            else: # If this is not the first waypoint, only enter final parameters so waypoints are connected (i.e. r_o_new = r_f_old, v_o_new = v_f_old)

                self.r_o[i][0] = self.r_f[i-1][0] # New r_o equals old r_f
                self.r_o[i][1] = self.r_f[i-1][1]
                self.r_o[i][2] = self.r_f[i-1][2]

                self.v_o[i][0] = self.v_f[i-1][0] # New v_o equals old v_f
                self.v_o[i][1] = self.v_f[i-1][1]
                self.v_o[i][2] = self.v_f[i-1][2]

                self.r_f[i][0] = float(input('Enter final x position: ')) # Enter new r_f
                self.r_f[i][1] = float(input('Enter final y position: '))
                self.r_f[i][2] = float(input('Enter final z position: '))
                print

                self.v_f[i][0] = float(input('Enter final x velocity: ')) # Enter new v_f
                self.v_f[i][1] = float(input('Enter final y velocity: '))
                self.v_f[i][2] = float(input('Enter final z velocity: '))
                print

                self.t_f[i] = float(input('Enter time to fly path (sec): ')) # Enter new t_f
                # print(self.t_f) 
                print

    # Function: print_inputs
    # Parameters: 
    #   - self: PathPlanner object (represents the instance of the class that called function)​
    #   - wp: Number of waypoints in trajectory
    # Description: Prints trajectory equation parameters (r_o, v_o, etc.)

    def print_inputs(self, wp):

        for i in range(wp): # Prints all waypoints

            print(self.r_o[i])
            print(self.v_o[i])
            print(self.r_f[i])
            print(self.v_f[i])
            print(self.t_o)
            print(self.t_f[i])

    # Function: find_trajectory
    # Parameters: 
    #   - self: PathPlanner object (represents the instance of the class that called function)​
    #   - wp: Number of waypoints in trajectory
    # Description: Integrates acceleration equation over specified time range to calculate velocity components at each interval​, sending velocity
    # components to Crazyflie using _set_vel_setpoint function from MotionCommander class

    def find_trajectory(self, wp):
        
        for i in range(wp): # For each waypoint
            
            for x in np.arange(0, self.t_f[i]+0.1, 0.1): # Integrates from 0 to t_f in intervals of 0.1 seconds
                
                print(x)

                # This is the integral of the acceleration equation, i.e. the analytical equation for velocity
                vel_t = self.v_o[i] - ((2*self.v_f[i] + 4*self.v_o[i])*(x - self.t_o)*self.t_f[i]**2 - (x - self.t_o)*(6*self.r_f[i] - 6*self.r_o[i] + 3*x*self.v_f[i] + 3*x*self.v_o[i] + self.t_o*self.v_f[i] + 5*self.t_o*self.v_o[i])*self.t_f[i] + (x - self.t_o)*(6*self.r_f[i]*x - 6*self.r_o[i]*x - self.t_o**2*self.v_f[i] + self.t_o**2*self.v_o[i] + 3*x*self.t_o*self.v_f[i] + 3*x*self.t_o*self.v_o[i]))/(self.t_f[i] - self.t_o)**3          
                
                self._mc._set_vel_setpoint(vel_t[0], vel_t[1], vel_t[2], 0) # Send velocity components to Crazyflie

                # print(vel_t)
                time.sleep(0.1)
            
            self._mc.stop() # Stops Crazyflie (i.e. sets it to hover) at the end of each leg of the trajectory

    # Not used, but could be explored in future research
    # Velocity eq could be integrated again to find position and this function could send position components instead, not sure if it would be any
    # better than the current method using velocity

    def send_position_setpoint(self, x, y, z):
        self._cf.commander.send_position_setpoint(x, y, z, 0)


# Function: Main Loop
# Description:
#   - Asks user for number of waypoints in trajectory
#   - Initializes PathPlanner object; r_o, r_f, v_o, v_f are (# of waypoints)x3 arrays to allow waypoint coordinates to be pre-loaded
#   - Sends MotionCommander take_off() command to Crazyflie so that it hovers at default altitude (0.3 m)​
#   - Runs find_trajectory function on specified inputs
#   - Sends MotionCommander land() command to end flight​

if __name__ == '__main__':

    cflib.crtp.init_drivers(enable_debug_driver=False) # More initialization for radio communication

    wp = int(input('Enter the number of waypoints in the trajectory: ')) # Enter number of waypoints

    # Declares r_o, r_f, v_o, v_f as arrays of size (wp, 3), initialized to zero 
    # Example: let wp = 2, r_o, r_f, v_o, v_f = ((0, 0, 0), (0, 0, 0)) for two waypoints

    pp = PathPlanner(np.zeros((wp, 3), dtype=float),np.zeros((wp, 3), dtype=float),np.zeros((wp, 3), dtype=float),np.zeros((wp, 3), dtype=float),0,np.zeros(wp, dtype=float), URI)
    pp.get_inputs(wp)

    print('MC take_off()')
    pp._mc.take_off()
    time.sleep(2)
        
    pp.find_trajectory(wp) # Computes and flies trajectory

    print('MC land()')
    pp._mc.land()
    print('Done')
