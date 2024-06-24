import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2

class ImageReaderNode(Node):

    def __init__(self):
        super().__init__('image_reader_node')  # Инициализируем родительский класс Node с именем 'image_reader_node'

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

    def image_callback(self, msg):
        # Преобразуем изображение из формата ROS в формат OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

        cv2.imshow("frame", cv_image)
        cv2.waitKey(1)
        
        

def main(args=None):
    rclpy.init(args=args)
    image_reader = ImageReaderNode()
    rclpy.spin(image_reader)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()