#! /usr/bin/env python3
"""
    This enables the turtle in turtlesim to move in a square path (closed-loop control).
"""

from math import atan2, sqrt

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def update_pose(data):
    """
        Periodically update the pose of the turtle.
    """
    # TODO: Need to work on localizing the pose variables.
    global x_pos
    global y_pos
    global ang

    x_pos = data.x
    y_pos = data.y
    ang = data.theta

def square_closedloop():
    """
        Move the turtle in a square loop.
    """
    # TODO: Need to work on localizing the pose variables.
    global x_pos
    global y_pos
    global ang

    x_pos = 0
    y_pos = 0
    ang = 0

    PI = 3.14159265359

    rospy.init_node("Turtle_closed_square",anonymous=True)
    rospy.loginfo("Turtle started running in square (closed-loop control)")
    vel_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/turtle1/pose", Pose, update_pose, queue_size=10)
    rate = rospy.Rate(5)

    cor_vel=Twist()
    rospy.loginfo("Moving from " + str(round(y_pos,2)) + "to 5.00")
    while sqrt(pow((5 - x_pos), 2) + pow((5 - y_pos), 2))!=0 and not rospy.is_shutdown():
        cor_vel.angular.z = 2*(atan2(5 - y_pos, 5 - x_pos) - ang)
        cor_vel.linear.x = max(0.1, sqrt(pow((5 - x_pos), 2) + pow((5 - y_pos), 2)))
        vel_pub.publish(cor_vel)
        rate.sleep()
        vel_pub.publish(cor_vel)
        rate.sleep()
        if sqrt(pow((5 - x_pos), 2) + pow((5 - y_pos), 2))<=0.1:
            print("Reached X-axis:", str(round(x_pos,2)), " Y-axis:", str(round(y_pos,2)))
            break

    cor_vel.linear.x = 0
    cor_vel.angular.z = 0.5
    vel_pub.publish(cor_vel)
    while not rospy.is_shutdown():
        vel_pub.publish(cor_vel)
        if ang>-0.02:
            break

    lin_vel=Twist()
    ang_vel=Twist()
    hor_pos=1
    hor_neg=0
    ver_pos=0
    ver_neg=0

    while not rospy.is_shutdown():
        if hor_pos==1:
            lin_vel.linear.x = max(0.2,8-x_pos)
            vel_pub.publish(lin_vel)
            if x_pos>=8:
                print("Reached X-axis:", str(round(x_pos,2)), " Y-axis:", str(round(y_pos,2)))
                while ang<PI/2 and not rospy.is_shutdown():
                    ang_vel.angular.z = max(0.1,PI/2-ang)
                    vel_pub.publish(ang_vel)
                    rate.sleep()
                hor_pos=0
                ver_pos=1

        if ver_pos==1:
            lin_vel.linear.x = max(0.2,8-y_pos)
            vel_pub.publish(lin_vel)
            if y_pos>=8:
                print("Reached X-axis:", str(round(x_pos,2)), " Y-axis:", str(round(y_pos,2)))
                while 0<ang<PI and not rospy.is_shutdown():
                    ang_vel.angular.z = max(0.1,PI-ang)
                    vel_pub.publish(ang_vel)
                    rate.sleep()
                hor_neg=1
                ver_pos=0

        if hor_neg==1:
            lin_vel.linear.x = max(0.2,x_pos-5)
            vel_pub.publish(lin_vel)
            if x_pos<=5:
                print("Reached X-axis:", str(round(x_pos,2)), " Y-axis:", str(round(y_pos,2)))
                ang_vel.angular.z = 0.5
                vel_pub.publish(ang_vel)
                while ang<-1.58 and not rospy.is_shutdown():
                    ang_vel.angular.z = max(0.1, abs(ang+PI/2))
                    vel_pub.publish(ang_vel)
                    rate.sleep()
                hor_neg=0
                ver_neg=1

        if ver_neg==1:
            lin_vel.linear.x = max(0.2,y_pos-5)
            vel_pub.publish(lin_vel)
            if y_pos<=5:
                print("Reached X-axis:", str(round(x_pos,2)), " Y-axis:", str(round(y_pos,2)))
                print("Completed square loop")
                break
        rate.sleep()

if __name__=="__main__":
    try:
        square_closedloop()
    except rospy.ROSInterruptException:
        pass
