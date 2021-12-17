#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String

# Initialize ROS::node
rospy.init_node('move', anonymous=True)
commandPublisher = rospy.Publisher('PresenceObs',String, queue_size=1)
            



# Publish velocity commandes:
def interpret_scan(data):
    global commandPublisher
    msg_envoi = "void"
    obstacles= []
    #print("\n\nI get scans")
    #rospy.loginfo('I get scans')
    angle= data.angle_min
    for aDistance in data.ranges :
        if 0.1 < aDistance and aDistance < 5.0 :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    #print("\n")
    """rospy.loginfo( str(
        [ [ round(p[0], 2), round(p[1], 2) ] for p in  obstacles[0:10] ] 
    ) + " ..." )"""


    for obs in obstacles:
        if(obs[0] > 0 and obs[0] < 0.2): #en X
            if(obs[1] > -0.25 and obs[1] < 0):   # en Y
                msg_envoi = "TournerDroite"
            if(obs[1] > 0 and obs[0] < 0.25):
                msg_envoi = "TournerGauche"
                
    commandPublisher.publish(msg_envoi)       
                
rospy.Subscriber('scan', LaserScan, interpret_scan)
#cmd= Twist()

print("Start listener.py")

rospy.spin()

