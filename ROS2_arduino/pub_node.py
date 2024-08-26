#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) # подключаемся к ардуино

class MyNode(Node):

    def __init__(self):
        super().__init__("publish_node")
        self.publisher = self.create_publisher(String, "/laptop/string", 1)

    def senf_message(self):
        a = input()     # ввод данных с клавиатуры
        ms = bytes(f"{a}",'utf-8')
        ser.write(ms)   # отправка данных в ардуино
        line = ser.readline().decode('utf-8').rstrip() # считываем ответный сигнал с ардуино
        msg = String()
        msg.data = line
        self.publisher.publish(msg) # публикуем полученные от ардуино данные в топик
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()