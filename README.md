# Stewart Platform (ROS 2 Lyrical Luth)

Simulating a 6-DOF Stewart platform in Gazebo Jetty (`gz-sim`) using native joint position controllers and `ros_gz_bridge` to control a closed-loop manipulator with ROS 2.

![Stewart Platform Simulation](gif/stewart.gif)

Because the Stewart platform is a closed-loop manipulator, the model description is written in SDF rather than URDF. Instead of a custom ROS 1 Gazebo Classic plugin, this ROS 2 port uses Gazebo Jetty's `JointPositionController` system plugins and `ros_gz_bridge` to expose the 6 prismatic leg commands to ROS 2.

### Prerequisites

Install `ros_gz` and `Eigen3` for ROS 2 Lyrical Luth:
* `sudo apt install ros-lyrical-ros-gz libeigen3-dev`

### Clone and Build

Clone this repository into your ROS 2 workspace `src` directory and build it with `colcon`:
* `cd ~/your_ros2_ws/src`
* `git clone https://github.com/Lkahuria/stewart-ros2.git`
* `cd ~/your_ros2_ws`
* `colcon build --packages-select stewart`
* `source install/setup.bash`

*(Note: `sdf/stewart/model.sdf` is already generated and configured for Gazebo Jetty, so you do not need to run `erb` or build the legacy `plugin/` folder).*

### Launch and Control

To launch Gazebo, the topic bridge, and the inverse kinematics (`ik`) node:
* `ros2 launch stewart stewart.launch.py`

To move the platform by publishing a target `Twist` pose (in a second sourced terminal):
* `ros2 topic pub -r 10 /stewart/platform_twist geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.35}, angular: {x: 0.15, y: -0.15, z: 0.2}}"`

**Note:** If using a DualShock 3 or 4 controller via USB (`joy_node` + `ps4_controller`), the left analog stick translates in `x` and `y`, `R2` increases `z` and `L2` decreases `z`, the right analog stick rotates around `x` and `y` (roll and pitch), and `R1`/`L1` adjust yaw.

### Credits

Ported to ROS 2 Lyrical Luth from the original ROS 1 repository by [daniel-s-ingram/stewart](https://github.com).
