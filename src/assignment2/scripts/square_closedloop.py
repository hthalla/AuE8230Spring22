#! /usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import threading
import time
from math import atan2, pow, sqrt

def update_pose(data):
    global x
    global y
    global ang

    x = data.x
    y = data.y
    ang = data.theta

def run_pose():
    while not rospy.is_shutdown():
        rospy.Subscriber("/turtle1/pose", Pose, update_pose)
        time.sleep(0.1)

def square_closedloop():
    global x
    global y
    global ang

    rospy.init_node("Turtle_closed_square",anonymous=True)
    vel_pub = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)
    rospy.loginfo("Turtle started running in square (closed-loop control)")

    cor_vel=Twist()
    rospy.loginfo("Moving from " + str(round(y,2)) + "to 5.00")
    while sqrt(pow((5 - x), 2) + pow((5 - y), 2))!=0 and not rospy.is_shutdown():
        cor_vel.angular.z = 2*(atan2(5 - y, 5 - x) - ang)
        cor_vel.linear.x = max(0.1, sqrt(pow((5 - x), 2) + pow((5 - y), 2)))
        vel_pub.publish(cor_vel)
        time.sleep(0.5)
        vel_pub.publish(cor_vel)
        time.sleep(0.5)
        if sqrt(pow((5 - x), 2) + pow((5 - y), 2))<=0.1:
            print("Reached X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))
            break

    cor_vel.linear.x = 0
    cor_vel.angular.z = 0.5
    vel_pub.publish(cor_vel)
    time.sleep(1)
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
        #print("X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))
        if hor_pos==1:        
            lin_vel.linear.x = max(0.2,8-x)
            vel_pub.publish(lin_vel)
            time.sleep(0.5)
            if x>=8:          
                print("Reached X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))
                while ang<1.57 and not rospy.is_shutdown():
                    ang_vel.angular.z = max(0.1,1.57-ang)
                    vel_pub.publish(ang_vel)
                    time.sleep(0.5)
                hor_pos=0
                ver_pos=1
                    
        if ver_pos==1:
            lin_vel.linear.x = max(0.2,8-y)
            vel_pub.publish(lin_vel)
            time.sleep(0.5)
            if y>=8:               
                print("Reached X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))
                while ang<3.14 and not rospy.is_shutdown() and ang>0:
                    ang_vel.angular.z = max(0.1,3.14-ang)
                    vel_pub.publish(ang_vel)   
                    time.sleep(0.5)
                hor_neg=1
                ver_pos=0
                
        if hor_neg==1:        
            lin_vel.linear.x = max(0.2,x-5)
            vel_pub.publish(lin_vel)
            time.sleep(0.5)
            if x<=5:         
                print("Reached X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))   
                ang_vel.angular.z = 0.5
                vel_pub.publish(ang_vel)
                time.sleep(0.5)
                while ang<-1.58 and not rospy.is_shutdown():
                    ang_vel.angular.z = max(0.1, abs(ang+1.57)) 
                    vel_pub.publish(ang_vel)
                    time.sleep(0.1)
                hor_neg=0
                ver_neg=1
                
        if ver_neg==1:
            lin_vel.linear.x = max(0.2,y-5)
            vel_pub.publish(lin_vel)
            time.sleep(0.5)
            if y<=5:          
                print("Reached X-axis:", str(round(x,2)), " Y-axis:", str(round(y,2)))
                print("Completed square loop")
                break
                    

if __name__=="__main__":
    try:
        x=0
        y=0
        a=threading.Thread(target=run_pose)
        a.start()
        square_closedloop()
    except rospy.ROSInterruptException:
        a.join()
        pass

