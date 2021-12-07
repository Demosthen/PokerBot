#!/usr/bin/env python
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Point
from ar_track_alvar_msgs.msg import AlvarCorners, AlvarMarkers
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from vision.msg import CardList
from vision.srv import fuck

#SUBSCRIBE TO THE TOPIC THAT POSTS EACH OF THE ALVARCORNERS (/ar_corners), ALVARMARKER (ar_pose_marker), CardList (/pokerbot/card)
#Write a callback function to respond whenever we get something from each topic
#Get the relative transformation between the two ar markers (how far apart are they in the x axis and y axis) in 3D and get the same transformation in 2D
#Use this to get the card coordinates by applying the inverse transformation from the 2D to the 3D

markers = None
coords = None
corners = None
cards = None

def get_markers(message):
    global markers
    markers = message.markers
    # Print the contents of the message to the console
    #print("Message: %s" % message)
def get_coords_cards(message):
    global coords, cards
    cards = message.cards
    coords = message.coords

    # Print the contents of the message to the console
    #print("Message: %s" % message.msg + ", Sent at: %s" % message.timestamp  + ", Received at: %s" % rospy.get_time()  )
def get_corners(message):
    global corners
    corners = message.corners

    # Print the contents of the message to the console
    #print("Message: %s" % message.msg + ", Sent at: %s" % message.timestamp  + ", Received at: %s" % rospy.get_time()  )

# class CardResponse(): # Implement this as a new message type
#     def __init__(self, card_list):
#         self.card_list = card_list
def pointcloud_projection(req):
    global markers
    global coords
    global corners
    global cards
    if markers is None or coords is None or corners is None or cards is None:
        return None
    # changex3d = np.abs(markers[0].pose.pose.position.x - markers[1].pose.pose.position.x)
    # changey3d = np.abs(markers[0].pose.pose.position.y - markers[1].pose.pose.position.y)
    orient = markers[0].pose.pose.orientation
    orientation_list = [orient.x, orient.y, orient.z, orient.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    changex3d = (0.046 * np.cos(yaw))
    changey3d = (0.046 * np.sin(yaw))
    changex2d = np.abs(corners[0].x - corners[1].x)
    changey2d = np.abs(corners[0].y - corners[1].y)
    z_coord = markers[0].pose.pose.position.z
    y_scale = changex3d/changey2d # intentional swap bc image x/y is swapped with transform x/y
    x_scale = changey3d/changex2d
    #import pdb; pdb.set_trace()
    print("SCALE:", x_scale, y_scale)
    #print(y_scale)
    tf_cards = []
    tf_coords = []
    avg_x = sum([c.x for c in corners]) / 4
    avg_y = sum([c.y for c in corners]) / 4
    distances = []
    for i, (coord, card) in enumerate(zip(coords, cards)):
        print("CARD:", coord.x, coord.y)
        dist_from_center = (coord.x - 640) ** 2 + (coord.y - 400) ** 2
        distances.append(dist_from_center)
        diff_x = (coord.x - avg_x) * x_scale
        diff_y = (coord.y - avg_y) * y_scale
        x = markers[0].pose.pose.position.x + diff_y
        y = markers[0].pose.pose.position.y - diff_x
        tf_coords.append(Point(x, y, z_coord))
        tf_cards.append(card)

    #sorted_cards = [card for _, card in sorted(zip(distances,tf_cards), key=lambda pair: pair[0])]
    #sorted_coords = [coord for _, coord in sorted(zip(distances,tf_coords), key=lambda pair: pair[0])]
    # coords_and_cards = zip(tf_coords, tf_cards)
    # arranged = sorted(coords_and_cards)
    # tuples = zip(*arranged)
    # tf_coords, tf_cards = [list(tuple) for tuple in tuples]
    return CardList(tf_cards, tf_coords, len(tf_cards))





# Define the method which contains the node's main functionality
def listener():

    # Create a new instance of the rospy.Subscriber object which we can use to
    # receive messages of type std_msgs/String from the topic /chatter_talk.
    # Whenever a new message is received, the method callback() will be called
    # with the received message as its first argument.
    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, get_markers)
    rospy.Subscriber('/pokerbot/card', CardList, get_coords_cards)
    rospy.Subscriber('/ar_corners', AlvarCorners, get_corners)
    rospy.Service('twod_to_3d', fuck, pointcloud_projection)
    # Wait for messages to arrive on the subscribed topics, and exit the node
    # when it is killed with Ctrl+C
    rospy.spin()


# Python's syntax for a main() method
if __name__ == '__main__':

    # Run this program as a new node in the ROS computation graph called
    # /listener_<id>, where <id> is a randomly generated numeric string. This
    # randomly generated name means we can start multiple copies of this node
    # without having multiple nodes with the same name, which ROS doesn't allow.
    rospy.init_node('service_node3d', anonymous=True)

    listener()
