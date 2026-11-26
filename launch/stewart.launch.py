import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_stewart = get_package_share_directory('stewart')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    sdf_file = os.path.join(pkg_stewart, 'sdf', 'stewart', 'model.sdf')
    world_file = os.path.join(pkg_stewart, 'world', 'stewart_world.sdf')

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    spawn_stewart = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-file', sdf_file, '-name', 'stewart', '-z', '0.1'],
        output='screen',
    )

    bridge_args = [
        f'/stewart/piston{i}_cmd@std_msgs/msg/Float64]gz.msgs.Double'
        for i in range(1, 7)
    ]

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=bridge_args,
        output='screen',
    )

    ik_node = Node(
        package='stewart',
        executable='ik.py',
        output='screen',
    )

    return LaunchDescription([
        gz_sim,
        spawn_stewart,
        bridge,
        ik_node,
    ])
