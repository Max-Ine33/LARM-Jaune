#!/usr/bin/env python3

import rospy
import numpy as np
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import Marker
from std_msgs.msg import String
import math as mths


#On déclare les variables
commandPublisher = rospy.Publisher('/bottle', Marker, queue_size=10)
list_bottle=[]
x=0
y=0
i=4

#On initialise notre noeud
rospy.init_node("bottle", anonymous=True)


#Fonction pour afficher des informations de débogages
def debug(info, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Alerte":
            print("[ALERTE] : ", info)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)  
   

#On initialise les markers
def initialize_marker(i,x,y):
    marker = Marker()
    marker.header.stamp=rospy.Time.now()
    marker.header.frame_id = 'map'
    marker.ns= "marker"
    marker.id= i
    marker.type = 1
    marker.action = Marker.ADD
    marker.pose.position.x= x
    marker.pose.position.y= y
    marker.pose.position.z=0.1
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    marker.color.r = 0.0
    marker.color.g = 0.5
    marker.color.b = 0.0
    marker.color.a = 1.0
    marker.scale.x = 0.1
    marker.scale.y = 0.1
    marker.scale.z = 0.2
    return marker
    
    
             
#On créer les markers
def create_marker(data):
    global pub,x,y,i,list_bottle
    bouteille=initialize_marker(i,x,y)
    b=rdm.uniform(0,1)
    if (b<0.2):

        if not list_bottle:
            list_bottle=[[1,1], [4,4],[8,7],[16,18]]
        else:
            
            if all(( mth.sqrt((x-n[0])**2 + (y-n[1])**2))>0.1 for n in list_bottle):
                list_bottle.append([x,y])
                print(list_bottle)
            
                pub.publish(bouteille)
                i+=1
            else: 
                for a in range(0,i,1):
                    print(a,list_bottle[a][0],list_bottle[a][1])
                    if (( mth.sqrt((x-list_bottle[a][0])**2 + (y-list_bottle[a][1])**2))<0.1):
                        list_bottle[a][0]=(list_bottle[a][0]+x)/2
                        list_bottle[a][1]=(list_bottle[a][1]+y)/2
                        print(a,list_bottle[a][0],list_bottle[a][1])
                        pub.publish(initialize_marker(a,list_bottle[a][0],list_bottle[a][1]))



    x+=rdm.uniform(0,0.3)
    y+=rdm.uniform(-0.2,0.2)


rospy.Subscriber('chatter', String, create_marker)
rospy.spin()

