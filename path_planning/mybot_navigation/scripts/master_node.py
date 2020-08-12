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
from mybot_navigation.msg import status_info
from std_msgs.msg import Float32MultiArray

def euclidean_distance(p1,p2):
	return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2 + (p1.z-p2.z)**2)

d=0.1#threshold distance of distinct occurence of 2 images on wall

class Master():
	def __init__(self):
		rospy.init_node('master',anonymous=True)
		self.images=0
		self.imloc=[]
		self.exit=None
		self.sub1=rospy.Subscriber("/recognizer",status_info,self.cb1)

	def cb1(self,msg):
		if msg.type=='image':
			if self.images==0:
				self.imloc.append(msg.now)
				self.images+=1
			else:
				for p in self.imloc:
					if euclidean_distance(msg.now,p)<d:
						return
				self.images+=1
				self.imloc.append(msg.now)
		elif msg.type=='exit':
			self.exit=msg.now

	def override(self):
		if self.images==5 and not(self.exit==None):
			ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
			#define a client for to send goal requests to the move_base server through a SimpleActionClient
			while not ac.wait_for_server(rospy.Duration.from_sec(5.0)):
			 rospy.loginfo("Waiting for the move_base action server to come up") #wait for the action server to come up
			goal=MoveBaseGoal()
			goal.target_pose.header.frame_id = "map"
			goal.target_pose.header.stamp = rospy.Time.now()
			goal.target_pose.pose.position =  self.exit
			goal.target_pose.pose.orientation.x = 0.0
			goal.target_pose.pose.orientation.y = 0.0
			goal.target_pose.pose.orientation.z = 0.0
			goal.target_pose.pose.orientation.w = 1.0
			rospy.loginfo("Sending goal location ...")
			ac.send_goal(goal)
			ac.wait_for_result(rospy.Duration(60))
			if ac.get_state()==GoalStatus.SUCCEEDED:
				return True
		return False

if __name__=='__main__':
	try:
		m=Master()
		if m.override():
			print('exited')
		rospy.spin()
	except rospy.ROSInterruptException:
		print('fatal error')