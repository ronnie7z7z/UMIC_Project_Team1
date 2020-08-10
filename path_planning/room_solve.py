#! /usr/bin/env python
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import math
import random
import time
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist,PoseWithCovarianceStamped
from sensor_msgs.msg import LaserScan
from wallfollower import WallFollower
from orient import Orient
#http://edu.gaitech.hk/turtlebot/map-navigation.html
#http://docs.ros.org/melodic/api/sensor_msgs/html/msg/LaserScan.html
class Explorer():
  def __init__(self):
    self.x=None
    self.y=None
    rospy.init_node('explorer',anonymous=True)
    self.sub1=rospy.Subscriber("/mybot/amcl/amcl_pose",PoseWithCovarianceStamped,self.cb) #to find position of bot wrt map frame
    self.sub2=rospy.Subscriber("/mybot/laser/scan",LaserScan,self.callback)

  def cb(self,data):
    self.x=data.pose.pose.position.x
    self.y=data.pose.pose.position.y

  def callback(self,data):
    try:
      #code to convert laser scan to action
      start=data.angle_min
      end=data.angle_max
      inc=data.angle_increment
      ranges=data.ranges
      max_range=max(data.ranges)
      i=ranges.index(max_range)
      angle=start+i*inc #angle along which max distance is encountered
      x=max_range*math.cos(angle)-0.05-self.x #coordinates of the point to which the bot must move to be
      y=-max_range*math.sin(angle)-0.05+self.y # close to the farthest point 
      if moveto(x,y):
        exits=[] 
        #list of potential exit points
        r=[] 
        #list of squared distances from the origin(assumed center of room) of the potential exit points
        o=Orient(i=0)
        #this is to make sure the bot is aligned along the wall
        w=WallFollower()
        #follow along once aligned and simultaneously try to find exit; the camera publishes automatically the side view
        if not w.exit is None:
          r.append(w.exit[0]**2+w.exit[1]**2)
          exits.append(w.exit)
          o=Orient(1)
          #once an edge is traversed the next turn decides whether or not this is actually a wall
          if o.wall==False:
            print('not a wall, explore more')
          else:
            for i in range(3):
              w=WallFollower()
              # travel along each of the walls
              o=Orient(1)
              #orient bot after each wall is traversed
              if w.exit is None:
                continue
              r.append(w.exit[0]**2+w.exit[1]**2)
              exits.append(w.exit)
              if i==2 and len(exits)<1:
                i=0
                #repeat the round if no potential exits found even after one round
              found_exit=exits[r.index(max(r))]#the exit has to be the point whose range extends outside the room -- max radius from origin
              moveto(found_exit[0],found_exit[1])
                  
    except:
      print('error with the callback or the data, do rostopic echo to verify')

  def moveto(x,y): #copied
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
      #define a client for to send goal requests to the move_base server through a SimpleActionClient
    while not ac.wait_for_server(rospy.Duration.from_sec(5.0)):
      rospy.loginfo("Waiting for the move_base action server to come up") #wait for the action server to come up
    goal=MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position =  Point(x,y,0)
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0
    rospy.loginfo("Sending goal location ...")
    ac.send_goal(goal)
    ac.wait_for_result(rospy.Duration(60))
    if ac.get_state()==GoalStatus.SUCCEEDED:
      rospy.loginfo("found potential wall") #succeeded in reaching farthest obstacle which could be the wall, obstacle or exit
      return True

if __name__ == '__main__':
    try:
        e=Explorer()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("explorer node terminated.")