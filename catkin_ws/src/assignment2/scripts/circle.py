#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def turtle_circle():
    rospy.init_node("circle",anonymous=True)
    rospy.loginfo("Turtle started running in circle")
    
    vel_pub =rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    
    vel = Twist()
    vel.linear.x = 1
    vel.linear.y = 0
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0
    vel.angular.z = 1
    
    while not rospy.is_shutdown():
        vel_pub.publish(vel)

if __name__=="__main__":
    try:
        turtle_circle()
    except rospy.ROSInterruptException:
        pass



