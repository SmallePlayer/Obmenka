import time
import zmq
import cv2
import numpy as np
import base64

import processing_def

class PMO:
    def __init__(self,address: str, port: int,topic: str):
        self.address = address
        self.port = port
        self.topic = topic

    def publisher_string(self,data: str|int):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://{self.address}:{self.port}")
        while True:
            message = f"{self.topic} {data}"
            socket.send_string(message)
            time.sleep(1)

    def publisher_frame(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://{self.address}:{self.port}")
        cap = cv2.VideoCapture(0)
        while True:
            encode_frame = PMO.__capture_camera(self,cap)
            socket.send_string(f"{self.topic} {encode_frame}")

    def subscriber_string(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{self.address}:{self.port}")
        socket.setsockopt_string(zmq.SUBSCRIBE,self.topic)
        while True:
            message = socket.recv_string()
            topic, data = message.split(' ',maxsplit=1)
            return data

    def subscriber_frame(self,yolo: bool):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://{self.address}:{self.port}")
        socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)
        while True:
            data = socket.recv_string()
            topic, encode_frame = data.split(' ',maxsplit=1)
            frame = PMO.__decoding_frame(self,encode_frame)
            if yolo==True:
                class_id = processing_def.yolo_detect("11","n",frame,show=True)
                return class_id

    def __capture_camera(self,cap):
        ret, frame = cap.read()
        success, encoded_frame = cv2.imencode('.jpg', frame)
        jpg_frame_text = base64.b64encode(encoded_frame).decode('utf-8')
        return jpg_frame_text

    def __decoding_frame(self,encode_frame):
        img = base64.b64decode(encode_frame)
        nparray = np.frombuffer(img, np.uint8)
        frame = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        return frame
