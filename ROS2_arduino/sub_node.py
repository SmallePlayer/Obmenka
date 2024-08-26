#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MyNode(Node):

    def __init__(self):
        super().__init__("sub_node")
        self.subscrip = self.create_subscription(String, "/laptop/string", self.msg_callback, 1)

    def msg_callback(self, msg: String):
        message = msg.data
        self.get_logger().info(message)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()