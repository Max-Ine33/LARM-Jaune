#!/usr/bin/python3


#On précise les imports
import math, rospy, time
from geometry_msgs.msg import Twist
from std_msgs.msg import String


#On déclare les constantes
VITESSE_ANGULAIRE = 0.2   #Cela représente la vitesse de rotation du robot sur lui même
VITESSE_LINEAIRE = 0.3     #Cela représente la vitesse du robot lorsqu'il va droit devant lui
DEBUG_MODE = rospy.get_param("/DEBUG_MODE")


#On déclare les variables
#commandPublisher = 0


#Fonction pour afficher des informations de débogages
def debug(info, param, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Action":
            print("[ACTION] : ", info, param)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)
    
    
#On se met sur écoute du topic utilisé par le laser

    


#On réalise les actions en fonction des données reçues
def move_command(data):
    cmd = Twist()
    if data.data == "TournerGauche":
    	vitesse = setVitesseAng(0.0)
    	debug("Je tourne sens trigo à une vitesse de ", -vitesse, "Action")
    	cmd.angular.z = -vitesse
        #time.sleep(2000)
    elif data.data == "TournerDroite":
    	vitesse = setVitesseAng(0.0)
    	debug("Je tourne sens horaire à une vitesse de ", vitesse, "Action")
    	cmd.angular.z = VITESSE_ANGULAIRE
    else:
    	vitesse = setVitesseAcc(0.0)
    	debug("Je vais tout droit à une vitesse de ", vitesse, "Action")
    	cmd.linear.x = vitesse
    commandPublisher.publish(cmd)
    

def setVitesseAng(i):
    while i <= VITESSE_ANGULAIRE:
        i = i + 0.05
    return i
    
def setVitesseAcc(i):
    while i <= VITESSE_LINEAIRE:
        i = i + 0.05
    return i
    
#Au démarrage du script, on execute la fonction principale
if __name__ == '__main__':
    debug("Lancement du script move_bot.py", "", "Debut")
    #global commandPublisher
    rospy.init_node('move', anonymous=True)
    commandPublisher = rospy.Publisher('/cmd_vel_mux/input/navi',Twist, queue_size=10)
    rospy.Subscriber('/PresenceObs', String, move_command)
    rospy.spin()
       
