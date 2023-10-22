#! /usr/bin/env python3

from cmath import inf
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

def update_scan(scan_data):
    global scd
    scd = scan_data.ranges

def laser_sub():
    rospy.Subscriber("/scan", LaserScan, callback=update_scan)

def bot_control():
    global scd

    rospy.init_node("control", anonymous=True)
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    rospy.sleep(1)
    msg1 = Twist()
    msg2 = Twist()
    vx = 0.25
    msg1.linear.x = vx
    ef = 0
    while not rospy.is_shutdown():
        front = np.array(scd[359:360] + scd[0:2]).mean()
        print(front)
        if front<0.75:
            rospy.loginfo("Head-on collision detected, turning in anti-clockwise direction")
            msg2.linear.x = 0
            msg2.angular.z = 0.5
            pub.publish(msg2)
            rospy.sleep(0.1)
        else:
            pub.publish(msg1)
            rospy.sleep(0.1)

            sidel = np.array(scd[5:60])
            #print(sidel)
            sider = np.array(scd[300:354])
            #print(sider)
            ei = ef
            ef = sidel[sidel<5].mean() - sider[sider<5].mean()
            
            if abs(ef)>0.1:
                rospy.loginfo("centering turtlebot")
                msg2.linear.x = vx
                msg2.angular.z = (ef)*1.5 + (ef - ei)*1
                pub.publish(msg2)
                rospy.sleep(0.1)
                sidel = np.array(scd[5:75])
                sider = np.array(scd[285:354])

if __name__ == "__main__":
    try:
        laser_sub()
        rospy.sleep(0.5)
        bot_control()
    except rospy.ROSInterruptException:
        pass



