import time
import zmq

class PMO:
    def __init__(self,address,port,topic):
        self.address = address
        self.port = port
        self.topic = topic

class Publisher(PMO):
    def __init__(self,address,port,topic,data, Delay):
        super().__init__(address,port,topic)
        self.data = data
        self.delay = Delay

    def publish(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://{self.address}:{self.port}")
        while True:
            message = f"{self.topic} {self.data}"
            socket.send_string(message)
            time.sleep(1)

class Subscriber(PMO):
    def __init__(self,address,port,topic):
        super().__init__(address,port,topic)

    def subscriber(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{self.address}:{self.port}")
        socket.setsockopt_string(zmq.SUBSCRIBE,self.topic)
        while True:
            data = socket.recv_string()
            return data