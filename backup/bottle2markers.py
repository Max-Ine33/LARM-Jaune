#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from visualization_msgs.msg import Marker
from std_msgs.msg import String

#On déclare les variables
DEBUG_MODE = True

#On déclare les variables
commandPublisher = 0




#Fonction pour afficher des informations de débogages
def debug(info, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Alerte":
            print("[ALERTE] : ", info)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)
        elif type_debug == "Info":
            print("[INFO] : ", info)
   

#On initialise les markers
def initial_marker(i,x,y):
    i = 3
    x = 0
    y = 0
    global commandPublisher
    debug("Appel fonction init", "Info")
    marker = Marker()
    marker.header.stamp=rospy.Time.now()
    marker.header.frame_id = 'map'
    marker.ns= "marker"
    marker.id= i
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z=0.15
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.3
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.1
    print("marker = ", marker)
    print("command pub = ", commandPublisher)
    commandPublisher.publish(marker)
    #return marker
    
    
             
#On créer les markers
def create_marker(data):
    debug("Appel fonction create_marker", "Info")
    initial_marker(3, 0.0, 0.0)
    
   #bouteille=create_marker(i,x,y)
    
def main():
    global commandPublisher
    #On initialise notre noeud
    rospy.init_node("bottle", anonymous=True)
    commandPublisher = rospy.Publisher('/bottle', Marker, queue_size=10)
    rospy.Subscriber('/test',String, create_marker)

    rospy.spin()

if __name__ == '__main__':
    print("Start bootle2markers.py")
    main()



