#!/usr/bin/python3

import rospy, rospkg
import numpy as np
import cv2, tf
import image_geometry
import time
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Twist, Point, PointStamped
from sensor_msgs.msg import PointCloud, LaserScan, Image, CameraInfo
from cv_bridge import CvBridge



################################################## 
############  PARTIE INITIALISATION ############## 
################################################## 

# Déclaration constantes
DEBUG_MODE = False                                           #Un mode debug plus "propre" que le ros log mais avec moins de détails
AFFICHAGE_VIDEO = False                                      #On veut afficher la vidéo ?
ECART_MAX_ENTRE_BOUTEILLE = 0.2                            #L'ecart min pour traduire comme nouvelle bouteille
MARQUEUR_SCALE = [0.1, 0.1, 0.1]                            #Différent paramètres pour la création de marqueur
MARQUEUR_COLOR = [0, 255, 0, 255]                           #Comme la couleur vert
MARQUEUR_TYPE = 1

rospack = rospkg.RosPack()                                  #Ce qui suit sert juste à localiser le fichier cascade.xml
path_pkg = rospack.get_path('grp-jaune')
object_cascade = cv2.CascadeClassifier(path_pkg + "/src/data/cascade.xml")



# Initialisation ROS::node
rospy.init_node('challenge2', anonymous=True)



# Déclaration variables
cam_info = CameraInfo()
tfListener = tf.TransformListener()
bridge = CvBridge()
points_list = []
depth = 0
nombre_bouteille = 0



#Fonction pour afficher des informations de débogages
def debug(info, type_debug):
    global DEBUG_MODE
    if DEBUG_MODE:
        if type_debug == "Alerte":
            print("[ALERTE] : ", info)
        elif type_debug == "Info":
            print("[INFO] : ", info)
        elif type_debug == "Debut":
            print("\n\n[INITIALISATION] : ", info)       



################################################## 
###############  PARTIE PERCEPTION ############### 
################################################## 

def perception_color(data):
    # @Paramètre : données recu par le topic /camera/color/image_raw
    # @Valeur retournée : Aucune, on encode puis converti les données à chaque appel, on fait tous les calculs ensuite
    
    global points_list, objet_precedent, init
    debug("Detection de couleurs.", "Info")
    img = bridge.imgmsg_to_cv2(data, desired_encoding='bgr8')                     #On encode les données reçues au format voulu (ici BGR) et on les convertis
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    object = object_cascade.detectMultiScale(gray, 1.5, 25)                       #On lance la detection d'objet via le fichier cascade.xml
    for (x, y, w, h) in object:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)                    #Si on reconnait des objets, on les entoure d'un rectangle rouge
        distance_en_metres = calcul_distance_en_metres(x, y, w, h)                #Appel de la fonction du calcul de distance
        point = calcul_point_central(x, y, w, h, distance_en_metres)              #Appel de la fonction du calcul du point central du rectangle dans le plan de la caméra
        if not check_proximite(point, points_list):                               #Appel de la fonction de vérification si le point n'a pas déjà été détecté
            points_list.append(creer_point_vers_map(point))                       #On place le nouveau point dans le repère de la "map"
            function_pub_bouteille(point)                                         #Appel de la fonction publier bouteille pour mettre le marker
            if DEBUG_MODE:
                print("Objet détecté à ", distance_en_metres, "mètres\n")
    if AFFICHAGE_VIDEO:                                                           #Pour un affichage video de la camera
        cv2.imshow("img", img)
        cv2.waitKey(1)
    


def perception_depth(data):
    # @Paramètre : données recu par le topic /camera/aligned_depth_to_color/image_raw
    # @Valeur retournée : Aucune, on encode puis converti les données à chaque appel

    global depth
    depth = bridge.imgmsg_to_cv2(data, desired_encoding='passthrough')
    


def perception_camera_info(data):
    # @Paramètre : données recu par le topic /camera/color/camera_info
    # @Valeur retournée : Aucune, on stocke la valeur globalement pour l'utiliser dans la fonction calcul_point_central()

    global cam_info
    cam_info = data
    
    

################################################## 
################  PARTIE CALCUL ################## 
################################################## 

def creer_point_vers_map(point_to_map):
    # @Paramètre : le point dans le repère de la caméra
    # @Valeur retournée : le point dans le repère "map"

    pointSt = PointStamped()
    pointSt.header.frame_id = "camera_color_optical_frame"
    pointSt.point.x, pointSt.point.y, pointSt.point.z = point_to_map                    #Les coordonnées du point sont désormais dans le repère "map"
    return tfListener.transformPoint("map", pointSt)



