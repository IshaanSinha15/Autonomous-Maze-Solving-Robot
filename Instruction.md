Instruction to run the project 

1. Open a wsl command prompt 

Run the following command in order 


2. To kill any previous ROS2 ,Gazebo or RVIZ process:

pkill -9 -f 'ros2 launch autonomous_tb3' || true
pkill -9 -f gzserver || true
pkill -9 -f gzclient || true
pkill -9 -f rviz2 || true
pkill -9 -f maze_solver.py || true
rm -rf build/ install/ log

3. Source ROS2 Humble and build your package:

source /opt/ros/humble/setup.bash
colcon build --packages-select autonomous_tb3

4. Source your workspace:

source install/setup.bash

5. Launch the simulation with GUI enabled:

ros2 launch autonomous_tb3 tb3_maze_navigation.launch.py use_gui:=true

6. Run the maze solver node:

source install/setup.bash
ros2 run autonomous_tb3 maze_solver.py



For checking Lidar / AMCL / NAV2 logs :

1. LIDAR Logs :

ros2 topic hz /scan
ros2 topic echo /scan --no-arr

2. AMCL Logs :

ros2 topic echo /amcl_pose

3. Particle cloud:

ros2 topic echo /particle_cloud


