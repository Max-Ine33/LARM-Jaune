#!/usr/bin/python3
import math, rospy
from geometry_msgs.msg import Twist

rospy.init_node('node_move', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def move_command(data):
    move = Twist()
    #rate = rospy.Rate(1)
    move.linear.x = 1
    #move.angular.z = 1
    pub.publish(move)
    
# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()
        

"""
# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel',
    Twist, queue_size=10
)

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.linear.x= 1
    commandPublisher.publish(cmd)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()"""
