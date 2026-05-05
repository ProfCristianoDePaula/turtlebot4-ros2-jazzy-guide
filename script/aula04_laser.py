#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class LaserReader(Node):

    def __init__(self):
        super().__init__('obstacle_check_node')

        self.subscription = self.create_subscription(LaserScan,'/scan', self.callback_laser, 10)

        self.get_logger().info("Nó de leitura do LiDAR iniciado")

    def callback_laser(self, msg):
        laser = msg.ranges

        # função auxiliar para evitar erro de índice
        def get_range(deg):
            index = int(deg / 360.0 * len(laser))
            if index >= len(laser):
                index = len(laser) - 1
            return laser[index]

        self.get_logger().info(f"0°   = {get_range(0):.2f}")
        self.get_logger().info(f"45°  = {get_range(45):.2f}")
        self.get_logger().info(f"90°  = {get_range(90):.2f}")
        self.get_logger().info(f"135° = {get_range(135):.2f}")
        self.get_logger().info(f"180° = {get_range(180):.2f}")
        self.get_logger().info(f"225° = {get_range(225):.2f}")
        self.get_logger().info(f"270° = {get_range(270):.2f}")
        self.get_logger().info(f"315° = {get_range(315):.2f}")

        self.get_logger().info("-------------------------")


def main():
    rclpy.init()
    node = LaserReader()
    rclpy.spin(node)


if __name__ == '__main__':
    main()
