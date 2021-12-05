#!/usr/bin/env python
# The line above tells Linux that this file is a Python script, and that the OS
# should use the Python interpreter in /usr/bin/env to run it. Don't forget to
# use "chmod +x [filename]" to make this script executable.

# Import the dependencies as described in example_pub.py
import rospy
import sys
import numpy as np
from path_planner import PathPlanner
from controller import Controller
from baxter_interface import Limb
from gameplay import gameplay
from moveit_msgs.msg import OrientationConstraint
from geometry_msgs.msg import PoseStamped

Kp = 0.45 * np.array([0.8, 2.5, 1.7, 2.2, 2.4, 3, 4])
Kd = 0.015 * np.array([2, 1, 2, 0.5, 0.8, 0.8, 0.8])
Ki = 0.01 * np.array([1.4, 1.4, 1.4, 1, 0.6, 0.6, 0.6])
Kw = np.array([0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9])

# planner = PathPlanner("right_arm")
# controller = Controller(Kp, Ki, Kd, Kw, Limb('right'))

# Define the callback method which is called whenever this node receives a 
# message on its subscribed topic. The received message is passed as the first
# argument to callback().
def callback(message):
    #input the logic, create a posestamp object and input the point coords into it
    # alternatively, call a function in a different file to implement

    #Initiates the gameplay class with the list of points as input
    # returns the point object that 
    play = gameplay(message)

    my_play = play.compare_cards()

    orien_const = OrientationConstraint()
    orien_const.link_name = "left_gripper"
    orien_const.header.frame_id = "base"
    orien_const.orientation.y = -1.0
    orien_const.absolute_x_axis_tolerance = 0.1
    orien_const.absolute_y_axis_tolerance = 0.1
    orien_const.absolute_z_axis_tolerance = 0.1
    orien_const.weight = 1.0
    try:
        # account for gripper size so it doesn't crash 
        # directly into the card's coordinates
        x, y, z = 0, 0, 0.8
        card_loc = PoseStamped()
        card_loc.header.frame_id = "base"

        #x, y, and z position
        card_loc.pose.position.x = my_play.x + x
        card_loc.pose.position.y = my_play.y + y
        card_loc.pose.position.z = my_play.z + z

        #Orientation as a quaternion
        card_loc.pose.orientation.x = 0.0
        card_loc.pose.orientation.y = -1.0
        card_loc.pose.orientation.z = 0.0
        card_loc.pose.orientation.w = 0.0

        # run the pose stamped object through planner
        plan = planner.plan_to_pose(card_loc, [])

        raw_input("Press <Enter> to move the right arm to position of first card: ")
        # if not planner.execute_plan(plan):
        #     raise Exception("Execution failed")
        if not controller.execute_path(plan):
            raise Exception("Execution failed")
    except Exception as e:
        print(e)
        traceback.print_exc()

    # Print the contents of the message to the console
    print("Message: %s" % message.msg + ", Sent at: %s" % message.timestamp  + ", Received at: %s" % rospy.get_time()  )

# Define the method which contains the node's main functionality
"""def listener():

    # Create a new instance of the rospy.Subscriber object which we can use to
    # receive messages of type std_msgs/String from the topic /chatter_talk.
    # Whenever a new message is received, the method callback() will be called
    # with the received message as its first argument.
    # Redefined message as List of Points
    rospy.Subscriber("point_cloud_publisher", List, callback)

    # Wait for messages to arrive on the subscribed topics, and exit the node
    # when it is killed with Ctrl+C
    rospy.spin()
"""

def twodto3d():
    rospy.wait_for_service('twod_to_3d')
    
    #need to change out service class
    two_to_3d = rospy.ServiceProxy('twod_to_3d', CardList)

    try:
        calling = two_to_3d
    except rospy.ServiceException as exc:
        print("Service did not process request: " + str(exc))
    return 1


# Python's syntax for a main() method
if __name__ == '__main__':

    # Run this program as a new node in the ROS computation graph called
    # /listener_<id>, where <id> is a randomly generated numeric string. This
    # randomly generated name means we can start multiple copies of this node
    # without having multiple nodes with the same name, which ROS doesn't allow.
    # rospy.init_node('my_listener', anonymous=True)

    # listener()
    rospy.init_node('moveit_node')
    planner = PathPlanner("right_arm")
    controller = Controller(Kp, Ki, Kd, Kw, Limb('right'))
    card_loc = PoseStamped()
    card_loc.header.frame_id = "base"

    #x, y, and z position
    card_loc.pose.position.x = 0.862
    card_loc.pose.position.y = -0.22
    card_loc.pose.position.z = 0.041
# [0.862, -0.220, 0.041]
    # Translation: [0.871, -0.252, 0.048]

    #Orientation as a quaternion
    card_loc.pose.orientation.x = 0.0
    card_loc.pose.orientation.y = -1.0
    card_loc.pose.orientation.z = 0.0
    card_loc.pose.orientation.w = 0.0
    planner.plan_to_pose(card_loc, [])

