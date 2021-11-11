#!/usr/bin/env python
import rospy
import numpy as np
from card_detector import classify

from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String

class VisionPublisher:   
    #Callback for when an image is received
    def imgReceived(self, img):
        #Save the image in the instance variable
        self.lastImage = img
        im = self.bridge.imgmsg_to_cv2(img, desired_encoding="rgb8")
        print(im.shape)
        classification = classify(im, 0.01)
        #Print an alert to the console
        print(str(classification))

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

        #Initialize the node
        rospy.init_node('cam_listener')

        #Subscribe to the image topic
        rospy.Subscriber("/cameras/left_hand_camera/image", Image, self.imgReceived)

        #Create the publisher
        self.pub = rospy.Publisher('testtestestestestsetsetsetes', String, queue_size=10)
        self.r = rospy.Rate(10) # 10 hz 

    def run(self):
        rospy.spin()

#Python's syntax for a main() method
if __name__ == '__main__':
  node = VisionPublisher()
  node.run()
