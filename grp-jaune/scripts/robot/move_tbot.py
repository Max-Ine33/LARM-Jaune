#!/usr/bin/python3


#On précise les imports
import math, rospy, time
from geometry_msgs.msg import Twist
from std_msgs.msg import String


#On déclare les constantes
VITESSE_ANGULAIRE = 0.2     #Cela représente la vitesse de rotation du robot sur lui même
VITESSE_LINEAIRE = 0.2      #Cela représente la vitesse du robot lorsqu'il va droit devant lui
DEBUG_MODE = rospy.get_param("/DEBUG_MODE_MOVE")

#On déclare les variables
commandPublisher = 0



#Fonction pour afficher des informations de débogages
def debug(info, param, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Action":
            print("[ACTION] : ", info, param)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)
 


#On réalise les actions en fonction des données reçues
def move_command(data):
    global commandPublisher
    cmd = Twist()
    if data.data == "TournerGauche":
        debug("Je tourne sens trigonométrque à une vitesse de ", -VITESSE_ANGULAIRE, "Action")              # L'idée est la suivante : Si on détecte un obstacle à gauche, on tourne à droite
        cmd.angular.z = -VITESSE_ANGULAIRE                                                                  # Si on détecte un obstacle à droite, on tourne à gauche, sinon on avance
    elif data.data == "TournerDroite":
        debug("Je tourne sens horaire à une vitesse de ", VITESSE_ANGULAIRE, "Action")
        cmd.angular.z = VITESSE_ANGULAIRE
    else:
        debug("Je vais tout droit à une vitesse de ", VITESSE_LINEAIRE, "Action")
        cmd.linear.x = VITESSE_LINEAIRE
    commandPublisher.publish(cmd)

  
        
#Au démarrage du script, on execute la fonction principale
if __name__ == '__main__':
    debug("\n\n------- Fichier move_tbot.py du grp-jaune lancé -------\n\n", "", "Debut")
    rospy.init_node('move', anonymous=True)
    commandPublisher = rospy.Publisher('/cmd_vel_mux/input/navi',Twist, queue_size=10)
    rospy.Subscriber('/PresenceObs', String, move_command)
    rospy.spin()
       
