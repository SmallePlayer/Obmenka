import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Float64MultiArray
import time 
from std_msgs.msg import String
import RPi.GPIO as GPIO


class UltraSo(Node):
    def __init__(self):
        super().__init__("flag_dvig")
        self.line_variable_publicher = self.create_publisher(Float64MultiArray, "ultra/variable", 10)
        self.timer = self.create_timer(0.1, self.motor_controller)
    
        self.trig_left_ultra_sens = 17
        self.echo_left_ultra_sens = 27
        self.trig_right_ultra_sens = 10
        self.echo_right_ultra_sens = 9
        self.trig_center_ultra_sens = 14
        self.echo_center_ultra_sens = 15

        

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_left_ultra_sens, GPIO.OUT)
        GPIO.setup(self.echo_left_ultra_sens, GPIO.IN)
        GPIO.setup(self.trig_right_ultra_sens, GPIO.OUT)
        GPIO.setup(self.echo_right_ultra_sens, GPIO.IN)
        GPIO.setup(self.trig_center_ultra_sens, GPIO.OUT)
        GPIO.setup(self.echo_center_ultra_sens, GPIO.IN)  

    def motor_controller(self):
        msg = Float64MultiArray()
        left_sens = self.distance(self.trig_left_ultra_sens, self.echo_left_ultra_sens)
        right_sens = self.distance(self.trig_right_ultra_sens, self.echo_right_ultra_sens)
        center_sens = self.distance(self.trig_center_ultra_sens, self.echo_center_ultra_sens)
        print(f"left: {left_sens} center: {center_sens} right: {right_sens}")
        msg.data = [left_sens, right_sens, center_sens]
        self.line_variable_publicher.publish(msg)



    def distance(self, trig, echo):
            # Установить пин TRIG в HIGH на 10 микросекунд
        GPIO.output(trig, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig, GPIO.LOW)
            
        pulse_start = time.time()
        pulse_end = time.time()
            
            # Ждем, пока пин ECHO не станет HIGH
        while GPIO.input(echo) == 0:
            pulse_start = time.time()
            
            # Ждем, пока пин ECHO не вернется в LOW
        while GPIO.input(echo) == 1:
            pulse_end = time.time()
            
        # Рассчитываем время прохождения звуковой волны
        pulse_duration = pulse_end - pulse_start
            
        # Переводим время в расстояние
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        
        time.sleep(0.25)
        print(distance)
        return distance
            

def main(args=None):
    rclpy.init(args=args)
    node = UltraSo()
    rclpy.spin(node)

