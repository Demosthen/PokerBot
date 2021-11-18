#!/usr/bin/env python
import rospy
import numpy as np
from darknet import *

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String

class VisionPublisher:   
    #Callback for when an image is received
    def imgReceived(self, img):
        #Save the image in the instance variable
        # self.lastImage = img
        im = self.bridge.imgmsg_to_cv2(img)
        r = detect_np(self.net, self.meta, im, 0.1)
        # classification = classify(im)
        #Print an alert to the console
        print("received", rospy.get_time())
        print(str(r))
        self.pub.publish(str(r))

    #When another node calls the service, return the last image
    def getLastImage(self, request):
        #Print an alert to the console
        #print("Image requested!")

        #Return the last image
        pass

    def __init__(self):
        #Create an instance variable to store the last image received
        self.lastImage = None
        self.bridge = CvBridge()

        # Import neural net metadata
        self.net = load_net(b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/tiny2-coco.cfg", b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/tiny2_coco_100k_candidate.weights", 0)
        self.meta = load_meta(b"/home/cc/ee106a/fl21/class/ee106a-afr/ros_workspaces/pokerbot/src/vision/src/PokerBot/output.data")

        #Initialize the node
        rospy.init_node('cam_listener')

        #Subscribe to the image topic
        rospy.Subscriber("/usb_cam/image_raw", Image, self.imgReceived)

        #Create the publisher
        self.pub = rospy.Publisher('/pokerbot/card', String, queue_size=10)
        self.r = rospy.Rate(100) # 10 hz 

    def run(self):
        rospy.spin()

#Python's syntax for a main() method
if __name__ == '__main__':
  node = VisionPublisher()
  node.run()
