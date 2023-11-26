#!/usr/bin/env python3
#Librerias de ROS2
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopTwistPublisher(Node):
    def __init__(self):
        super().__init__('teleop_twist_publisher')

        self.teleop_twist_keyboard_subscriber = self.create_subscription(
            Twist, # Mensaje de los comandos de velocidad del teclado
            "/cmd_vel", # Topic de los comandos de velocidad del teclado
            self.teleop_twist_callback,
            10
        )

        self.diff_drive_publisher = self.create_publisher(
             Twist, # Mensaje del controlador Diff Drive Controller del robot
             "/diff_drive_controller/cmd_vel_unstamped", # Topic del controlador Diff Drive Controller del robot
             10
        )
        
        self.twist_msg = Twist()
    
    # Suscribir a los comandos de velocidad del teclado. 
    def teleop_twist_callback(self, twist_msg):
        # (Paso opcional) Asignar comandos de velocidad del teclado a un atributo del nodo
        self.twist_msg.linear.x = twist_msg.linear.x
        self.twist_msg.linear.y = twist_msg.linear.y
        self.twist_msg.linear.z = twist_msg.linear.z
        self.twist_msg.angular.x = twist_msg.angular.x
        self.twist_msg.angular.y = twist_msg.angular.y
        self.twist_msg.angular.z = twist_msg.angular.z

        # Publicar comandos de velocidad del teclado en el controlador del robot
        self.diff_drive_publisher.publish(self.twist_msg)

        # Imprimir comandos de velocidad del teclado
        print("\nDiffbot's Velocity:")
        print("Linear Velocity:")
        print(f"x: {round(twist_msg.linear.x, 2)} m/s") #Solo importa velocidad lineal en x
        print("Angular Velocity:")
        print(f"z: {round(twist_msg.angular.z, 2)} rad/s") #Solo importa velocidad angular en z

def main(args=None):
    rclpy.init(args=args)
    teleop_twist_publisher_node = TeleopTwistPublisher()
    try:
        rclpy.spin(teleop_twist_publisher_node)
    except KeyboardInterrupt:
        teleop_twist_publisher_node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()