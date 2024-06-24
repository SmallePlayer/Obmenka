import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray, Float64MultiArray
from time import sleep
from std_msgs.msg import String
import numpy as np
import RPi.GPIO as GPIO

class ServoDvig(Node):
    def __init__(self):
        super().__init__("dvijenie_apteka")
        self.aruco_subscriber = self.create_subscription(String, 'aruco/detect', self.aruco_callback, 10)
        self.subscription = self.create_subscription(Float64MultiArray, 'ultra/variable', self.ultras_callback, 10)      
        
        self.standart_speed = 20
        #self.publisher = self.create_publisher(Float64MultiArray, '', 10)
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
    
    def start(self):
        if self.flag == 1:    
            GPIO.output(self.left_motor_forward, GPIO.LOW)
            GPIO.output(self.left_motor_back, GPIO.LOW)
            self.pwmr.ChangeDutyCycle(20)
            GPIO.output(self.right_motor_back, GPIO.LOW)
            sleep(1)
            self.pwml.ChangeDutyCycle(20)
            GPIO.output(self.left_motor_back, GPIO.LOW)
            self.pwmr.ChangeDutyCycle(20)
            GPIO.output(self.right_motor_back, GPIO.LOW)
            sleep(1)
            GPIO.output(self.left_motor_forward, GPIO.LOW)
            GPIO.output(self.left_motor_back, GPIO.LOW)
            GPIO.output(self.right_motor_forward, GPIO.LOW)
            GPIO.output(self.right_motor_back, GPIO.LOW)
            self.flag = 0

    def aruco_callback(self, msg):
        self.aruco = msg.data
        print("da")
        if self.aruco == '10':
            self.flag = 1
            self.start()    

    def ultras_callback(self, msg):
        self.right_sens, self.left_sens, self.center_sens = msg.data 
        msg = Float64MultiArray()
        
        if(self.left_sens <= 20 and self.center_sens <= 20):
            self.pwml.ChangeDutyCycle(20)
            GPIO.output(self.left_motor_back, GPIO.LOW)
            GPIO.output(self.right_motor_forward, GPIO.LOW)
            GPIO.output(self.right_motor_back, GPIO.LOW)
            sleep(1)
            GPIO.output([self.left_motor_back, self.left_motor_forward, self.right_motor_back, self.right_motor_forward])
                    
def main(args=None):
    rclpy.init(args=args)
    node = ServoDvig()
    rclpy.spin(node)
    print("END NODE")
