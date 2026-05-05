# TurtleBot4 — Navigation Guide (ROS 2 Jazzy + Gazebo + Nav2)

Autonomous Mobile Robots Course  
Exercise 2 — Autonomous Navigation with TurtleBot4

This guide covers how to run the full autonomous navigation stack for the
TurtleBot4 in simulation: Gazebo, AMCL localization, Nav2, and RViz2.

It uses the map generated in Exercise 1 (`maze_class7_map`).

---

## Exercise 2 — Running Navigation (5 Terminals)

Open 5 terminals. In each one, source the environment first:

```bash
cd ~/turtlebot4_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

---

### Terminal 1 — Gazebo Simulation

```bash
ros2 launch turtlebot4_gz_bringup turtlebot4_gz.launch.py
```

Launches: Gazebo Harmonic, TurtleBot4 robot, maze world, ROS↔Gazebo bridge, sensors, odometry.

Wait until Gazebo opens and the robot appears. Click **Play** in Gazebo.

---

### Terminal 2 — LiDAR Bridge (required)

```bash
ros2 run ros_gz_bridge parameter_bridge \
  /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan
```

> **Why this is needed:** the default `ros_gz_bridge.launch.py` maps the LiDAR
> using a full Gazebo path (`/world/{world}/model/{robot}/link/...`) with a
> remapping to `/scan`. For the `maze_class7` world this remapping fails and
> `/scan` never appears in ROS 2. This manual bridge publishes directly to
> `/scan`, which Nav2 requires. Without this step the robot will not move.

---

### Terminal 3 — Localization (AMCL + map server)

```bash
ros2 launch turtlebot4_navigation localization.launch.py \
  map:=/home/prof-cristiano/turtlebot4_ws/install/turtlebot4_navigation/share/turtlebot4_navigation/maps/maze_class7_map.yaml \
  use_sim_time:=true
```

Launches: `map_server`, `amcl`, localization lifecycle manager.

---

### Terminal 4 — Nav2 (navigation brain)

```bash
ros2 launch turtlebot4_navigation nav2.launch.py use_sim_time:=true
```

Launches: controller server, planner server, behavior server, BT navigator,
waypoint follower, velocity smoother, global costmap, local costmap.

---

### Terminal 5 — RViz2 (visualization)

```bash
ros2 launch turtlebot4_viz view_navigation.launch.py use_sim_time:=true
```

Launches RViz2 with the TurtleBot4 navigation configuration.

---

## Sending Navigation Goals in RViz2

After all 5 terminals are running:

1. In RViz2, set **Fixed Frame** to `map`
2. Confirm the maze map is visible and the robot model appears
3. Click **2D Pose Estimate** → click and drag on the map to set the robot's initial position and orientation (match what you see in Gazebo)
4. Wait ~3 seconds for AMCL particles to converge
5. Click **Nav2 Goal** → click and drag on a corridor in the map to send a navigation goal
6. The robot will plan a path (green line) and move autonomously toward the goal
7. Repeat from step 5 to send additional goals

> Watch the **local costmap** (colored square around the robot) update in
> real time as the robot moves through the maze.

---

## Terminal Summary

| Terminal | Function                      |
| -------- | ----------------------------- |
| 1        | Gazebo simulation             |
| 2        | LiDAR sensor bridge (`/scan`) |
| 3        | AMCL localization + map       |
| 4        | Nav2 navigation stack         |
| 5        | RViz2 visualization           |

---

## Nav2 Parameter Changes and Justification

File: `src/turtlebot4/turtlebot4_navigation/config/nav2.yaml`

### Parameter — `vx_max` (MPPI Controller)

Section: `controller_server > FollowPath`

|          | Value      |
| -------- | ---------- |
| Original | `0.22 m/s` |
| Modified | `0.31 m/s` |

`vx_max` sets the upper bound of linear velocity that the MPPI Controller
samples when generating candidate trajectories. The default `0.22 m/s` is the
nominal safe speed of the TurtleBot4, but the hardware supports up to `0.31 m/s`.
Raising this limit allows the controller to select faster trajectories on long
straight corridors, reducing total navigation time. The effect is directly
observable: the robot accelerates on open stretches and slows down near curves,
driven by the `PathAngleCritic` cost combined with the new velocity ceiling.


---

