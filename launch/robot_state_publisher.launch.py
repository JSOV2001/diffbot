from ament_index_python import get_package_share_directory
import os
import xacro
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

pkg_path = get_package_share_directory("diffbot")
xacro_filepath = os.path.join(pkg_path, "description", "diffbot.urdf.xacro")
robot_description_config = xacro.process_file(xacro_filepath)

use_sim_time = LaunchConfiguration('use_sim_time')

def generate_launch_description():
    use_sim_time_declaration = DeclareLaunchArgument(
        'use_sim_time', 
        default_value= 'true', 
        description= 'Use sim time if true'
    )

    rsp_node = Node(
        package= "robot_state_publisher",
        executable= "robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description_config.toxml(),
                'use_sim_time': use_sim_time
            }
        ]
    )

    nodes_to_run = [use_sim_time_declaration, rsp_node]
    return LaunchDescription(nodes_to_run)