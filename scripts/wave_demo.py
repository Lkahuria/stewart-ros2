#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class StewartWaveDemo(Node):
    def __init__(self):
        super().__init__('stewart_wave_demo')
        self.pub = self.create_publisher(Twist, '/stewart/platform_twist', 10)
        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(1.0 / 30.0, self.timer_callback)  # 30 Hz
        self.get_logger().info('Starting continuous Stewart platform wave motion...')

    def timer_callback(self):
        now = self.get_clock().now()
        t = (now - self.start_time).nanoseconds * 1e-9

        freq = 0.25 #in Hz: 0.25 = 1 cycle every 4 sec, 0.5 = 1 cycle every 2 sec)
        w = 2.0 * math.pi * freq

        msg = Twist()
        msg.linear.z = 0.35 + 0.15 * math.sin(w * t)
        msg.linear.x = 0.12 * math.cos(w * t)
        msg.linear.y = 0.12 * math.sin(w * t)

        msg.angular.x = 0.18 * math.sin(w * t)
        msg.angular.y = 0.18 * math.cos(w * t)
        msg.angular.z = 0.25 * math.sin(0.5 * w * t)

        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = StewartWaveDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