def calcul_distance_en_metres(x, y, w, h):
    # @Paramètres : coordonnées de l'objet reconnu par les rectangles rouges
    # @Valeur retournée : la distance entre l'objet et la caméra 


    centre_rectangle = depth[y+h//4:y+3*h//4, x+w//4:x+3*w//4]                          #On récupere le centre du rectangle rouge (sur la base de 1/4, 3/4) en prenant la valeur arrondi à l'inférieur (d'où le ..//4 et non /4)
    distance_en_mm = np.median(centre_rectangle)                                        #Pour limiter des valeurs en dehors de l'objet (un mur loin), on prends la médiane du rectangle
    return distance_en_mm / 1000                                                        #La distance étant en milimètres, on travaille en mètres
    


def calcul_point_central(x, y, w, h, distance_en_metres):
    # @Paramètres : coordonnées de l'objet reconnu par les rectangles rouges et de la distance en mètres
    # @Valeur retournée : le point central dans le repère de la caméra (après on le mettra par rapport au repère "map")

    cam_model = image_geometry.PinholeCameraModel()                                     #Les trois lignes suivantes nous permettent de connaître la relation entre
    cam_model.fromCameraInfo(cam_info)                                                  #le point dans l'espace et sa projection dans le repère de la caméra
    vector = np.array(cam_model.projectPixelTo3dRay((x+w//2, y+h//2)))                  #plus d'infos sur la docs : http://docs.ros.org/en/kinetic/api/image_geometry/html/python/index.html, (inspiré d'exemples)
    point = vector * ( distance_en_metres + 0.021)                                      #Le point se situe à une certaine distance de la caméra, en prenant aussi en considération le "milieu interieur" de la bouteille, la valeur 0.021 a été mesuré à la main
    return point



def check_proximite(nv_point, points_list):
    # @Paramètres : le point détecté et la liste des points déjà détectés
    # @Valeur retournée : booléen, vrai si le point a été trouvé avant, faux sinon

    for pt in points_list:
        diff_x = abs(nv_point[1] - pt.point.x)                                                 #On calcul la différence (en absolue) de la valeurs de x,y,z des points                                              
        diff_y = abs(nv_point[2] - pt.point.y)
        if diff_x <= ECART_MAX_ENTRE_BOUTEILLE or diff_y <= ECART_MAX_ENTRE_BOUTEILLE:         #Si elle est supérieur au seuil, on prend en compte comme nouvelle bouteille sinon non
            debug("\n\n\nbouteille proche", "Alerte")
            return True
        else:
            return False
		


################################################## 
############### PARTIE PUBLICATION ############### 
################################################## 

def function_pub_bouteille(point):
    # @Paramètre : le point dans le repère "map"
    # @Valeur retournée : Aucune, on créer un marqueur et on publie dans le topic bottle

    global nombre_bouteille
    marker = Marker()
    marker.header.frame_id = 'camera_color_optical_frame'
    marker.header.stamp = rospy.Time.now()
    marker.ns = "bottle"
    marker.id = nombre_bouteille
    marker.type = MARQUEUR_TYPE
    marker.action = 0
    marker.scale.x, marker.scale.y, marker.scale.z = MARQUEUR_SCALE
    marker.color.r, marker.color.g, marker.color.b, marker.color.a = MARQUEUR_COLOR
    marker.pose.position.x, marker.pose.position.y, marker.pose.position.z = point
    marker.pose.orientation.x, marker.pose.orientation.y, marker.pose.orientation.z = point
    marker.lifetime = rospy.Duration(0)
    pub_bottle.publish(marker)                                                              #Après avoir mis le marqueur, on publie dans le topic bottle
    nombre_bouteille += 1

   
    
debug("\n\n------- Fichier challenge2.py du grp-jaune lancé -------\n\n", "Debut")
pub_bottle = rospy.Publisher('/bottle', Marker, queue_size=10)

sub_depth = rospy.Subscriber("/camera/aligned_depth_to_color/image_raw", Image, perception_depth)
sub_color = rospy.Subscriber("/camera/color/image_raw", Image, perception_color)
sub_cam = rospy.Subscriber("/camera/color/camera_info", CameraInfo, perception_camera_info)
#print("==================")

# spin() pour être dans une boucle infinie
rospy.spin()

