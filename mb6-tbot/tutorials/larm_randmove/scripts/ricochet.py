#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel_mux/input/navi',
    Twist, queue_size=10
)

# Publish velocity commandes:
def move_command(data):
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    cmd= Twist()
    cmd.linear.x= 0.1
    commandPublisher.publish(cmd)

# Publish velocity commandes:
def interpret_scan(data):
    rospy.loginfo('I get scans')
    obstacles= []
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )

# connect to the topic:
rospy.Subscriber('scan', LaserScan, interpret_scan)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()
