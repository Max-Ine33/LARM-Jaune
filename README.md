# General information
- **UV** : LARM
- **Group** : grp-jaune
- **Name** : Fabien Plouvier and Maxine Gravier
- **Date** : 13/12/2021 -> 19/01/2022 

📌This directory corresponds to the work done for our Software and Automation for Mobile Robotics course.
  
# What is the context?

## The specifications

🛠️The main objectives of the project were :  

- Control a robot in a cluttered environment
- Map a static environment
- Detect all the Nuka-Cola cans
- Estimate the position of all the Nuka-Cola in the map
- Optimize the exploration strategy

The Nuka-Cola can:  
![Nuka-Cola](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRIKP7d5HF9AlhLNM-LgxfoMV8zhmg5SxJi6w&usqp=CAU)
## The tools available

Our project is based on the programming of the robot [TurtleBot](http://kobuki.yujinrobot.com/about2/).  
**The TurtleBot :**   

![TurtleBot](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1TD8glNSh65AcX9a84uFww1x6CdrCJkrCD7lUaYKr3D4Yco7dwe-8W9_fKuY3FR89DNk&usqp=CAU)

This robot allows the connection of an external computer, as well as additional sensors (such as a [Laser](https://www.roscomponents.com/en/lidar-laser-scanner/87-ust-30lx.html), or an [Intel RealSense](https://www.intel.fr/content/www/fr/fr/architecture-and-technology/realsense-overview.html) camera)

To develop programs on this robot, we used the [Robot Operating System (ROS)](https://www.ros.org/). It has powerful tools for the implementation of robotic projects, and it is open source.

# The organisation

Each week corresponds to a challenge to be achieved.  

**Challenge 1 :**  
The goal is to demonstrate the capability of a robot to move in a cluttered environment and potentially to visit all a closed area.  

**Challenge 2 :**  
The goal is to demonstrate the capability the robot has to map an environment and to retrieve specific objects on it.

**Challenge 3 :**  
The goal is to demonstrate the capability the robot has to explore autonomously an unknown environment and to retrieve specific objects on it.  


The challenges have their own git branches, to access them, do : 
```git
git checkout branchname //for example : challenge2 or challenge3
```