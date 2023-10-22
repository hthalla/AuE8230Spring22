#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from math import pi
from turtlesim.msg import Pose
from sensor_msgs.msg import LaserScan

dist = 1
class TurtleBot:
    
    def callback(msg):
        global dist
        dist = min(msg.ranges)
    
    # Initialize a node
    rospy.init_node('tb_controller', anonymous=True)

    # Publish velocity and subscribe to the 'scan' topic.
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 10)
    pose_subscriber = rospy.Subscriber('scan', LaserScan, callback)

    # Define variables for publishing
    rate = rospy.Rate(10)
    vel_msg = Twist()  

    while dist > 0.5: # Condition for moving forward given no near obstacle.
        vel_msg.linear.x = 0.2
        velocity_publisher.publish(vel_msg)
        rate.sleep()
    
    vel_msg.linear.x = 0 # Emergency break when distance measured is less than 0.5
    velocity_publisher.publish(vel_msg) 
    rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
    except rospy.ROSInterruptException:
        pass
