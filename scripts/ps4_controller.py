#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class PS4ControllerNode(Node):
    def __init__(self):
        super().__init__('ps4_controller')
        self.twist_msg = Twist()
        self.pub = self.create_publisher(Twist, '/stewart/platform_twist', 10)
        self.sub = self.create_subscription(Joy, '/joy', self.callback, 10)

    def callback(self, msg: Joy):
        if len(msg.axes) < 5 or len(msg.buttons) < 8:
            return

        self.twist_msg.linear.x = -msg.axes[0] / 2.0
        self.twist_msg.linear.y = msg.axes[1] / 2.0
        self.twist_msg.angular.x = -msg.axes[4] / 5.0
        self.twist_msg.angular.y = -msg.axes[3] / 5.0

        if msg.buttons[7] and self.twist_msg.linear.z < 1.0:
            self.twist_msg.linear.z += 0.01
        elif msg.buttons[6] and self.twist_msg.linear.z > 0.0:
            self.twist_msg.linear.z -= 0.01

        if msg.buttons[5] and self.twist_msg.angular.z < math.pi / 2.0:
            self.twist_msg.angular.z += 0.01
        elif msg.buttons[4] and self.twist_msg.angular.z > -math.pi / 2.0:
            self.twist_msg.angular.z -= 0.01

        self.pub.publish(self.twist_msg)


def main(args=None):
    rclpy.init(args=args)
    node = PS4ControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
