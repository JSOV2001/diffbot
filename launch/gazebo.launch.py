from ament_index_python import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch import LaunchDescription

pkg_filepath = os.path.join(get_package_share_directory("diffbot"))
rsp_launch_filepath = os.path.join(pkg_filepath, "launch", "robot_state_publisher.launch.py")

def generate_launch_description():
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([rsp_launch_filepath]),
        launch_arguments= {
            'use_sim_time': 'true'
        }.items()
    )

    gazebo_cmd = ExecuteProcess(
        cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_init.so", "-s", "libgazebo_ros_factory.so"]
    )

    gazebo_spawn_node = Node(
        package= "gazebo_ros",
        executable= "spawn_entity.py",
        arguments= ["-topic", "robot_description", "-entity", "diffbot"]
    )

    nodes_to_run = [rsp_launch, gazebo_cmd, gazebo_spawn_node]
    return LaunchDescription(nodes_to_run)