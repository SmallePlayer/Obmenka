import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64MultiArray, Float64MultiArray
from time import sleep
from std_msgs.msg import String
import numpy as np

class ServoDvig(Node):
    def __init__(self):
        super().__init__("speed_dvig")
        #подписки на топики
        self.subscription_sensor = self.create_subscription(Float64MultiArray, 'ultra/variable', self.ultras_callback, 10)      
        self.subscription_yolo_znaki = self.create_subscription(String, 'yolo/znak', self.yolo_znak_callback, 10)
        self.subscription_yolo_svetofor = self.create_subscription(String, 'yolo/svet', self.yolo_svet_callback, 10)
        #паблишер скорости на мотор
        self.publisher = self.create_publisher(Float64MultiArray, 'speed/variable', 10)
        #минимальная скорость робота
        self.standart_speed = 15
        self.flag = 0

        self.yolo_znaki = 'pravo'
        self.yolo_svet = None

    def yolo_znak_callback(self, msg):
        self.yolo_znaki = msg.data
        #print(msg.data)
        #print(f"znak:{self.yolo_znaki}")
        
    def yolo_svet_callback(self, msg):
        self.yolo_svet = msg.data
        #print(msg.data)
        #print(f"svetofor:{self.yolo_svet}")
    
    #определение направления и мощности на моторы
    def detect_speed(self, left_sens, right_sens):
        difference = left_sens - right_sens
        devision = self.pid(difference)
        return abs(devision)
    
    #пид есть пид
    def pid(self, input_data):
            # Константы для регулятора
            setpoint = 0
            Kp = 0.1
            Ki = 0.0
            Kd = 0.1
            i = 0

            var = input_data

            errorOld = 0

            error = setpoint - var
            print(f"error: {error}")
                    
            d = error - errorOld
            print(f"errorOld: {errorOld}")

            i = i + (setpoint - var)
            print(f"i: {i}")

            out_var = (setpoint - var)*Kp + i*Ki +d*Kd
            errorOld = error

            var = var + out_var

            print(f"setpoint: {setpoint} | var: {var} | output_var: {out_var}")
            return out_var
        
    #выставление скорости на каждый мотор в зависимости от направления
    def speed_nap(self, stock_speed, left_sens, right_sens, devition):

        if (left_sens - right_sens) < 0:
            self.speed_left = stock_speed + devition
            self.speed_right = stock_speed - devition
            print(f"> {self.speed_left} || {self.speed_right}")
        elif (left_sens - right_sens) > 0:
            self.speed_left = stock_speed - devition
            self.speed_right = stock_speed + devition
            print(f"< {self.speed_left} || {self.speed_right}")
        else:
            self.speed_left = stock_speed 
            self.speed_right = stock_speed
            print(f"^ {self.speed_left} || {self.speed_right}")
        #если больше ста, то значит сто
        return self.speed_left, self.speed_right
        
        
    def ultras_callback(self, msg):
        self.left_sens, self.right_sens, self.center_sens = msg.data 
        msg = Float64MultiArray()

        current_znak = self.yolo_znaki  #save now znak

        print(f"znak:{self.yolo_znaki}")    
        print(f"svetofor:{self.yolo_svet}")

        # первое двиение
        if self.flag == 0:
            print("ЕДЕМ ПРЯМО---------------------")
            standart_speed = 18.0
            msg.data = [20.0, standart_speed]
            self.publisher.publish(msg)
            sleep(3)
            self.flag = 1
            
        #если не красный то мы не едем
        if self.yolo_svet == "green" or self.center_sens < 20: 
            print("можно ехать")
            #если знак вправо едем и стена кончилась делаем поворот
            if current_znak == 'pravo' and self.left_sens > 20:
                print("едем направо")
                self.speed_left = 30.0
                self.speed_right = 15.0
                msg.data = [self.speed_left , self.speed_right]
                self.publisher.publish(msg)
                sleep(5)
                current_znak = self.yolo_znaki  #save now znak
                #если знак прямо едем и стена где либо кончилась едем вперед
            elif current_znak == 'pramo' and (self.left_sens > 50 or self.right_sens > 50):
                print("едем прямо")
                self.speed_left = 20.0
                self.speed_right = 20.0
                msg.data = [self.speed_left , self.speed_right]
                self.publisher.publish(msg)
                sleep(2)
                current_znak = self.yolo_znaki  #save now znak
                #если знак влево едем и стена кончилась делаем поворот
            elif current_znak == 'levo' and self.right_sens > 50:
                print("едем налево")
                self.speed_left = 15.0
                self.speed_right = 23.0
                msg.data = [self.speed_left , self.speed_right]
                self.publisher.publish(msg)
                sleep(5)
                current_znak = self.yolo_znaki  #save now znak

        # то на сколько надо изменить мощность на моторы(либо в положительную либо в отрицательну сторону)
        dev = self.detect_speed(self.left_sens, self.right_sens)

        
        self.speed_left, self.speed_right = self.speed_nap(self.standart_speed, self.left_sens, self.right_sens, dev)
        if self.speed_left > 100: self.speed_left = 100.0
        elif self.speed_right > 100: self.speed_right = 100.0
        elif self.speed_left <= 0: self.speed_left = 10.0
        elif self.speed_right <= 0: self.speed_right = 10.0

        msg.data = [self.speed_left , self.speed_right]
        print(msg.data)
        self.publisher.publish(msg)
                   
def main(args=None):
    rclpy.init(args=args)
    node = ServoDvig()
    rclpy.spin(node)
    print("END NODE")