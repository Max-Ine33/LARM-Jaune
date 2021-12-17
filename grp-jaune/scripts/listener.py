#!/usr/bin/python3
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

# Initialize ROS::node
rospy.init_node('move', anonymous=True)

commandPublisher = rospy.Publisher(
    '/cmd_vel',
    Twist, queue_size=10
)
obstacles= []
angle = 0
# Publish velocity commandes:
def move_command(data):
    global commandPubisher
    global obstacles
    # Compute cmd_vel here and publish... (do not forget to reduce timer duration)
    #zone devant : [xdébut, xfin],[ydébut, yfin]
    cmd= Twist()
    obstacle_devant = False
    obstacle_gauche = False
    zone_devant = [[-0.2, 0.2],[0.1, 0.3]]
    zone_gauche = [[-1.0, -0.2],[-0.2, 0.2]]
    for p in obstacles[0:]:
        px = round(p[0],2)
        py = round(p[1],2)
        if py > zone_devant[1][0] and py < zone_devant[1][1]:
            if px > zone_devant[0][0] and px < zone_devant[0][1]:
                obstacle_devant = True
        if py > zone_gauche[1][0] and py < zone_gauche[1][1]:
            if px > zone_gauche[0][0] and px < zone_gauche[0][1]:
                obstacle_gauche = True

    if obstacle_devant == True and obstacle_gauche == False:
        print("\nobstacle devant, je tourne à droite")
        cmd.linear.x= 0.0
        cmd.angular.z = -0.5
        #cmd.linear.x= 1.0
    elif obstacle_devant == True and obstacle_gauche == True:
        print("\nobstacle gauche")
        cmd.linear.x= 0.0
    else:
        print("\nj'avance")
        cmd.linear.x= 1.0
           
                
    
    
    commandPublisher.publish(cmd)

# Publish velocity commandes:
def interpret_scan(data):
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
    

# connect to the topic:
rospy.Subscriber('/base_scan', LaserScan, interpret_scan)

# call the move_command at a regular frequency:
rospy.Timer( rospy.Duration(0.1), move_command, oneshot=False )
# spin() enter the program in a infinite loop
print("Start move.py")
rospy.spin()

