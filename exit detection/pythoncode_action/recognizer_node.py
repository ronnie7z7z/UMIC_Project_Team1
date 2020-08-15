#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import os
import time

#id for the exit photo when training is 3,say
#id for a template of frame is 4, say

class Recognizer():
	def __init__(self):
		self.x=None
		self.y=None
		rospy.init_node('recognizer',anonymous=True)
		self.sub=rospy.Subscriber("/objects", 1, self.callback)

	def callback(self,msg):
		id=msg.data[0]
		if id==3:
			time.sleep(10.0)
                        os.system('rosnode kill /video_record_camera1')
			os.system('rosnode kill /explore')
		else:
			print('exit not reached yet')

if __name__=='__main__':
	try:
		r=Recognizer()
		rospy.spin()
	except rospy.ROSInterruptException:
		print('recognizer node terminated')
