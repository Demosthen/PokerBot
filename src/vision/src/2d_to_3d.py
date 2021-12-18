#!/usr/bin/env python
import rospy
import numpy as np
from geometry_msgs.msg import PoseStamped, Point
from ar_track_alvar_msgs.msg import AlvarCorners, AlvarMarkers
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from sensor_msgs.msg import Image, CameraInfo
from vision.msg import CardList
from vision.srv import fuck
import tf
USE_TWO_TAGS = True
USE_INTRINSIC = True
#SUBSCRIBE TO THE TOPIC THAT POSTS EACH OF THE ALVARCORNERS (/ar_corners), ALVARMARKER (ar_pose_marker), CardList (/pokerbot/card)
#Write a callback function to respond whenever we get something from each topic
#Get the relative transformation between the two ar markers (how far apart are they in the x axis and y axis) in 3D and get the same transformation in 2D
#Use this to get the card coordinates by applying the inverse transformation from the 2D to the 3D

markers = None
coords = None
corners = None
corners2 = None
cards = None
K = None
inv_K = None
tf_listener = None
transformer = None
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
    global corners, corners2
    corners = message.corners
    corners2 = message.corners2

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
    if USE_TWO_TAGS:
        changex3d = markers[0].pose.pose.position.x - markers[1].pose.pose.position.x
        changey3d = markers[0].pose.pose.position.y - markers[1].pose.pose.position.y
        marker_pixx1 = sum([c.x for c in corners]) / 4
        marker_pixx2 = sum([c.x for c in corners2]) / 4
        marker_pixy1 = sum([c.y for c in corners]) / 4
        marker_pixy2 = sum([c.y for c in corners2]) / 4
        changex2d = np.abs(marker_pixx1 - marker_pixx2)
        changey2d = np.abs(marker_pixy1 - marker_pixy2)
    else:
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


def skew_3d(omega):
    """
    Converts a rotation vector in 3D to its corresponding skew-symmetric matrix.
    
    Args:
    omega - (3,) ndarray: the rotation vector
    
    Returns:
    omega_hat - (3,3) ndarray: the corresponding skew symmetric matrix
    """

    # YOUR CODE HERE
    return np.array([[0, -omega[2], omega[1]],
                        [omega[2], 0, -omega[0]],
                        [-omega[1], omega[0], 0]])

def hat_3d(xi):
    """
    Converts a 3D twist to its corresponding 4x4 matrix representation
    
    Args:
    xi - (6,) ndarray: the 3D twist
    
    Returns:
    xi_hat - (4,4) ndarray: the corresponding 4x4 matrix
    """

    # YOUR CODE HERE
    xi_hat = np.zeros((4,4))
    xi_hat[:3, :3] = skew_3d(xi[3:])
    xi_hat[:3, -1] = xi[:3]
    return xi_hat

def intrinsic_projection(req):
    global markers
    global coords
    global corners
    global cards
    if markers is None or coords is None or corners is None or cards is None or K is None:
        return None
    if USE_TWO_TAGS and len(markers) != 2:
        return None
   
    #Wait for transform to get published by rviz
    tf_listener.waitForTransform('/left_hand_camera', '/base', rospy.Time(), rospy.Duration(10))
    
    (trans, rot) = tf_listener.lookupTransform('/left_hand_camera', '/base', rospy.Time(0))
    (trans2, rot2) = tf_listener.lookupTransform('/base', '/left_hand_camera', rospy.Time(0))
    transform = transformer.fromTranslationRotation(trans, rot) # base to camera
    inv_transform =transformer.fromTranslationRotation(trans2, rot2) # camera to base
    tf_marker_coords = [np.matmul(transform, np.array([m.pose.pose.position.x, m.pose.pose.position.y, m.pose.pose.position.z, 1])) for m in markers]
    z_coord = sum([c[2] for c in tf_marker_coords]) / len(tf_marker_coords)
    distances = []
    tf_coords = []
    tf_cards = []
    for i, (coord, card) in enumerate(zip(coords, cards)):
        print("CARD:", coord.x, coord.y)
        homog_coord = np.array([coord.x, coord.y, 1]) # if fails, flip x and y and negate the homogeneous y coordinate
        three_d = np.matmul(inv_K, homog_coord)
        print(three_d)
        three_d *= z_coord / three_d[2]
        h_three_d = np.array([three_d[0], three_d[1], three_d[2], 1])
        three_d = np.matmul(inv_transform, h_three_d)
        dist_from_center = (coord.x - 400) ** 2 + (coord.y - 640) ** 2
        distances.append(dist_from_center)
        x, y, z = three_d[0], three_d[1], three_d[2]
        tf_coords.append(Point(x, y, z))
        tf_cards.append(card)
    return CardList(tf_cards, tf_coords, len(tf_cards))


def simple_projection(req):
    global markers
    global corners
    global corners2
    global coords
    global cards

    hand_index = None
    hand_pixels = None
    for i in range(len(markers)):
        if markers[i].id == 7: # AR tag 7 indicates the hand
            hand_index = i
            if (i == 0):
                hand_pixels = corners
            elif (i == 1):
                hand_pixels = corners2
            else:
                print("Why are we here?")
            break
    if hand_pixels is None:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        return None
    print(hand_pixels)
    avg_y = sum([c.y for c in hand_pixels]) / 4
    hand_len = 0
    tf_coords = []
    tf_cards = []
    for _, (coord, card) in enumerate(zip(coords, cards)):
        if abs(coord.y - avg_y) < 200:
            tf_coords.append(Point(markers[hand_index].pose.pose.position.x, markers[hand_index].pose.pose.position.y + 0.1 + 0.1*hand_len, markers[hand_index].pose.pose.position.z))
            tf_cards.append(card)
            hand_len += 1
        else:
            print("ignoring center card:", card)

    return CardList(tf_cards, tf_coords, len(tf_cards))

def get_cam_info(req):
    global K, inv_K
    K = np.reshape(req.K, (3, 3))
    inv_K = np.linalg.inv(K)

# Define the method which contains the node's main functionality
def listener():

    # Create a new instance of the rospy.Subscriber object which we can use to
    # receive messages of type std_msgs/String from the topic /chatter_talk.
    # Whenever a new message is received, the method callback() will be called
    # with the received message as its first argument.
    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, get_markers)
    rospy.Subscriber('/pokerbot/card', CardList, get_coords_cards)
    rospy.Subscriber('/ar_corners', AlvarCorners, get_corners)
    rospy.Service('twod_to_3d', fuck, intrinsic_projection if USE_INTRINSIC else pointcloud_projection)
    if USE_INTRINSIC:
        rospy.Subscriber("/cameras/left_hand_camera/camera_info", CameraInfo, get_cam_info)
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
    tf_listener = tf.TransformListener()
    transformer = tf.listener.TransformerROS()
    listener()
