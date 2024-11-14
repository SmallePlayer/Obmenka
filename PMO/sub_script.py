import asyncio
from oop import *
import cv2

def main():
        sub = PMO("localhost",49002,'room')
        while True:
            data = sub.subscriber_frame(yolo=True)
            print(data)

if __name__ == "__main__":
    main()