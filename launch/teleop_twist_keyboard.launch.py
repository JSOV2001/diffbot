from ament_index_python import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch import LaunchDescription

pkg_path = get_package_share_directory("diffbot")
diff_drive_controller_launch_filepath = os.path.join(pkg_path, "launch", "diff_drive_controller.launch.py")

def generate_launch_description():
    diff_drive_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([diff_drive_controller_launch_filepath])
    )

    teleop_twist_keyboard_node = Node(
        package="teleop_twist_keyboard",
        executable="teleop_twist_keyboard",
        name="teleop_twist_keyboard",
        prefix="xterm -e",
        output="screen",
        emulate_tty=True,
        arguments=[("__log_level:=debug")]
    )

    teleop_twist_publisher_node = Node(
        package="diffbot",
        executable="teleop_twist_publisher.py",
        output='screen',
        emulate_tty=True,
        arguments=[('__log_level:=debug')]
    )

    nodes_to_run = [
        diff_drive_controller_launch, 
        teleop_twist_keyboard_node, 
        teleop_twist_publisher_node
    ]
    return LaunchDescription(nodes_to_run)
