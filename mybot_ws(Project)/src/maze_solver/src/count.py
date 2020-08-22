#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg):
    print 'Value at the back'
    print msg.ranges[0]
    print 'Value at the left'
    print msg.ranges[180]
    print 'Value at the front'
    print msg.ranges[360]

rospy.init_node('Scan_values')
sub = rospy.Subscriber('/mybot/laser/scan',LaserScan,callback)
rospy.spin()