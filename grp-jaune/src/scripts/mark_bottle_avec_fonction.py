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
rospy.init_node('training', anonymous=True)

# chemin = rospy.__path__  #+ "src/scripts/cascade.xml"
# print(chemin)
img = np.array([[200, 33, 213]], np.uint8)
bridge = CvBridge()
object_cascade = cv2.CascadeClassifier("chemin_fichier_xml")
cam_info = CameraInfo()
depth = 0
stamp=0
nb_detections = 0
count_bouteille = 0

publisher_led = rospy.Publisher('/mobile_base/commands/led1', Led, queue_size=10)
publisher_bouteilles = rospy.Publisher('/bottle', Marker, queue_size=10)

def perception_img(data):
    global stamp
    stamp = data.header.stamp
    img = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    object = object_cascade.detectMultiScale(gray, 1.2, minNeighbors=3)
    for (x, y, w, h) in object:
        cv2.rectangle(img, (x, y), (x+w, y+h), 255, 0, 0), 2)
        dist = trouver_distance(x, y, w, h)
        point = calculer_point_central(x, y, w, h, dist)
        print(x, y, w, h, dist, point)
        publier_bouteille(point)
    print("==================")
    gerer_led(len(object))

    

    #cv2.imshow("img", img)
    #cv2.waitKey(33)


depth = 0


def perception_depth(data):
    global depth
    depth = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    #cv2.imshow("depth", depth)
    #cv2.waitKey(33)

def perception_caminfo(data):
    global cam_info
    cam_info = data


listener_img = rospy.Subscriber("/camera/color/image_raw", Image, perception_img)
listener_depth = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, perception_depth)
listener_cam_info = rospy.Subscriber("/camera/color/camera_info", CameraInfo, perception_caminfo)


def trouver_distance(x, y, w, h):
    centre_depth = depth[y+h//4:y+3*h//4, x+w//4:x+3*w//4] # récupérer centre du rectangle de détection
    dist = np.median(centre_depth) # prendre la médiane de ce rectangle permet de ne pas être affecté par les valeurs extremes comme l'arrière plan
    return dist / 1000 # convertir les mm en m

def calculer_point_central(x, y, w, h, dist):
    cam_model = image_geometry.PinholeCameraModel()
    cam_model.fromCameraInfo(cam_info)
    ray = np.array(cam_model.projectPixelTo3dRay((x+w//2, y+h//2))) # transformer les coordonnées du pixel central en un point dans le repère de la caméra (à une distance de 1)
    point = ray * (dist + 0.022) # on multiplie donc par la distance mesurée par la caméra à laquelle on ajoute environ la moitié du diamètre de la bouteille
    return point

def gerer_led(nb):
    global nb_detections
    if nb_detections != nb:
        nb_detections = nb
        print(nb_detections)
        msg = Led()
        msg.value = nb_detections
        if msg.value > 3: msg.value = 3
        publisher_led.publish(msg)

def publier_bouteille(point):
    global count_bouteille
    msg = Marker()
    msg.header.frame_id = "camera_color_optical_frame"
    #msg.header.stamp = stamp
    #msg.point.x, msg.point.y, msg.point.z = point
    msg.ns = "bottle"
    msg.id = count_bouteille
    msg.type = 1
    msg.action = 0
    msg.pose.position.x, msg.pose.position.y, msg.pose.position.z = point
    msg.scale.x, msg.scale.y, msg.scale.z = [0.1, 0.1, 0.1]
    msg.color.r, msg.color.g, msg.color.b, msg.color.a = [0, 255, 0, 255]
    msg.lifetime.secs, msg.lifetime.nsecs = [2, 0]
    publisher_bouteilles.publish(msg)
    count_bouteille += 1

# spin() enter the program in a infinite loop
print("Start scanop.py\n")
rospy.spin()
