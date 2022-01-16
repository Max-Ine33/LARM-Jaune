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

```bash
├── CMakeLists.txt
├── package.xml
└── src
    ├── data
    │   ├── cascade.xml
    │   └── challenge2.rviz
    ├── launch
    │   ├── challenge2.launch
    │   └── challenge2_avec_rosbag.launch
    └── scripts
        └── challenge2.py
 ```
## How to install and run the scripts?
⚠️To be able to use our work correctly, please follow the steps for installing and running the files/scripts.

### Installation
1. Clone our folder in your directory:
```git
git clone https://github.com/Max-Ine33/LARM-Jaune.git
```

2. Change the current git branch to challenge2
```git
git checkout challenge2
```
*Note :
The grp-yellow folder DOES NOT requires the mb6-tbot package.*

### Running
From the catkin worskspace

1. Compile the project :
```bash
catkin_make
```

2. Source the project :
```
source devel/setup.bash
```

3. Launch the project :
```
roslaunch grp-jaune challenge2.launch
```

## How do the scripts work?

To be able to recognise the bottle as accurately as possible, we used the Haar method.
It is based on the image-based learning method.
One of the biggest drawbacks is the time it takes to train the model.

Here is the general idea of our project:
1. We get the data by topic (colour, depth and camera information)
2. We detect the bottles in this data
3. Calculate a central point of the bottle with the camera marker
4. Transform the coordinates into the map
5. Check if the bottle has not already been found
6. Create or not a mark and publish it in the topic bottle 


## Optional
You have the possibility to see debug messages during the execution of the script.

If you want to enable this mode :
- set the value of DEBUG_MODE in the python script to True

In the same way, to have the video display of the camera and the object recognition by rectangle on it: 
- set the value of AFFICHAGE_VIDEO in the python script to True
