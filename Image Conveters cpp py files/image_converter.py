#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('mybot_description')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
class image_converter:

  def __init__(self):
    #self.image_pub = rospy.Publisher("videosrc",Image,queue_size=10)
    rospy.init_node('image_converter', anonymous=True)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/mybot/camera1/image_raw",Image,self.callback)
    self.image=None
  def callback(self,data):
    try:
      self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
      cv2.circle(self.image, (50,50), 10, 255)

    cv2.imshow("Image window", self.image)
    cv2.waitKey(3)

  def write(self,id,dir):
    cv2.imwrite(os.path.join(dir,id+'.png'),self.img)

def main(args):
  os.mkdir('room_images')
  r=rospy.Rate(10)
  id='frame_0'
  try:
    while not rospy.is_shutdown():
      ic=image_converter()
      ic.write(id=id,dir='room_images')
      id=id[:-1]+int(id[-1]+1)
      r.sleep()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)