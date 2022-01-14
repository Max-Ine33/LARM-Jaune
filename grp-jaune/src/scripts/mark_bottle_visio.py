#!/usr/bin/python3

from itertools import starmap
import rospy
import numpy as np
import cv2
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Twist, Point, PointStamped
from sensor_msgs.msg import PointCloud, LaserScan, Image, CameraInfo
from cv_bridge import CvBridge
from kobuki_msgs.msg import Led
import image_geometry

# Initialize ROS::node
rospy.init_node('visio_cam', anonymous=True)

bridge = CvBridge()
object_cascade = cv2.CascadeClassifier("/home/bot/catkin_ws/src/LARM-Jaune/grp-jaune/src/data/cascade.xml")

def perception_img(data):
    print("perception data start !")
    img = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    object = object_cascade.detectMultiScale(gray, 1.4, 20)
    for (x, y, w, h) in object:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #print("img =", img)
    cv2.imshow("img", img)
    cv2.waitKey(1)
    print("==================")
    print("perception data finish !")
    

sub = rospy.Subscriber("/camera/color/image_raw", Image, perception_img)
    
    
print("Start mark_bottle_visio.py")
print("==================")
rospy.spin()




# spin() enter the program in a infinite loop
print("Start mark_bottle.py")
