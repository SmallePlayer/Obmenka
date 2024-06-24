import rclpy
from std_msgs.msg import String

def talker():
    # Создание нового экземпляра ROS 2 Node
    rclpy.init(args=None)
    node = rclpy.create_node('talker')

    # Создание Publisher объекта
    topic = 'chatter'
    qos = rclpy.qos.QoSProfile(depth=10)
    pub = node.create_publisher(String, topic, qos)

    # Создание цикла
    rate = 10  # Гц
    timer = node.create_timer(rate, timer_callback)

    def timer_callback(event):
        msg = String()
        msg.data = 'Hello, world!'
        pub.publish(msg)
        print('Publishing: {}'.format(msg.data))

    rclpy.spin(node)

# Запуск talker
if __name__ == '__main__':
    try:
        talker()
    except Exception as e:
        print(e)
    finally:
        rclpy.shutdown()
