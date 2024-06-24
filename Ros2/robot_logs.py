import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Float64, Int64MultiArray

import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge

class robotLogs(Node):
    def __init__(self):
        super().__init__("robot_logs")

        self.bridge = CvBridge()

        self.image_subscription = self.create_subscription(
            Image, 
            'camera/image', 
            self.image_callback,  
            10
        )
        self.image_subscription

        self.yolo_subscription = self.create_subscription(
            Float64,
            'yolo/info',
            self.yolo_callback,
            10
            )
        #self.yolo_subscription

        self.aruco_subscription = self.create_subscription(
            String,
            'aruco/detect', 
            self.aruco_callback,
            10
            )
        #self.aruco_subscription

    

    def image_callback(self, msg):

        # Преобразуем изображение из формата ROS в формат OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        cv2.imshow("frame", cv_image)
        cv2.waitKey(1)

    def yolo_callback(self, msg):
        yolo_log = msg
        print(str(yolo_log)) 

    def aruco_callback(self, msg):
        aruco_id = msg
        print(str(aruco_id))

    def line_callback(self, msg):
        left_line_sensor, right_line_sensor = msg.data
        print(left_line_sensor, right_line_sensor)

def main(args=None):
    rclpy.init(args=args)
    robot_log = robotLogs()
    rclpy.spin(robot_log)
