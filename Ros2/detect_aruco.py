import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import cv2.aruco as aruco
from cv_bridge import CvBridge


class detectAruoMarkers(Node):
    def __init__(self):
        super().__init__("aruco_detect")

        # Создаем объект CvBridge для преобразования изображений между OpenCV и ROS
        self.bridge = CvBridge()

        # Подписываемся на тему 'camera/image' для чтения изображений
        self.subscription = self.create_subscription(
            Image, 
            'camera/image', 
            self.image_callback, 
            10
            )      
        self.subscription
        self.aruco_publisher = self.create_publisher(String, 'aruco/detect', 10)
        

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        msg = String()

        dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_250)
        detector_params = aruco.DetectorParameters()

        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, 
                        dictionary, parameters=detector_params )
        
        if ids is not None:
            aruco.drawDetectedMarkers(cv_image,corners)

        id = str(ids)
        print(f" id:{id}, type:{type(id)}")

        msg.data = id
        self.aruco_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    detectAruco = detectAruoMarkers()
    rclpy.spin(detectAruco)
    