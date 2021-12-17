#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
import sensor_msgs.msg
from geometry_msgs.msg import Twist

def callback(msg):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    print("##############################################")
    print("Value at 0 degree:", msg.ranges[0])
    print("values at 90 degree", msg.ranges[360])
    print("values at 180 degree", msg.ranges[719])
    

    #If the distance to an obstacle in front of the robot is bigger than 1 meter, the robot will move forward
    if msg.ranges[360] < 1.0:
        print("obstacle devant")
    if msg.ranges[719] < 1.0:
        print("obstacle côté gauche")
    if msg.ranges[0] < 1.0:
        print("obstacle côté droit")
    if msg.ranges[360] > 1.0:
        print("je vais tout droit")
        move.linear.x = 1.0
        move.angular.z = 0.0
    #If the distance to an obstacle in front of the robot is smaller than 1 meter, the robot will stop
    elif msg.ranges[719] > 1.0 and msg.ranges[360] < 1.0:
        print("je vais à gauche")
        move.linear.x = -1.0
        #move.linear.z = 1.0
    else:
        move.linear.x = 0.0
        move.angular.z = 0.0

    pub.publish(move)
    
#def listener():
rospy.init_node('listener', anonymous=True)
sub = rospy.Subscriber('/base_scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.Rate(10) # 10hzrospy.init_node('listener', anonymous=True)
move = Twist()
    # spin() simply keeps python from exiting until this node is stopped
print("start listener.py")
rospy.spin()

print("start listener.py")
