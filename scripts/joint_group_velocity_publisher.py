#!/usr/bin/env python3
#Librerias de ROS2
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
#Librerias de Python
import math

class JointGroupVelocityPublisher(Node):
    def __init__(self):
        super().__init__('joint_group_velocity_publisher')

        self.joint_group_velocity_publisher = self.create_publisher(
             Float64MultiArray, 
             "/joint_group_velocity_controller/commands", 
             10
        )
        
        # Velocidad angular en °/seg
        self.current_velocity_in_degrees = 30 

        # Velocidades angulares en las ruedas
        self.joint_group_velocity_msg = Float64MultiArray() # Debe ser en rad/seg

        self.joint_group_velocity_timer = self.create_timer(0.1, self.publish_velocity_in_joint_group)
    
    def publish_velocity_in_joint_group(self):
        # Convertir velocidades angulares de °/seg a rad/seg
        self.current_velocity_in_radians = math.radians(self.current_velocity_in_degrees)

        # Definir las velocidades angulares en las ruedas
        self.joint_group_velocity_msg.data = [
            self.current_velocity_in_radians, # Left Wheel Joint en rad/seg
            self.current_velocity_in_radians # Right Wheel Joint en rad/seg
        ]

        # Publicar velocidad angular de las ruedas
        self.joint_group_velocity_publisher.publish(self.joint_group_velocity_msg)

        # Imprimir velocidad angular de las ruedas
        print("\nJoint Group's Angular Velocity in Degrees:")
        print(f"Left Wheel Joint: {self.current_velocity_in_degrees} °/s ")
        print(f"Right Wheel Joint: {self.current_velocity_in_degrees} °/s ")

def main(args=None):
    rclpy.init(args=args)
    joint_group_velocity_publisher_node = JointGroupVelocityPublisher()
    try:
        rclpy.spin(joint_group_velocity_publisher_node)
    except KeyboardInterrupt:
        joint_group_velocity_publisher_node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()