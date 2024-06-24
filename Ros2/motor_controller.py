import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Int64MultiArray
from time import sleep
from std_msgs.msg import String
import RPi.GPIO as GPIO


class ServoDvig(Node):
    def __init__(self):
        super().__init__("flag_dvig")
        self.line_variable_sub = self.create_subscription(Int64MultiArray, "line/variable", self.motor_controller, 10)
        self.subscription = self.create_subscription(String, 'aruco/detect', self.aruco_callback, 10) 
        self.timer = self.create_timer(0.2, self.print_log)     
        
        self.left_motor_forward = 13
        self.left_motor_back = 19
        self.right_motor_forward = 12
        self.right_motor_back = 16

        self.left_var = 0
        self.right_var = 0
        self.aruco_id = None
        self.aruco_old_id = None
        self.aruco_flag = None

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_motor_forward, GPIO.OUT)
        GPIO.setup(self.left_motor_back, GPIO.OUT)
        GPIO.setup(self.right_motor_forward, GPIO.OUT)
        GPIO.setup(self.right_motor_back, GPIO.OUT)


    def aruco_callback(self, msg):
        self.aruco_id = msg
        if self.aruco_old_id is not None and self.aruco_id != self.aruco_old_id:
            self.aruco_old_id = self.aruco_id
        #print(str(self.aruco_id))
        if self.aruco_old_id== "[[10]]":
            self.aruco_flag = 0
        if self.aruco_old_id == "[[20]]":
            self.aruco_flag = 1


    def motor_controller(self, msg):
        self.left_var, self.right_var = msg.data
        print(f"left: {self.left_var} right: {self.right_var}")

        # if (self.aruco_flag == 0): 
        #     print("start")
        #     if (self.left_var == 1):
        #         print("left-line-STOP")
        #         GPIO.output(self.left_motor_forward, GPIO.HIGH)
        #         GPIO.output(self.left_motor_back, GPIO.HIGH)
        #         GPIO.output(self.right_motor_forward, GPIO.HIGH)
        #         GPIO.output(self.right_motor_back, GPIO.HIGH)
        #     else:
        #         if (self.right_var == 0):
        #             print("left-------")
        #             GPIO.output(self.left_motor_forward, GPIO.HIGH)
        #             GPIO.output(self.left_motor_back, GPIO.LOW)
        #             GPIO.output(self.right_motor_forward, GPIO.HIGH)
        #             GPIO.output(self.right_motor_back, GPIO.HIGH)
        #         else:
        #             print("right------")
        #             GPIO.output(self.left_motor_forward, GPIO.HIGH)
        #             GPIO.output(self.left_motor_back, GPIO.HIGH)
        #             GPIO.output(self.right_motor_forward, GPIO.HIGH)
        #             GPIO.output(self.right_motor_back, GPIO.LOW)
        # elif (self.aruco_flag == 1):
        #     print("Stop")
        #     GPIO.output(self.left_motor_forward, GPIO.HIGH)
        #     GPIO.output(self.left_motor_back, GPIO.HIGH)
        #     GPIO.output(self.right_motor_forward, GPIO.HIGH)
        #     GPIO.output(self.right_motor_back, GPIO.HIGH)


    def print_log(self, msg):
        
        print(f"aruco {self.aruco_flag}, left {self.left_var}, right {self.right_var}")

        msg = Int64MultiArray()
        msg.data = []

        
            

def main(args=None):
    rclpy.init(args=args)
    node = ServoDvig()
    rclpy.spin(node)
    GPIO.cleanup()
    print("END NODE")
