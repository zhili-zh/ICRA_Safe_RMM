#!/usr/bin/env python
"""
behavior_planner.py

todo
"""
# Companion code for the UConn undergraduate Honors Thesis "Evaluating Driving
# Performance of a Novel Behavior Planning Model on Connected Autonomous
# Vehicles" by Keyur Shah (UConn '20). Thesis was advised by Dr. Fei Miao;
# see http://feimiao.org/research.html.
#
# This code is meant for use with the autonomous vehicle simulator CARLA
# (https://carla.org/).
#
# Disclaimer: The CARLA project, which this project uses code from, follows the
# MIT license. The license is available at https://opensource.org/licenses/MIT.

import os
import glob
import sys
from .tools.misc import scalar_proj, norm
from .enums_old import RoadOption

try:
    os_version = 'win-amd64' if os.name == 'nt' else 'linux-x86_64'
    sys.path.append(glob.glob(f'/opt/carla-simulator/PythonAPI/carla/dist/carla-0.9.10-py3.7-{os_version}.egg')[0])
except IndexError:
    pass

import carla


class BehaviorPlanner:
    """
    Base class to define behavior planners in CARLA
    """

    def __init__(self, vehicle, dt, param_dict):
        """
        todo

        :param vehicle:
        :param dt:
        :param param_dict:
        """
        self.dt = dt
        self.vehicle = vehicle
        self.path_planner = None
        self.world = self.vehicle.get_world()
        self.map = self.vehicle.get_world().get_map()
        self.current_waypoint = None

        self.Tds = param_dict['Tds']
        self.theta_a = param_dict['theta_a']
        # Safety parameters
        self.theta_l = param_dict['theta_l']
        self.theta_c = param_dict['theta_c']
        self.theta_r = param_dict['theta_r']
        #self.change_distance = param_dict['chg_distance']

    def discrete_state(self):
        """
        todo
        """
        # path planner is not allowed to take left/right turn roadoptions,
        # so target road option will necessarily be one of LANEFOLLOW (LK),
        # CHANGELANELEFT (CL), or CHANGELANERIGHT (CR) and thus we use the
        # target road option variable as our state
        return self.path_planner._target_road_option

    def get_measurements(self):
        """
        todo
        """
        try:
            velocity_fwd = scalar_proj(
                self.vehicle.get_velocity(),
                self.current_waypoint.transform.get_forward_vector()
            )
        except:
            # return 0 if we can't find the fwd velocity
            print("Warning-- could not find forward velocity!")
            velocity_fwd = 0.0

        acceleration = norm(self.vehicle.get_acceleration())
        is_changing_lanes = (self.path_planner._target_road_option in {RoadOption.CHANGELANELEFT,
                                                                        RoadOption.CHANGELANERIGHT})

        if is_changing_lanes:
            comfort = 1
        elif acceleration >= self.theta_a:
            comfort = 2
        else:
            comfort = 3

        return velocity_fwd, comfort

    '''
    def run_step(self, debug=False):
        """
        todo

        :param debug:
        """
        self.current_waypoint = self.map.get_waypoint(self.vehicle.get_location())

        control = carla.VehicleControl()

        if debug:
            control.steer = 0.0
            control.throttle = 0.0
            control.brake = 0.0
            control.hand_brake = False
            control.manual_gear_shift = False

        return control
        pass
    '''
    def emergency_stop(self):
        """
        todo
        """
        control = carla.VehicleControl()
        control.steer = 0.0
        control.throttle = 0.0
        control.brake = 1.0
        control.hand_brake = False

        return control
