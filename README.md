# General information
- **UV** : LARM
- **Group** : grp-jaune
- **Name** : Fabien Plouvier and Maxine Gravier
- **Date** : 17/01/2022 -> 19/01/2022
- **Challenge** : 3  

📌This branch of our Git repository corresponds to our work for the Challenge 3.  
  
## What is the context?
🛠️The specifications were :
(Minimal)

1. The group follows the consigns (i.e. the repository is presented as expected)
2. The robot navigate to goal position provided with rviz
3. The robot build a map in /map topic
4. The robot detects 1st-version-bottle (orange one) and publish markers in /bottle topic at the position of detected bottles.

(Optional)
1. The robot detect 2d-version-bottle (black one)
2. There is no need to publish goal positions. The robot is autonomous to achieve its mission.
3. Any suggestions provided by the group are welcome.

## What is in the branch?
To complete those specifications, we created the 📂 "grp-jaune" folder which contains the "launch", "script", "rviz" and data files

👀For a better understanding, here is the tree structure of our grp-yellow folder:
```bash
├── CMakeLists.txt
├── data
│   └── cascade.xml
├── launch
│   ├── challenge3_simulation.launch
│   └── challenge3_tbot.launch
├── package.xml
├── rviz
│   ├── challenge3_simulation.rviz
│   └── challenge3_tbot.rviz
└── scripts
    ├── robot
    │   ├── listener_tbot.py
    │   ├── move_tbot.py
    │   └── vision_bottle.py
    └── simulation
        ├── listener_sim.py
        └── move_sim.py
```
# How to install and run the scripts?
⚠️To be able to use our work correctly, please follow the steps for installing and running the files/scripts.

## Installation

1. Clone our folder in your directory:
```git
git clone https://github.com/Max-Ine33/LARM-Jaune.git
```

2. Change the current git branch to challenge3
```git
git checkout challenge3
```
*Note : The grp-yellow folder REQUIRES the [mb6-tbot](https://bitbucket.org/imt-mobisyst/AC/src/master/) package.*
*Make sure that mb6-tbot project is already installed aside*

## Running

From the catkin worskspace

1. Compile the project :
```bash
catkin_make
```

2. Source the project :
```bash
source devel/setup.bash
```

3. Launch the project :
For the **robot** :
```bash
roslaunch grp-jaune challenge3_tbot.launch
```
For the **simulation** :
```bash
roslaunch grp-jaune challenge3_simulation.launch
```

# How do the scripts work?

## Vision (Camera)
To be able to recognise the bottle as accurately as possible, we used the Haar method. It is based on the image-based learning method. One of the biggest drawbacks is the time it takes to train the model.

Here is the general idea of our project:

1. We get the data by topic (colour, depth and camera information)
2. We detect the bottles in this data
3. Calculate a central point of the bottle with the camera marker
4. Transform the coordinates into the map
5. Check if the bottle has not already been found
6. Create or not a mark and publish it in the topic bottle

## Obstacle detection (Laser)
We have opted for the use of an "intermediate" topic whose purpose is to pass information from the laser topic to the robot control topic.

Here is the general idea of this detection:
1. The front area of the robot is divided into 2 sub-areas, so the obstacles are located among the 2
2. Depending on the position of the obstacle (left or right), a message is published on an intermediate topic (like "TurnLeft" or "TurnRight").
3. Data are received by the suscriber of the intermediate topic, choices are made (turn left => speed_angular * (-1)...) 
4. Then published on the control topic of the robot.

# Optional
You have the possibility to see debug messages during the execution of the script.

1. If you want to enable the **debug mode** (simulation and robot parts):

- set the value of DEBUG_MODE_... in the launch file to ``True`` :
```xml
<param name="DEBUG_MODE_LISTENER" type="bool" value="False" />
<param name="DEBUG_MODE_MOVE" type="bool" value="False" />
<param name="DEBUG_MODE_VISION" type="bool" value="False" />
```
2. In the same way, to have **the video display** (robot part) of the camera and the object recognition by rectangle on it (using OpenCV):

- set the value of VIDEO_VIEWER_MODE in the launch file to ``True`` :
```xml
<param name="VIDEO_VIEWER_MODE" type="bool" value="False" />
```
