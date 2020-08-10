#!/usr/bin/env python
import rospy
import tf
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
#the code assumes that during one callback execution, only one message is sent by the topic subscribed to 
class Orient(): # this class if implemented tries to make the bot align starting angle of laser i.e.,-90 deg, perpendicular to the wall
  def __init__(self,i):
    rospy.init_node('orient', anonymous=True)
    #Creating cmd_pub Publisher that will publish a Twist msg to cmd_vel
    self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=50)
    #Creating a Subscriber that will call laser_scan_callback every Laser Scan
    self.laser_sub = rospy.Subscriber("/mybot/laser/scan", LaserScan, self.laser_scan_callback(i))
    self.wall=False # a parameter to ascertain whether or not the object was a wall
  def laser_scan_callback(self, msg,i):
    if i==0:
      start=msg.angle_min
      #starting angle of laser
      desired_start=start+msg.ranges.index(min(msg.ranges))*msg.angle_increment #the angle of point of min distance from the wall
      self.rotate(desired_start-start)
    elif i==1:
        if abs(msg.ranges.index(min(msg.ranges))*msg.angle_increment-(math.pi/2))<=0.001 and abs(min(msg.ranges)-0.05)<=0.01:
          #if the next obstacle is right in front and very close -- that's probably the next wall else, the previous wall wasnt one at all
          self.wall=True
          self.rotate(0) #align along the next wall

  def rotate(self,angle):
    t0 = rospy.Time.now().to_sec()
    current_angle = 0
    cmd0=Twist()
    if angle>=0:
      cmd0.angular.z=-0.1
      while(current_angle < (angle+(math.pi/2))):
        self.cmd_pub.publish(cmd0)
        t1 = rospy.Time.now().to_sec()
        current_angle = 0.1*(t1-t0)

if __name__ == '__main__':
    try:
        o=Orient(i=0)
        O=Orient(i=1)
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("orient node terminated.")