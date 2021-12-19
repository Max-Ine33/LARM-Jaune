# LARM-Max-Fab
This branch of our Git repository corresponds to our work for the Challenge 1.  
  
## What is the context?
The specifications were :  
1. The robot is positioned somewhere in a closed area (i.e. an area bounded with obstacles).  
2. The robot moves continuously in this area by avoiding the obstacles (i.e. area limits and some obstacles randomly set in the area).
3. The robot trajectory would permit the robot to explore the overall area. In other words, the robot will go everywhere (i.e. the probability that the robot
      will reach a specific reachable position in the area is equal to 1 at infinity times).  
        
## What is in the branch?
To complete those specifications, we created the "grp-jaune" file which contains the "launch" and "scripts" files.  

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
