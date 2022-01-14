#!/usr/bin/python3

from itertools import starmap
import rospy
import numpy as np
import cv2
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Twist, Point, PointStamped
from sensor_msgs.msg import PointCloud, LaserScan, Image, CameraInfo
from cv_bridge import CvBridge
import image_geometry

# Initialize ROS::node
rospy.init_node('visio_cam', anonymous=True)


# Déclaration variables
depth = 0
cam_info = CameraInfo()
count_bottle = 0

bridge = CvBridge()
object_cascade = cv2.CascadeClassifier("/home/fabien.plouvier/UV-LARM/Github/catkin-ws/src/LARM-Jaune/grp-jaune/src/data/cascade.xml")

pub_bottle = rospy.Publisher('/bottle', Marker, queue_size=10)

def perception_color(data):
    #print("perception data start !")
    img = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    object = object_cascade.detectMultiScale(gray, 1.8, 22)
    dist = 0
    for (x, y, w, h) in object:
    	cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    	dist = calcul_distance(x, y, w, h)
    	point = calculer_point_central(x, y, w, h, dist)
    	function_pub_bottle(point)
    cv2.imshow("img", img)
    cv2.waitKey(1)
    if dist !=0:
    	print("Objet détecté à ", dist, "mètres\n")
    #print("==================")
    #print("perception data finish !")
    
    
    
def perception_depth(data):
    global depth
    depth = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    #cv2.imshow("depth", depth)
    #cv2.waitKey(33)
    
    
def perception_caminfo(data):
    global cam_info
    cam_info = data
    
    
        
def calcul_distance(x, y, w, h):
    centre_depth = depth[y+h//4:y+3*h//4, x+w//4:x+3*w//4] # récupérer centre du rectangle de détection
    dist = np.median(centre_depth) # prendre la médiane de ce rectangle permet de ne pas être affecté par les valeurs extremes comme l'arrière plan
    return dist / 1000 # convertir les mm en m
    
def calculer_point_central(x, y, w, h, dist):
    cam_model = image_geometry.PinholeCameraModel()
    cam_model.fromCameraInfo(cam_info)
    ray = np.array(cam_model.projectPixelTo3dRay((x+w//2, y+h//2))) # transformer les coordonnées du pixel central en un point dans le repère de la caméra (à une distance de 1)
    point = ray * (dist + 0.022) # on multiplie donc par la distance mesurée par la caméra à laquelle on ajoute environ la moitié du diamètre de la bouteille
    return point
    
    
def function_pub_bottle(point):
    global count_bottle
    marker = Marker()
    #marker.point.x, marker.point.y, marker.point.z = point
    #marker.header.stamp=rospy.Time.now()
    marker.header.frame_id = 'map'
    marker.header.stamp = rospy.Time.now()
    marker.ns = "bottle"
    marker.id = count_bottle
    marker.type = 1
    marker.action = 0
    marker.pose.position.x, marker.pose.position.y, marker.pose.position.z = point
    marker.pose.orientation.x, marker.pose.orientation.y, marker.pose.orientation.z = point #[0,0,0,1]
    marker.scale.x, marker.scale.y, marker.scale.z = [0.1, 0.1, 0.1]
    marker.color.r, marker.color.g, marker.color.b, marker.color.a = [0, 255, 0, 255]
    marker.lifetime = rospy.Duration(0)
    pub_bottle.publish(marker)
    count_bottle += 1

   
sub_depth = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, perception_depth)
sub_color = rospy.Subscriber("/camera/color/image_raw", Image, perception_color)
sub_cam = rospy.Subscriber("/camera/color/camera_info", CameraInfo, perception_caminfo)
    
print("Start mark_bottle_visio.py\n")

#print("==================")

# spin() enter the program in a infinite loop
rospy.spin()






