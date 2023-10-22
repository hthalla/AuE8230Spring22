## Turtlesim Control

Package Name: turtlesim_control <br>
ROS Version: Noetic <br>

This package contains three routines performed on the turtle in Turtlesim Simulation.

### How to Run
Clone the repository.
```
$ catkin_make
```

### Please follow the below steps to run the simulations
1. Launch files have been created for all three scripts (circle.py, square_openloop.py, square_closedloop.py) by the names circle.launch, square_openloop.launch, square_closedloop.launch respectively.
2. Go to the AuE8230Spring22_Prasanna_Gupta directory and launch the respective launch files present in the turtlesim_control package.
3. The demonstration videos have also been saved in the videos folder present in turtlesim_control.

### Working of circle script:
1. This script just publishes the cmd_vel both linear and angular velocities through out the execution time with no feedback.
2. To launch this node, run the following command
```
$ roslaunch turtlesim_control circle.launch
```

### Working of square_openloop script:
1. This script also just publishes the cmd_vel but at the same time keeps track of time to for rotating the turtle at the corners of the square.
2. As the linear velocity is given as 0.2, the code waits for 10 secs from the start to end of any side and then initializes the rotate command to rotate 90 deg before starting along perpendicular side.
3. To launch this node, run the following command
```
$ roslaunch turtlesim_control square_openloop.launch
```

### Working of square_closedloop script:
1. This script alongwith publishing the cmd_vel also keeps track of its current pose (x, y, theta) for velocity control based on the distance to the target. 
2. For getting the pose of the turtle in the real time an additional thread has been created using multithreading and this constantly updates the pose details of the turtle.
3. To launch this node, run the following command
```
$ roslaunch turtlesim_control square_closedloop.launch
```