#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import time

def square_openloop():
    rospy.init_node("square_openloop", anonymous=True)
    rospy.loginfo("Turtle started running in square (open-loop control)")
    vel_pub=rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    
    lin_vel=Twist()
    lin_vel.linear.x = 0.2
    ang_vel=Twist()
    ang_vel.angular.z = 0.2

    lin = 1
    st=time.time()

    while not rospy.is_shutdown():
        if lin==1:        
            vel_pub.publish(lin_vel)
            if time.time()-st>=10:                
                lin=0
                st=time.time()
        if lin==0:
            vel_pub.publish(ang_vel)
            if time.time()-st>=7.82:
                lin=1
                st=time.time()

if __name__=="__main__":
    try:
        square_openloop()
    except rospy.ROSInterruptException:
        pass