#!/usr/bin/env python
"""
Path Planning Script for Lab 7
Author: Valmik Prabhu
"""
import sys
from baxter_interface import Limb

import rospy
import numpy as np
import traceback

from moveit_msgs.msg import OrientationConstraint, RobotTrajectory
from geometry_msgs.msg import PoseStamped
import tf

from path_planner import PathPlanner
try:
    from original_controller import Controller
except ImportError:
    pass
    
def main():
    """
    Main Script
    """

    # Make sure that you've looked at and understand path_planner.py before starting

    # planner = PathPlanner("right_arm")
    planner = PathPlanner("left_arm")

    # Baxter K-values
    Kp = 0.45 * np.array([0.8, 2.5, 1.7, 2.2, 2.4, 3, 4])
    Kd = 0.015 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
    Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
    Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])

    # controller = Controller(Kp, Ki, Kd, Kw, Limb('right'))
    controller = Controller(Kp, Ki, Kd, Kw, Limb('left'))

    while not rospy.is_shutdown():
        while not rospy.is_shutdown():
            try:
                # x, y, z = -, -0.228, -0.004
                goal_1 = PoseStamped()
                goal_1.header.frame_id = "base"
        #   x:  0.58446449893
        #   y: -0.119159108905
        #   z: -0.194665700564


                #x, y, and z position
                goal_1.pose.position.x = 0.601435412454
                goal_1.pose.position.y = -0.26602931234
                goal_1.pose.position.z = -0.05

                #Orientation as a quaternion
                goal_1.pose.orientation.x = 0.0
                goal_1.pose.orientation.y = -1.0
                goal_1.pose.orientation.z = 0.0
                goal_1.pose.orientation.w = 0.0
                # Might have to edit this . . . 
                plan = planner.plan_to_pose(goal_1, [])

                raw_input("Press <Enter> to move the arm to goal pose 1: ")
                # if not planner.execute_plan(plan):
                #     raise Exception("Execution failed")
                if not controller.execute_path(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print(e)
                traceback.print_exc()
            else:
                break

if __name__ == '__main__':
    rospy.init_node('moveit_node')
    main()
