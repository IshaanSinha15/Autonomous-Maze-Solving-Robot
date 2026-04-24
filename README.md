# Autonomous Maze Solving Robot

## Introduction

### Problem Statement
Navigating a robot autonomously through a maze is a classic robotics challenge that tests perception, localization, path planning, and control. The problem involves enabling a robot to perceive its environment, build a map, and find an optimal path to the goal without human intervention.

### Importance in Robotics/Automation
Autonomous navigation is fundamental in robotics, with applications in warehouse automation, search and rescue, service robots, and more. Solving maze navigation efficiently demonstrates key concepts in SLAM (Simultaneous Localization and Mapping), autonomous decision-making, and real-time control.

### Solution Overview
This project uses a TurtleBot3 robot simulated in Gazebo, leveraging ROS2 for communication and navigation. The robot builds a map using LIDAR data, localizes itself, and solves the maze using a custom maze-solving algorithm. The system integrates mapping, localization, and navigation stacks for end-to-end autonomy.

---

## Objectives
- Develop a robot capable of autonomously solving and navigating a 2D maze.
- Demonstrate real-time mapping, localization, and path planning in a simulated environment.
- Validate the solution using ROS2 and Gazebo simulation.
- **Scope:** The project focuses on simulation (no physical hardware), using TurtleBot3, and covers mapping, localization, and navigation in a static maze.

---

## Methodology


### Algorithms
- **Mapping (SLAM):** Uses ROS2 Cartographer for real-time mapping and localization based on LIDAR data.
- **Maze Solving (A* Algorithm):** Implements the A* (A-star) search algorithm in Python (`maze_solver.py`) to find the optimal path through the maze. The robot uses sensor data and the occupancy grid to dynamically plan and follow the shortest path to the goal.
- **Navigation:** Utilizes ROS2 Navigation Stack (Nav2) for path planning and obstacle avoidance.

**Flow of Execution:**
1. Start simulation and bring up the robot in Gazebo.
2. Launch mapping and localization nodes.
3. Run the maze solver node to compute and follow the path to the goal.
4. The robot updates its position and map, replanning as needed.

**Justification:**
- The A* algorithm is widely used for pathfinding due to its efficiency and optimality in grid-based environments like mazes.
- ROS2 provides robust middleware for modular robotics development.
- Cartographer and Nav2 are standard, well-supported solutions for mapping and navigation.
- Custom maze-solving logic allows flexibility and optimization for the specific maze structure.

### Tools, Platforms, and Technologies

**Software:**
- **ROS2 Humble:** Middleware for robot communication, mapping, and navigation.
- **Python:** For scripting custom logic (e.g., maze_solver.py).
- **Gazebo:** 3D simulation environment for testing robot behavior.
- **RViz2:** Visualization tool for robot state, sensor data, and navigation.

**Hardware:**
- Simulated TurtleBot3 (no physical hardware required).

**Simulation Environments:**
- **Gazebo:** Used for simulating the robot and maze environment.

**Libraries/Frameworks:**
- **Nav2:** ROS2 Navigation Stack for path planning and control.
- **Cartographer:** For SLAM and localization.
- **OpenCV (if used):** For any image processing tasks.
- **Standard Python libraries:** For algorithm implementation.

---

## Project Structure

```
├── src/
│   └── autonomous_tb3/
│       ├── CMakeLists.txt
│       ├── package.xml
│       ├── config/
│       ├── launch/
│       ├── script/
│       │   ├── entity_spawner.py
│       │   ├── maze_solver.py
│       │   ├── occupancy_grid_pub.py
│       │   └── startup_initial_pose.py
│       └── worlds/
├── build/
├── install/
├── log/
└── Instruction.md
```

---

## How to Run the Project

1. **Open a WSL command prompt**
2. **Kill any previous ROS2, Gazebo, or RVIZ process:**
   ```bash
   pkill -9 -f 'ros2 launch autonomous_tb3' || true
   pkill -9 -f gzserver || true
   pkill -9 -f gzclient || true
   pkill -9 -f rviz2 || true
   pkill -9 -f maze_solver.py || true
   rm -rf build/ install/ log
   ```
3. **Source ROS2 Humble and build your package:**
   ```bash
   source /opt/ros/humble/setup.bash
   colcon build --packages-select autonomous_tb3
   ```
4. **Source your workspace:**
   ```bash
   source install/setup.bash
   ```
5. **Launch the simulation with GUI enabled:**
   ```bash
   ros2 launch autonomous_tb3 tb3_maze_navigation.launch.py use_gui:=true
   ```
6. **Run the maze solver node:**
   ```bash
   source install/setup.bash
   ros2 run autonomous_tb3 maze_solver.py
   ```

---

## Checking Logs

- **LIDAR Logs:**
  ```bash
  ros2 topic hz /scan
  ros2 topic echo /scan --no-arr
  ```
- **AMCL Logs:**
  ```bash
  ros2 topic echo /amcl_pose
  ```
- **Particle Cloud:**
  ```bash
  ros2 topic echo /particle_cloud
  ```

---

## References
- [ROS2 Documentation](https://docs.ros.org/en/humble/index.html)
- [TurtleBot3 Documentation](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
- [Gazebo Documentation](https://gazebosim.org/docs)

---

## Authors
- Ishaan Sinha
- Ishika Raj
- Tahir Shafiq 
- Syed Kaifuddin