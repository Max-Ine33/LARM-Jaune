#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist

rospy.init_node('node_move', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def move_command(data):
    move = Twist()
    #rate = rospy.Rate(1)
    pub.publish(move)
    
# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()
       
