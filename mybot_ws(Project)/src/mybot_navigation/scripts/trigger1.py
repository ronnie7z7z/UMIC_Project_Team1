#! /usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray,String
import os
import time

#id for the exit photo when training is 3,say
#id for a template of frame is 4, say

class Recognizer():
	def __init__(self):
		rospy.init_node('recognizer',anonymous=True)
		self.sub=rospy.Subscriber("/objects",Float32MultiArray, self.callback)
		self.pub=rospy.Publisher("validity_of_detection",String,queue_size=10)
		self.maze='no'
		self.exit='no'

	def callback(self,msg):
		if msg.data==[]:
			print('yet to detect')
			return
		else:
			id=msg.data[0]

			#trigger 1 : start of maze
			if id==3:
				time.sleep(10.0)
				if self.maze=='no':
					print("approaching maze")
					os.system('rosnode kill /slam_gmapping /amcl /image_converter')
					os.system('rosnode kill /explore /move_base /gmapping_node ')
					os.system('roslaunch  maze_solver start_maze.launch')
					os.system('python passcode_generator.py')
				self.maze='yes'

			elif id==4:
				if self.maze=='no':
					pub.publish('invalid exit')
				else:
					self.exit='yes'
					os.system('python trigger2.py')
					pub.publish('exit')
			else:
				print('maze not reached yet')

if __name__=='__main__':
	try:
		r=Recognizer()
		rospy.spin()
	except rospy.ROSInterruptException:
		print('recognizer node terminated')
