#!/usr/bin/python3


#On précise les imports
import math, rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String


#On déclare les constantes
VITESSE_ANGULAIRE = 0.5    #Cela représente la vitesse de rotation du robot sur lui même
VITESSE_LINEAIRE = 0.8     #Cela représente la vitesse du robot lorsqu'il va droit devant lui
DEBUG_MODE = False


#On déclare les variables
commandPublisher = 0


#Fonction pour afficher des informations de débogages
def debug(info, param, type_debug):
    if type_debug == "Action":
        print("[ACTION] : ", info, param)
    elif type_debug == "Debut":
        print("\n\n[INITIALISATION] : ", info)
    
    
#On se met sur écoute du topic utilisé par le laser
def move():
    global commandPublisher
    rospy.init_node('move', anonymous=True)
    commandPublisher = rospy.Publisher('/cmd_vel',Twist, queue_size=10)
    rospy.Subscriber('/PresenceObs', String, move_command)
    rospy.spin()


#On réalise les actions en fonction des données reçues
def move_command(data):
    global debugMode
    cmd = Twist()
    if data.data == "TournerGauche":
        if DEBUG_MODE:
            debug("Je tourne à gauche à une vitesse de ", -VITESSE_ANGULAIRE, "Action")
        cmd.angular.z = -VITESSE_ANGULAIRE
    elif data.data == "TournerDroite":
        if DEBUG_MODE:
            debug("Je tourne à droite à une vitesse de ", VITESSE_ANGULAIRE, "Action")
        cmd.angular.z = VITESSE_ANGULAIRE
    else:
        if DEBUG_MODE:
            debug("Je vais tout droit à une vitesse de ", VITESSE_LINEAIRE, "Action")
        cmd.linear.x = VITESSE_LINEAIRE
    commandPublisher.publish(cmd)
    
    
#Au démarrage du script, on execute la fonction principale
if __name__ == '__main__':
    if DEBUG_MODE:
        debug("Lancement du script move_sim.py", "Debut")
    move()
       
