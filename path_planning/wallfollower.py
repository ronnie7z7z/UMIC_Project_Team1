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
from orient import Orient
#the bot moves along the wall with the wall on the left
class WallFollower():
	def __init__(self):
		rospy.init_node('wall_follower',anonymous=True)
		self.x=None
		self.y=None
		self.sub1=rospy.Subscriber("/mybot/amcl/amcl_pose",PoseWithCovarianceStamped,self.cb)
		self.sub=rospy.Subscriber("/mybot/laser/scan",LaserScan,self.callback)
		self.finish=False
		self.exit=None #a two-tuple to hold coordinates of a potential exit point
        self.exitrange=None #the distance from the potential exit point

	def cb(self,data):
		self.x=data.pose.pose.position.x
		self.y=data.pose.pose.position.y

	def callback(self,msg):
		i=int(-msg.angle_min/msg.angle_increment)#the index of ranges of the point directly ahead
		x=msg.ranges[i]-self.x #coordinates of the point directly ahead wrt map frame
		y=-self.y #the y coordinate of the point straight ahead in bot frame is 0
		max_range=max(msg.ranges)
		ma=msg.angle_min+msg.ranges.index(max_range)*msg.angle_increment#angle along which maximum range occurs
        if ma<0:#this corresponds to the exit only if it lies on the wall, i.e., to the left
        	self.exit=(max_range*math.cos(ma)-self.x,msg.-max_range*math.sin(ma)+self.y)#potential exit point
        	self.exitrange=max_range #range of the potential exit point

		ac = actionlib.SimpleActionClient("move_base", MoveBaseAction) #these few lines of code have been copied as is
		#define a client for to send goal requests to the move_base server through a SimpleActionClient
		while not ac.wait_for_server(rospy.Duration.from_sec(5.0)):
		   rospy.loginfo("Waiting for the move_base action server to come up") #wait for the action server to come up
		goal=MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position =  Point(x-0.05,y,0)
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		goal.target_pose.pose.orientation.z = 0.0
		goal.target_pose.pose.orientation.w = 1.0
		#rospy.loginfo("Sending goal location ...")
		ac.send_goal(goal)
		ac.wait_for_result(rospy.Duration(60))
		if(ac.get_state() ==  GoalStatus.SUCCEEDED):
			self.finish=True#done following this wall

			
if __name__ == '__main__':
    try:
        WallFollower()
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("wall follower node terminated.")