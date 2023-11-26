#Librerias para Ubicar Archivos
import os
from ament_index_python import get_package_share_directory
#Librerias para Procesar Archivos
import xacro
from launch.launch_description_sources import PythonLaunchDescriptionSource
#Librerias para Lanzar Nodos
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch import LaunchDescription

pkg_share_filepath = os.path.join(get_package_share_directory("diffbot"))

gazebo_launch_filepath = os.path.join(pkg_share_filepath, "launch", "gazebo.launch.py")

urdf_filepath = os.path.join(pkg_share_filepath, "description", "diffbot.urdf.xacro")
robot_description_file = xacro.process_file(urdf_filepath)
robot_description = {"robot_description": robot_description_file.toxml()}

controller_filepath = os.path.join(pkg_share_filepath, "config", "joint_group_velocity_controller.yaml")

def generate_launch_description():
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_launch_filepath])
    )

    # ROS2 Control activado con las configuracion del YAML
    controller_manager_node = Node(
        package= "controller_manager",
        executable= "ros2_control_node",
        parameters= [robot_description, controller_filepath]
    )

    # Joint State Broadcaster activado para moverse transmitir informacion de los joints
    joint_state_broadcaster_spawner_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments= ["joint_state_broadcaster"]
    )
    
    # Joint Group Velocity Controller activado para moverse como modelo diferencial
    joint_group_velocity_spawner_node = Node(
        package="controller_manager",
        executable="spawner",
        arguments= ["joint_group_velocity_controller"]
    )

    nodes_to_run = [
        gazebo_launch, 
        controller_manager_node, 
        joint_state_broadcaster_spawner_node, 
        joint_group_velocity_spawner_node
    ]
    return LaunchDescription(nodes_to_run)