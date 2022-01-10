#!/usr/bin/python3
import math, rospy
import tf
from std_msgs.msg import String
from nav_msgs.msg import Odometry

#On déclare les variables
tfListener = tf.TransformListener()

# On initialise notre noeud
rospy.init_node('move', anonymous=True)


#commandPublisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


def callback_odom(data):
	rospy.loginfo("Infos odom : %s",data.pose.pose)
	
	
def callback_tf(data):
	global tfListener
	local_goal= tfListener.transformPose("/base_footprint", data)
	rospy.loginfo("Infos tf: %s",local_goal)

# spin() enter the program in a infinite loop
print("Start move.py")
rospy.Timer(rospy.Duration(0.1), callback_tf, oneshot=False )
rospy.Subscriber('/goal',Odometry,callback_odom)
rospy.spin()
