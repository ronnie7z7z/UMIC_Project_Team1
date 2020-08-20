#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
PI = 3.1415926535897

def move(speed, distance, isForward = True):
    
    rospy.init_node('MazeSolverNode', anonymous = True)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
       
    #Checking if the movement is forward or backwards
    if(isForward):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0
    
    
        #Setting the current time for distance calculus
    t0 = float(rospy.Time.now().to_sec())
    current_distance = 0

        #Loop to move the turtle in an specified distance
    while(current_distance < distance):
            
         velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
         t1=float(rospy.Time.now().to_sec())
            
         current_distance= speed*(t1-t0)
            
        #After the loop, stops the robot
    vel_msg.linear.x = 0
    velocity_publisher.publish(vel_msg)

def rotate(angle, speed, clockwise = False):

    #Starts a new node
    rospy.init_node('MazeSolverNode', anonymous = True)
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Converting from angles to radians
    angular_speed = speed*2*PI/360
    relative_angle = angle*2*PI/360

    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
 
    if clockwise:
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)
    
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)


    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

if __name__ == '__main__':

    try:
    	move(0.5,5)
    	rotate(90,0.3)
    	  
    	  
    except rospy.ROSInterruptException:
        pass
