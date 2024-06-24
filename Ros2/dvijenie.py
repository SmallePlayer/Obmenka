import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Float64MultiArray
from time import sleep
from std_msgs.msg import String
import RPi.GPIO as GPIO
import numpy as np

class ServoDvig(Node):
    def __init__(self):
        super().__init__("flag_dvig")
        self.subscription = self.create_subscription(Float64MultiArray, 'ultra/variable', self.ultras_callback, 10)      
        self.text_subscription = self.create_subscription(String, 'pc/info', self.yol_callback, 10)
        self.left_motor_forward = 13
        self.left_motor_back = 19
        self.right_motor_forward = 12
        self.right_motor_back = 16

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_motor_forward, GPIO.OUT)
        GPIO.setup(self.left_motor_back, GPIO.OUT)
        GPIO.setup(self.right_motor_forward, GPIO.OUT)
        GPIO.setup(self.right_motor_back, GPIO.OUT)
        self.pwml = GPIO.PWM(self.left_motor_forward, 50)
        self.pwmr = GPIO.PWM(self.right_motor_forward, 50)
        self.pwml.start(0)
        self.pwmr.start(0)


    def ultras_callback(self, msg):
        
        speed_left, speed_right = msg.data

                    
        print(f"left {speed_left} right {speed_right}")
        self.pwml.ChangeDutyCycle(speed_left)
        GPIO.output(self.left_motor_back, GPIO.LOW)
        self.pwmr.ChangeDutyCycle(speed_right)
        GPIO.output(self.right_motor_back, GPIO.LOW)
            
def main(args=None):
    rclpy.init(args=args)
    node = ServoDvig()
    rclpy.spin(node)
    GPIO.cleanup()
    print("END NODE")
