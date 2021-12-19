# General information
- **UV** : LARM
- **Group** : grp-jaune
- **Name** : Fabien Plouvier and Maxine Gravier
- **Date** : 13/12/2021 -> 19/12/2021
- **Challenge** : 1  

📌This branch of our Git repository corresponds to our work for the Challenge 1.  
  
## What is the context?
🛠️The specifications were :  
1. The robot is positioned somewhere in a closed area (i.e. an area bounded with obstacles).  
2. The robot moves continuously in this area by avoiding the obstacles (i.e. area limits and some obstacles randomly set in the area).
3. The robot trajectory would permit the robot to explore the overall area. In other words, the robot will go everywhere (i.e. the probability that the robot
      will reach a specific reachable position in the area is equal to 1 at infinity times).  
        
## What is in the branch?
To complete those specifications, we created the 📂 **"grp-jaune" folder** which contains the "launch" and "scripts" files.  
The behavior is **split into 2 nodes** (obstacle detection, and move).

👀For a better understanding, here is **the tree structure** of our grp-yellow folder:  
```bash
├── CMakeLists.txt
├── launch                               #The launch files allows the node to start.
│   ├── challendge1_simulation.launch    #For the simulation
│   └── challendge1_turtlebot.launch     #For the turtlebot
├── package.xml
└── scripts                              #The "scripts" folder contains Python scripts that determines the Turtlebot's reaction when faced to an obstacle.  
    ├── script_simulation                #For the simulation
    │   ├── listener_sim.py
    │   └── move_sim.py
    └── script_turtlebot                 #For the turtlebot
        ├── listener_bot.py
        └── move_bot.py
```

## How to install and run the scripts?
⚠️To be able to use our work correctly, please follow the steps for **installing** and **running** the files/scripts.

### Installation
1. Clone our folder in your directory: 
```git
git clone https://github.com/Max-Ine33/LARM-Jaune.git
```

2. Change the current git branch to challenge1
```git
git checkout challenge1
```

*Note :  
The grp-yellow folder requires the [mb6-tbot](https://bitbucket.org/imt-mobisyst/AC/src/master/) package.  
It is already on the challenge1 branch. Make sure it is installed correctly after cloning.* 

### Running
From the catkin worskspace  
1. Compile the project :
```Bash
catkin_make
```

2. Source the project :
```Bash
source devel/setup.bash
```

3. Launch the simulation :  
```Bash
roslaunch grp-jaune challenge1_simulation.launch
```

4. Launch the Turtlebot demonstration :  
```Bash
roslaunch grp-jaune challenge1_turtlebot.launch
```
