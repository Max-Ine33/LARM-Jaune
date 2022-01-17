#!/usr/bin/python3


#On précise les imports
import math, rospy, math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


#On déclare les constantes
INTERVALLE_X = 0.1    #Les points qui sont étudiés se situent sur l'intervalle [0, 0.25] sur l'axe des X
INTERVALLE_Y = 0.1     #Les points qui sont étudiés se situent sur l'intervalle [0, 0.2] sur l'axe des Y
DISTANCE_SCAN_MAX = 1.5
DISTANCE_SCAN_MIN = 0.01
DEBUG_MODE = True


#On déclare les variables
commandPublisher = rospy.Publisher('/PresenceObs',String, queue_size=10)


#On initialise notre noeud
rospy.init_node('Interception', anonymous=True)


#Fonction pour afficher des informations de débogages
def debug(info, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Alerte":
            print("[ALERTE] : ", info)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)       

       
#Fonction qui détecte élèments scannés par le laser:
def interpret_scan(data):
    global commandPublisher    #on déclare les variables qui seront utilisées
    msg_envoi = "void"
    obstacles= []              #on utilise le code de conversion des données du laser en point cloud, fournit
    angle= data.angle_min
    for aDistance in data.ranges :
        if DISTANCE_SCAN_MIN < aDistance and aDistance < DISTANCE_SCAN_MAX :
            aPoint= [ 
                math.cos(angle) * aDistance, 
                math.sin( angle ) * aDistance
            ]
            obstacles.append( aPoint )
        angle+= data.angle_increment
    for obs in obstacles:
        debug("Avancer !", "Alerte")
        if(obs[0] > 0 and obs[0] < INTERVALLE_X):         #si l'obstacle à proximité se situe dans l'intervalle de l'axe X voulut
            if(obs[1] > -INTERVALLE_Y and obs[1] < 0):    #alors, on fait des tests pour savoir si l'élèment se trouve à gauche ou à droite
                debug("Obstacle à droite !", "Alerte")
                msg_envoi = "TournerDroite"               #le robot demande de changer alors de sens 
            if(obs[1] > 0 and obs[0] < INTERVALLE_Y):
                debug("Obstacle à gauche !", "Alerte")
                msg_envoi = "TournerGauche"           
    commandPublisher.publish(msg_envoi)       
                
rospy.Subscriber('/scan', LaserScan, interpret_scan)
debug("Lancement du script listener_sim.py", "Debut")
rospy.spin()

