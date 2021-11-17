#!/usr/bin/env python
"""
Path Planning Script for Lab 7
Author: Valmik Prabhu
"""
import sys
import baxter_interface
assert sys.argv[1] in ("sawyer", "baxter")
ROBOT = sys.argv[1]

if ROBOT == "baxter":
    from baxter_interface import Limb
else:
    from intera_interface import Limb

import rospy
import numpy as np
import traceback

from moveit_msgs.msg import OrientationConstraint, RobotTrajectory
from geometry_msgs.msg import PoseStamped

from path_planner import PathPlanner
try:
    from controller import Controller
except ImportError:
    pass
    
def main():
    """
    Main Script
    """

    # Make sure that you've looked at and understand path_planner.py before starting

    planner = PathPlanner("left_arm")

    if ROBOT == "sawyer":
        Kp = 0.2 * np.array([0.4, 2, 1.7, 1.5, 2, 2, 3])
        Kd = 0.01 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
        Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
        Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])
    else:
        Kp = 0.45 * np.array([0.8, 2.5, 1.7, 2.2, 2.4, 3, 4])
        Kd = 0.015 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
        Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
        Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])

    controller = Controller(Kp, Ki, Kd, Kw, Limb('left'))

    ##
    ## Add the obstacle to the planning scene here
    # table_size = [0.4, 1.2, 0.1]
    # table_pose = PoseStamped()
    # table_pose.header.frame_id = "base"
    # table_pose.pose.position.x = 0.5
    # table_pose.pose.position.y = 0
    # table_pose.pose.position.z = -0.2
    # table_pose.pose.orientation.x = 0
    # table_pose.pose.orientation.y = 0

    # table_pose.pose.orientation.z = 0
    # table_pose.pose.orientation.w = 1
    # planner.add_box_obstacle(table_size, "table", table_pose)

    # wall_size = [0.5, 0.1, 1]
    # wall_pose = PoseStamped()
    # wall_pose.header.frame_id = "base"
    # wall_pose.pose.position.x = 0.8
    # wall_pose.pose.position.y = 0.2
    # wall_pose.pose.position.z = -0.2
    # wall_pose.pose.orientation.x = 0
    # wall_pose.pose.orientation.y = 0
    # wall_pose.pose.orientation.z = 0
    # wall_pose.pose.orientation.w = 1
    # planner.add_box_obstacle(wall_size, "wall", wall_pose)
    ##

    # planner.remove_obstacle("wall")

    # #Create a path constraint for the arm
    # #UNCOMMENT FOR THE ORIENTATION CONSTRAINTS PART
    orien_const = OrientationConstraint()
    orien_const.link_name = "left_gripper"
    orien_const.header.frame_id = "base"
    orien_const.orientation.y = -1.0
    orien_const.absolute_x_axis_tolerance = 0.1
    orien_const.absolute_y_axis_tolerance = 0.1
    orien_const.absolute_z_axis_tolerance = 0.1
    orien_const.weight = 1.0

    while not rospy.is_shutdown():

        while not rospy.is_shutdown():
            try:
                if ROBOT == "baxter":
                    x, y, z = 0.47, -0.85, 0.07
                else:
                    x, y, z = 0.8, 0.05, 0.07
                goal_1 = PoseStamped()
                goal_1.header.frame_id = "base"

                #x, y, and z position
                goal_1.pose.position.x = x
                goal_1.pose.position.y = -y
                goal_1.pose.position.z = z

                #Orientation as a quaternion
                goal_1.pose.orientation.x = 0.0
                goal_1.pose.orientation.y = -1.0
                goal_1.pose.orientation.z = 0.0
                goal_1.pose.orientation.w = 0.0

                # Might have to edit this . . . 
                plan = planner.plan_to_pose(goal_1, [])

                raw_input("Press <Enter> to move the right arm to goal pose 1: ")
                # if not planner.execute_plan(plan):
                #     raise Exception("Execution failed")
                if not controller.execute_path(plan):
                    raise Exception("Execution failed")
            except Exception as e:
                print e
                traceback.print_exc()
            else:
                break

        while not rospy.is_shutdown():
            try:
                #creates a new posestamped object
                goal_2 = PoseStamped()
                #coords relative to base
                goal_2.header.frame_id = "base"

                ##to do: subscribe to publisher to obtain coords 

                # make game play decision

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
                print e
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
                print e
            else:
                break

if __name__ == '__main__':
    rospy.init_node('moveit_node')
    main()
