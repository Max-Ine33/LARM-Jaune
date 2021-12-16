#!/usr/bin/python3
import rospy
from sensor_msgs.msg import LaserScan
import sensor_msgs.msg
from geometry_msgs.msg import Twist

def callback(msg):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
    print("##############################################")
    # values at 0 degree
    print("s2 [0]")
    print(msg.ranges[0])
    # values at 90 degree
    print("s3 [90]")
    print(msg.ranges[360])
    # values at 180 degree
    print("s4 [180]")
    print(msg.ranges[719])
    
    
    
    
    #If the distance to an obstacle in front of the robot is bigger than 1 meter, the robot will move forward
    if msg.ranges[0] > 1:
        move.linear.x = 0.5
        move.angular.z = 0.0
    #If the distance to an obstacle in front of the robot is smaller than 1 meter, the robot will stop
    else:
        move.linear.x = 0.0
        move.angular.z = 0.0

    pub.publish(move)
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, callback)
    rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Rate(10) # 10hzrospy.init_node('listener', anonymous=True)
    move = Twist()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    print("start listener.py")
    listener()
