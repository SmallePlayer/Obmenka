import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Int64MultiArray
from time import sleep
from std_msgs.msg import String
import RPi.GPIO as GPIO


class ServoDvig(Node):
    def __init__(self):
        super().__init__("flag_dvig")
        self.line_variable_publicher = self.create_publisher(Int64MultiArray, "line/variable", 10)
        self.timer = self.create_timer(0.1, self.motor_controller)
        self.left_line_sensor = 23
        self.right_line_sensor = 24

        

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_line_sensor, GPIO.IN)
        GPIO.setup(self.right_line_sensor, GPIO.IN)

    def motor_controller(self):
        msg = Int64MultiArray()
        left_variable = GPIO.input(self.left_line_sensor)
        right_variable = GPIO.input(self.right_line_sensor)
        msg.data = [left_variable, right_variable]
        self.line_variable_publicher.publish(msg)
        #print(f"left variable: {left_variable} right variable: {right_variable}")
        print(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ServoDvig()
    rclpy.spin(node)
