# LARM-Max-Fab
This branch of our Git repository corresponds to our work for the Challenge 1.  
  
The specifications were :  
	1) The robot is positioned somewhere in a closed area (i.e. an area bounded with obstacles).  
	2) The robot moves continuously in this area by avoiding the obstacles (i.e. area limits and some obstacles randomly set in the area).
	3) The robot trajectory would permit the robot to explore the overall area. In other words, the robot will go everywhere (i.e. the probability that the robot
      will reach a specific reachable position in the area is equal to 1 at infinity times).  
        
        
To complete those specifications, we created the "grp-jaune" file which contains the "launch" and "scripts" files.  
The "scripts" file contains Python scripts that determines the Turtlebot's reaction when faced to an obstacle.  
The launch files allows the node to start.
