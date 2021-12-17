#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String

pub = 0


def debug():


def move():
    global pub

    rospy.init_node('move', anonymous=True)
    pub = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    rospy.Subscriber('PresenceObs', String, move_command)
    rospy.spin()


def move_command(data):
    cmd = Twist()
    if data.data=="TournerDroite":
        cmd.angular.z=5
    elif data.data=="TournerGauche":
        cmd.angular.z=-5
    else:
        cmd.linear.x= 1.0
    #rate = rospy.Rate(1)
    pub.publish(cmd)
    
# call the move_command at a regular frequency:
#rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )


if __name__ == '__main__':
    move()
       
