#!/usr/bin/env python3  
import roslib
# roslib.load_manifest('learning_tf')
import rospy
import math
import tf
import turtlesim.srv
from geometry_msgs.msg import Twist
from move_robot import MoveTurtlebot3
from apriltag_ros.msg import AprilTagDetectionArray

def clip(val, mx, mn=None):
    if mn == None:
        return max(-mx, min(val, mx))
    return max(mn, min(val, mx))

at_x = 0
at_z = 0
def april_tag_callback(data):
    if len(data.detections) > 0:
        # do something
        global at_x
        global at_z
        at_x = data.detections[0].pose.pose.pose.position.x
        at_z = data.detections[0].pose.pose.pose.position.z
        # print(f"{at_x=}\t{at_z=}")
    else:
        at_x = 0.5
        at_z = distance_target

if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')
    rate = rospy.Rate(10.0)

    # moveTurtlebot3_object = MoveTurtlebot3()
    mv_objevt = rospy.Publisher('/cmd_vel', Twist)
    april_tag_sub = rospy.Subscriber("/tag_detections", AprilTagDetectionArray, april_tag_callback)
    
    while not rospy.is_shutdown():
        
        # define slope and limits of speed
        v_max = 0.15
        v_mul = 1
        a_max = 0.45
        a_mul = 2.5
        distance_target = 0.5
        
        # define and calculate message
        cmd = Twist()
        cmd.linear.x = clip((at_z-distance_target)*v_mul, v_max)
        cmd.angular.z = clip(-at_x*a_mul, a_max)

        print(f"{cmd.linear.x=}\t{cmd.angular.z=}")
        # Make it start turning
        # moveTurtlebot3_object.move_robot(cmd)
        mv_objevt.publish(cmd)

        # shut up to hear
        rate.sleep()

