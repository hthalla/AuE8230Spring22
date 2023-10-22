#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from math import pi

class TurtleBot:
    def __init__(self):

        rospy.init_node('square_openloop', anonymous=True)

        self.velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

        self.rate = rospy.Rate(10)

    def move(self):    
        vel_msg = Twist()    

        #Since we are moving just in x-axis
        vel_msg.linear.y = 0
        vel_msg.linear.z = 0
        vel_msg.angular.x = 0
        vel_msg.angular.y = 0
        vel_msg.angular.z = 0
        
        while not rospy.is_shutdown():

            while True:

                #Setting the current time for distance calculus
                speed = 0.3
                distance = 2
                t0 = float(rospy.Time.now().to_sec())
                current_distance = 0
                vel_msg.linear.x = speed
                #Loop to move the turtle in an specified distance
                while(current_distance < distance):
                    #Publish the velocity
                    self.velocity_publisher.publish(vel_msg)
                    #Takes actual time to velocity calculus
                    t1=float(rospy.Time.now().to_sec())
                    #Calculates distancePoseStamped
                    current_distance= speed*(t1-t0)
                #After the loop, stops the robot
                vel_msg.linear.x = 0
                self.rate.sleep()

                angular_speed = 0.3
                relative_angle = pi/2
                vel_msg.angular.z = abs(float(0.3))
                 
                # Setting the current time for distance calculus
                t0 = float(rospy.Time.now().to_sec())
                current_angle=0.00
                while(current_angle < relative_angle):
                    self.velocity_publisher.publish(vel_msg)
                    t1 = rospy.Time.now().to_sec()
                    current_angle = angular_speed*(t1-t0)
                    
                #After the loop, stops the robot
                vel_msg.angular.z = 0
                self.velocity_publisher.publish(vel_msg)
                self.rate.sleep()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.move()
    except rospy.ROSInterruptException:
        pass
