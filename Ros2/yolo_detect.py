import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from ultralytics import YOLO
from std_msgs.msg import String

class ImageDetect(Node):
    def __init__ (self):
        super().__init__('image_yolo_predict')

        self.bridge = CvBridge()
        self.subscription = self.create_subscription(Image, 'camera/image', self.image_callback, 1)
        self.text_publisher = self.create_publisher(String, 'yolo/svet', 1)

    def image_callback(self, msg):
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        log = 0

        model = YOLO(r'/home/pes/Desktop/20nSvet/weights/best.pt')
        results = model.predict(cv_image)

        try:
            result = results[0]
            box = result[0]
            
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                print(f"name object:{class_id}")
                msg = String()
                msg.data = class_id
                self.text_publisher.publish(msg)
        except:
            print('ERROR')

def main(args = None):
    rclpy.init(args=args)
    capture = ImageDetect()
    rclpy.spin(capture)