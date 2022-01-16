# General information
- **UV** : LARM
- **Group** : grp-jaune
- **Name** : Fabien Plouvier and Maxine Gravier
- **Date** : 03/01/2022 -> 14/01/2022
- **Challenge** : 2  

📌This branch of our Git repository corresponds to our work for the Challenge 2.  
  
## What is the context?
🛠️The specifications were :  
(Minimal)  
1. The group follows the consigns (i.e. the repository is presented as expected)  
2. The robot build a map in /map topic
3. The robot detect 1st-version-bottle (orange one) and publish markers /bottle topic at the position of the robot.  

(Optional)  
1. Information is returned to rviz (started automaticaly, with appropriate configuration).  
2. The map is good shapped even in large environement.  
3. The robot detect 2d-version-bottle (black one). 
4. The position of bottle in the map is precise.  
5. The position of the bottle is streamed one and only one time in the /bottle topic.  
6. All the bottle are detected (wathever the bottle position and the background).  
7. Only the bottle are detected (even if similar object are in the environment).  
8. A service permit to get all bottle positions. 

## What is in the branch?
To complete those specifications, we created the 📂 "grp-jaune" folder which contains the "launch", "script" and data files

👀For a better understanding, here is the tree structure of our grp-yellow folder:
