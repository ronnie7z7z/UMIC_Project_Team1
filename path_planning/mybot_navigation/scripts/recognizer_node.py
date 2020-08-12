#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import PoseWithCovarianceStamped
from mybot_navigation.msg import status_info
#from geometry_msgs.msg import Twist

#id for the exit photo when training is 3,say
#id for a template of frame is 4, say

class Recognizer():
	def __init__(self):
		self.state=status_info()
		rospy.init_node('explorer',anonymous=True)
		self.sub2=rospy.Subscriber("/amcl_pose",PoseWithCovarianceStamped,self.cb)
		self.sub=rospy.Subscriber("/objects", 1, self.callback)
		self.pub=rospy.Publisher("/status",status_info)

	def cb(self,data):
		self.state.now=data.pose.pose.position

	def callback(self,msg):
		id=msg.data[0]
		if id==3:
			#exit point discovered
			self.state.type='exit'
		elif id==4:
			self.state.type='image'
		else:
			self.state.type='ignored'
		rospy.loginfo(self.state.type)
		self.pub.publish(self.state)

if __name__=='__main__':
	try:
		r=Recognizer()
		rospy.spin()
	except rospy.ROSInterruptException:
		print('recognizer node terminated')