#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('mybot_description')
import sys
import rospy
import cv2
import numpy as np
import scipy.ndimage
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
'''
def empty(a):
  pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
cv2.createTrackbar("Threshold1", "Parameters", 227, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 50, 255, empty)
cv2.createTrackbar("Area", "Parameters", 2000, 30000, empty)
'''
#images=[]
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'saved_images')
if not os.path.exists(final_directory):
  os.makedirs(final_directory)
os.chdir(final_directory)
def hsv(img):
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  lower = np.array([0,0,60])
  upper= np.array([255,20,180])
  mask = cv2.inRange(hsv, lower, upper)
  res = cv2.bitwise_and(img,img, mask= mask)
  cv2.imshow("res",res)
  z=np.zeros(res.shape)
  return (np.linalg.norm(res-z))
  
def getContours(img, imgContour, imgCopy,imgBlur, i):

  _,contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  for cnt in contours:

    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
    (x,y,w,h) = cv2.boundingRect(approx)
    ar = float(w)/h
    #cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7)
    area = cv2.contourArea(cnt)
    areaMin = 2000
    if area>areaMin and area<10000 and ar>0.7 and ar<1.2:
      ROI = imgCopy[y:y+h, x:x+w]
      if (hsv(ROI))>10000:
        print(hsv(ROI))
        cv2.drawContours(imgContour, cnt, -1, (255,0,255), 7)
        cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 5)
        cv2.imwrite("{}.png".format(i+1), ROI)
        i+=1
    #elif area>areaMin and area<13000 and ar<2:
     # cv2.rectangle(imgContour, (x,y), (x+w, y+h), (255,0,0), 5)
      #print(ar)
  return i

class image_converter:

  def __init__(self,I):
    rospy.init_node('image_converter', anonymous=False)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/mybot/camera1/image_raw",Image,self.callback)
    self.image=None
    self.i=I
  def callback(self,data):
    try:
      self.image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      imgContour = self.image.copy()
      imgCopy = self.image.copy()
      imgBlur = cv2.GaussianBlur(self.image, (7,7), 1)
      imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
      smooth = scipy.ndimage.median_filter(imgGray, size=2)
      #ret,thresh = cv2.threshold(smooth,100,255,cv2.THRESH_BINARY)
      threshold1 = 227
      threshold2 = 50
      imgCanny = cv2.Canny(smooth, threshold1, threshold2)
      lines = cv2.HoughLines(imgCanny, 1, np.pi/180, 150)
      kernel = np.ones((5,5))
      imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
      self.i = getContours(imgDil, imgContour, imgCopy,imgBlur, self.i)
      cv2.imshow("Result", imgContour)
      cv2.waitKey(3)

    except CvBridgeError as e:
      print(e)

    #(rows,cols,channels) = self.image.shape
    #if cols > 60 and rows > 60 :
    #  cv2.circle(self.image, (50,50), 10, 255)

    #cv2.imshow("Image window", self.image)
    #os.system('roslaunch mybot_gazebo mybot_trigger2.launch')

def main(args):
  try:
    while not rospy.is_shutdown():
      i=0
      ic=image_converter(i)
      rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
