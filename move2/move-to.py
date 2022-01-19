#!/usr/bin/python3
import rospy
from std_msgs.msg import String

tfListener = tf.TransformListener()
            
def callback(goal):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", goal.goal)
    
def subscriber():
    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber("base_scan", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    subscriber()
