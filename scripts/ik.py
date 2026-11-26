#!/usr/bin/env python3
import math
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class IKNode(Node):
    def __init__(self):
        super().__init__('ik')
        self.z_home = 2.125
        self.nominal_length = 1.9291198

        # Base anchor coordinates (6x4 homogeneous)
        self.b = np.array([
            [-0.101,  0.800,  0.25, 1.0],
            [ 0.101,  0.800,  0.25, 1.0],
            [ 0.743, -0.313,  0.25, 1.0],
            [ 0.642, -0.487,  0.25, 1.0],
            [-0.643, -0.486,  0.25, 1.0],
            [-0.744, -0.311,  0.25, 1.0],
        ])

        # Platform anchor coordinates (6x4 homogeneous)
        self.p = np.array([
            [-0.642,  0.487, -0.05, 1.0],
            [ 0.642,  0.487, -0.05, 1.0],
            [ 0.743,  0.313, -0.05, 1.0],
            [ 0.101, -0.800, -0.05, 1.0],
            [-0.101, -0.800, -0.05, 1.0],
            [-0.743,  0.313, -0.05, 1.0],
        ])

        self.pubs = [
            self.create_publisher(Float64, f'/stewart/piston{i + 1}_cmd', 10)
            for i in range(6)
        ]

        self.sub = self.create_subscription(
            Twist,
            '/stewart/platform_twist',
            self.callback,
            10,
        )

    def transformation_matrix(self, x, y, z, r, p, yaw):
        cr, sr = math.cos(r), math.sin(r)
        cp, sp = math.cos(p), math.sin(p)
        cy, sy = math.cos(yaw), math.sin(yaw)

        return np.array([
            [cy * cp, -sy * cr + cy * sp * sr,  sy * sr + cy * sp * cr, x],
            [sy * cp,  cy * cr + sy * sp * sr, -cy * sr + sy * sp * cr, y],
            [   -sp,                  cp * sr,                 cp * cr, z],
            [    0.0,                     0.0,                     0.0, 1.0],
        ])

    def callback(self, msg: Twist):
        T = self.transformation_matrix(
            msg.linear.x,
            msg.linear.y,
            msg.linear.z + self.z_home,
            msg.angular.x,
            msg.angular.y,
            msg.angular.z,
        )

        for i in range(6):
            leg_vec = T @ self.p[i] - self.b[i]
            extension = float(np.linalg.norm(leg_vec[:3]) - self.nominal_length)
            out = Float64()
            out.data = extension
            self.pubs[i].publish(out)


def main(args=None):
    rclpy.init(args=args)
    node = IKNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
