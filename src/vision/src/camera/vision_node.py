#!/usr/bin/env python
import rospy

from sensor_msgs.msg import Image

class VisionPublisher:

  #Callback for when an image is received
  def imgReceived(self, message):
    #Save the image in the instance variable
    self.lastImage = message

    #Print an alert to the console
    #print(rospy.get_name() + ":Image received!")

  #When another node calls the service, return the last image
  def getLastImage(self, request):
    #Print an alert to the console
    #print("Image requested!")

    #Return the last image
    return ...

  def __init__(self):
    #Create an instance variable to store the last image received
    self.lastImage = None

    #Initialize the node
    rospy.init_node('cam_listener')

    #Subscribe to the image topic
    rospy.Subscriber("/cameras/left_hand_camera/image", Image, self.imgReceived)

    #Create the service
    # rospy.Service('last_image', ImageSrv, self.getLastImage)
    self.pub = rospy.Publisher('testtestestestestsetsetsetes', )
    

  def run(self):
    rospy.spin()

#Python's syntax for a main() method
if __name__ == '__main__':
  node = VisionPublisher()
  node.run()
