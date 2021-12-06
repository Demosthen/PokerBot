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

    planner = PathPlanner("right_arm")

    # Baxter K-values
    Kp = 0.45 * np.array([0.8, 2.5, 1.7, 2.2, 2.4, 3, 4])
    Kd = 0.015 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
    Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
    Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])

    controller = Controller(Kp, Ki, Kd, Kw, Limb('right'))

    while not rospy.is_shutdown():
        while not rospy.is_shutdown():
            try:
                # x, y, z = -, -0.228, -0.004
                goal_1 = PoseStamped()
                goal_1.header.frame_id = "right_hand_camera"
                t = tf.TransformListener()
                # 0.640, -0.154, -0.001
                #x, y, and z position
                goal_1.pose.position.x = 0.0300999662754
                goal_1.pose.position.y = 0.0460
                goal_1.pose.position.z = 0

                #Orientation as a quaternion
                goal_1.pose.orientation.x = 0.0
                goal_1.pose.orientation.y = -1.0
                goal_1.pose.orientation.z = 0.0
                goal_1.pose.orientation.w = 0.0

                tf.waitforTransform("/base", "/right_hand_camera", rospy.Time(), rospy.Duration(4.0))
                transd_pose = t.transformPose("base", goal_1)
                # Might have to edit this . . . 
                print(transd_pose)
                plan = planner.plan_to_pose(transd_pose, [])

                raw_input("Press <Enter> to move the right arm to goal pose 1: ")
                # if not planner.execute_plan(plan):
                #     raise Exception("Execution failed")
                if not controller.execute_path(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print(e)
                traceback.print_exc()
            else:
                break

        while not rospy.is_shutdown():
            try:
                goal_2 = PoseStamped()
                goal_2.header.frame_id = "base"

                #x, y, and z position
                goal_2.pose.position.x = 0.6
                goal_2.pose.position.y = -(-0.3)
                goal_2.pose.position.z = 0.0

                #Orientation as a quaternion
                goal_2.pose.orientation.x = 0.0
                goal_2.pose.orientation.y = -1.0
                goal_2.pose.orientation.z = 0.0
                goal_2.pose.orientation.w = 0.0

                plan = planner.plan_to_pose(goal_2, [])

                raw_input("Press <Enter> to move the right arm to goal pose 2: ")
                if not controller.execute_path(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print(e)
            else:
                break

        while not rospy.is_shutdown():
            try:
                goal_3 = PoseStamped()
                goal_3.header.frame_id = "base"

                #x, y, and z position
                goal_3.pose.position.x = 0.6
                goal_3.pose.position.y = -(-0.1)
                goal_3.pose.position.z = 0.1

                #Orientation as a quaternion
                goal_3.pose.orientation.x = 0.0
                goal_3.pose.orientation.y = -1.0
                goal_3.pose.orientation.z = 0.0
                goal_3.pose.orientation.w = 0.0

                plan = planner.plan_to_pose(goal_3, [])

                raw_input("Press <Enter> to move the right arm to goal pose 3: ")
                if not controller.execute_path(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print(e)
            else:
                break

if __name__ == '__main__':
    rospy.init_node('moveit_node')
    main()
