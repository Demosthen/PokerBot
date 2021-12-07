#!/usr/bin/env python
import rospy
import numpy as np
from card_detector import *

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from vision.msg import CardList
from geometry_msgs.msg import Point

from collections import OrderedDict

class VisionPublisher:   
    #Callback for when an image is received
    def imgReceived(self, img):
        #Save the image in the instance variable
        # self.lastImage = img
        im = self.bridge.imgmsg_to_cv2(img)
        r = self.net.detect(im, 0.5, nms=0.6)[1]
        r.reverse()
        #Print an alert to the console
        card_dict = OrderedDict()
        for card in r:
            name = card[0]
            if (name in card_dict):
                if (card_dict[name][0]):
                    break
                else:
                    card_dict[name][0] = 1
                    card_dict[name][1] = (card_dict[name][1] + card[2][0]) / 2
                    card_dict[name][2] = (card_dict[name][2] + card[2][1]) / 2
                    # print("CARD %s" %name, card_dict[name])
            else:
                card_dict[name] = [0] + list(card[2])
        msg = CardList()
        msg.count = len(card_dict)
        msg.cards = card_dict.keys()
        msg.coords = [Point(card_dict[item][1], card_dict[item][2], 0) for item in card_dict]
        # print(msg)
        self.pub.publish(msg)

    def __init__(self):
        #Create an instance variable to store the last image received
        self.lastImage = None
        self.bridge = CvBridge()

        # Import neural net metadata
        self.net = ImageDetector(
        config_file="/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/custom_yolo.config",
        data_file="/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/cards.data",
        weights="/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/darknet/weights/backup/yolov4-tiny-custom_30000.weights")

        #Initialize the node
        rospy.init_node('cam_listener')

        #Subscribe to the image topic
        rospy.Subscriber("/cameras/right_hand_camera/image", Image, self.imgReceived)
        # rospy.Subscriber("/cameras/left_hand_camera/image", Image, self.imgReceived)
        
        #Create the publisher
        self.pub = rospy.Publisher('/pokerbot/card', CardList, queue_size=2)
        self.r = rospy.Rate(100) # 10 hz 

    def run(self):
        rospy.spin()

#Python's syntax for a main() method
if __name__ == '__main__':
  node = VisionPublisher()
  node.run()
