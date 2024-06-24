# Импортируем необходимые библиотеки
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
import time


# Определяем класс CaptureCameraNode, который является ROS2-нодой для захвата изображений с камеры
class CaptureCameraNode(Node):
    def __init__(self):
        # Инициализируем родительский класс Node с именем 'capture_camera'
        super().__init__('capture_camera')
        
        self.bridge = CvBridge()

        # Создаем издателей для публикации изображений и текстовых сообщений
        self.publisher = self.create_publisher(Image, 'camera/image', 10)
        self.text_publisher = self.create_publisher(String, 'camera/info', 10)

        # Определяем путь к устройству камеры
        path = 0
        # Инициализируем объект VideoCapture для захвата видео с камеры
        self.cap = cv2.VideoCapture(path, cv2.CAP_V4L)
        print("Camera created", self.cap)

        # Создаем таймер, который вызывает функцию capture_and_publish каждую секунду
        self.timer = self.create_timer(0.01, self.capture_and_publish)

        

    # Функция для захвата и публикации изображения
    def capture_and_publish(self):
        # Захватываем изображение с камеры
        ret, frame = self.cap.read()
        if ret:
            #time.sleep(2)
            # Выводим текущее время захвата на консоль
            print("Last time of get image:", time.ctime())
            
            # Преобразуем изображение в формат ROS и публикуем его
            msg = self.bridge.cv2_to_imgmsg(frame, "bgr8")
            self.publisher.publish(msg)

            # Подготавливаем и публикуем текстовое сообщение с временем захвата изображения
            msg = String()
            msg.data = f"Last time of get image: {time.ctime()}"
            self.text_publisher.publish(msg)

   

def main(args=None):
    # Инициализируем ROS
    rclpy.init(args=args)
    # Создаем объект нашей ноды
    capture_camera = CaptureCameraNode()
    # Запускаем цикл обработки ROS
    rclpy.spin(capture_camera)

if __name__ == '__main__':
    main()