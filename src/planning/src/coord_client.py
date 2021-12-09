#!/usr/bin/env python
# The line above tells Linux that this file is a Python script, and that the OS
# should use the Python interpreter in /usr/bin/env to run it. Don't forget to
# use "chmod +x [filename]" to make this script executable.

# Import the dependencies as described in example_pub.py
from numpy.core.shape_base import block
import rospy
import roslib; roslib.load_manifest('planning')
import sys
import numpy as np

from path_planner import PathPlanner
from controller import Controller
from baxter_interface import Limb, Gripper
from moveit_msgs.msg import OrientationConstraint
from geometry_msgs.msg import PoseStamped
from vision.msg import CardList
import time
from copy import deepcopy
import rospy
import actionlib
from moveit_msgs.msg import MoveGroupAction, MoveGroupGoal, MoveGroupFeedback, MoveGroupResult, JointConstraint, Constraints

class Coord_Client():
    def __init__(self):
        self.Kp = 0.45 * np.array([0.8, 2.5, 1.7, 2.2, 2.4, 3, 4])
        self.Kd = 0.015 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
        self.Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
        self.Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])
        arm = 'left' # right or left
        self.planner = PathPlanner("%s_arm" % arm)
        self.controller = Controller(self.Kp, self.Ki, self.Kd, self.Kw, Limb(arm))
        self.gripper = Gripper(arm)
        print(self.gripper.type())
        self.gripper.set_vacuum_threshold(400)

    def move(self, pose, loc, hover=True):
        if hover:
            hover_pose = deepcopy(pose)
            hover_pose.pose.position.z += 0.2
            plan_hover = self.planner.plan_to_pose(hover_pose, [])
            #raw_input("Press <Enter> to move the arm to hover %s " % loc)
            if not self.controller.execute_path(plan_hover, timeout=300, log=False):
                raise Exception("Execution failed")
        
        orien_const = OrientationConstraint()
        orien_const.link_name = "left_gripper"
        orien_const.header.frame_id = "base"
        orien_const.orientation.y = -1.0
        orien_const.absolute_x_axis_tolerance = 0.2
        orien_const.absolute_y_axis_tolerance = 0.2
        orien_const.absolute_z_axis_tolerance = 0.2
        orien_const.weight = 1.0
        plan_down = self.planner.plan_to_pose(pose, [orien_const])
        raw_input("Press <Enter> to move the arm to final position %s: " % loc)
        rospy.sleep(0.5)
        if not self.controller.execute_path(plan_down, timeout=300, log=False):
            raise Exception("Execution failed")
        rospy.sleep(0.5)
        print("done")

    def pickup(self):
        self.gripper.close(timeout=30)

    # Releases the vacuum gripper holding the card
    def release(self):
        self.gripper.open()

# Python's syntax for a main() method
if __name__ == '__main__':

    # Run this program as a new node in the ROS computation graph called
    # /listener_<id>, where <id> is a randomly generated numeric string. This
    # randomly generated name means we can start multiple copies of this node
    # without having multiple nodes with the same name, which ROS doesn't allow.
    # rospy.init_node('my_listener', anonymous=True)

    # listener()
    rospy.init_node('moveit_node')
    client = Coord_Client()
    card_loc = PoseStamped()

    card_loc.header.frame_id = "base"

    #x, y, and z position
    card_loc.pose.position.x = 0.471
    card_loc.pose.position.y = 0.252
    card_loc.pose.position.z = 0.048

    # Translation: [0.871, -0.252, 0.048]

    #Orientation as a quaternion
    card_loc.pose.orientation.x = 0.0
    card_loc.pose.orientation.y = -1.0
    card_loc.pose.orientation.z = 0.0
    card_loc.pose.orientation.w = 0.0
    planner.plan_to_pose(card_loc, [])

