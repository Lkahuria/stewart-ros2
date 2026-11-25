# Stewart Platform Simulation (ROS 2 Lyrical Luth)

A 6-DOF Stewart platform simulation running on **ROS 2 Lyrical Luth** and **Gazebo Jetty (`gz-sim`)**. This repository ports the original ROS 1 implementation to `ament_cmake`, `rclcpp`, and Gazebo Jetty's native joint position controllers and `ros_gz_bridge`.
### Supported ROS 2 Versions

* **Works out of the box:** **Jazzy**, **Kilted**, **Lyrical**, and **Rolling** (tested on ROS 2 Lyrical Luth with Gazebo Jetty).

* **ROS 2 Humble:** Humble defaults to Gazebo Fortress (formerly ‘Ignition Fortress’), which uses different plugin names than `model.sdf`. Humble users must install **Gazebo Harmonic** (`ros-humble-ros-gzharmonic`) instead of the default `ros-humble-ros-gz` package.

### Prerequisites

* **For ROS 2 Jazzy, Kilted, Lyrical, or Rolling:**
  ```bash
  sudo apt install ros-\$ROS_DISTRO-ros-gz libeigen3-dev
  ```

* **For ROS 2 Humble** (using the [OSRF Gazebo repository](https://gazebosim.org/docs/latest/ros_installation/)):
  ```bash
  sudo apt install ros-humble-ros-gzharmonic libeigen3-dev
  ```
  *(Note: `ros-humble-ros-gzharmonic` conflicts with `ros-humble-ros-gz`, so remove `ros-humble-ros-gz` first if already installed).*


## Build Instructions

1. Create a ROS 2 workspace (if you don't already have one) and clone this repository into `src/`:
   ```bash
   mkdir -p ~/stewart_ws/src
   cd ~/stewart_ws/src
   git clone https://github.com/Lkahuria/stewart-ros2.git
   ```

2. Build the package with `colcon`:
   ```bash
   cd ~/stewart_ws
   colcon build --packages-select stewart
   source install/setup.bash
   ```

> **Note:** `sdf/stewart/model.sdf` is already configured with Gazebo Jetty's closed-loop joints and `JointPositionController` plugins. Do **not** regenerate it from `model.sdf.erb`.

## Running the Simulation

Launch Gazebo Jetty, the ROS-Gazebo topic bridge, and the inverse kinematics (`ik`) node:

```bash
source ~/stewart_ws/install/setup.bash
ros2 launch stewart stewart.launch.py
```

## Controlling the Platform

The `ik` node subscribes to `/stewart/platform_twist` (`geometry_msgs/msg/Twist`) and computes the 6 prismatic leg extensions:
* **`linear.x, linear.y, linear.z`**: Surge, sway, and heave translation (in meters)
* **`angular.x, angular.y, angular.z`**: Roll, pitch, and yaw rotation (in radians)

Open a second terminal, source the workspace, and publish a target pose:

* **Lift and tilt the platform:**
  ```bash
  source ~/stewart_ws/install/setup.bash
  ros2 topic pub -r 10 /stewart/platform_twist geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.35}, angular: {x: 0.15, y: -0.15, z: 0.2}}"
  ```

* **Return to level home position:**
  ```bash
  ros2 topic pub -r 10 /stewart/platform_twist geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
  ```

## Credits

Ported to ROS 2 Lyrical Luth and Gazebo Jetty from the original ROS 1 repository by [Daniel S. Ingram](https://github.com).
