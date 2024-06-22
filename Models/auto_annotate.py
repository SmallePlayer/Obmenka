import os
import cv2
import time
import numpy
from ultralytics import YOLO

model = YOLO(r'C:\Models\Ovoshi\weights\best.pt')
model.fuse()

print("Текущая деректория:", os.getcwd())
if not os.path.isdir('folder'):
    os.mkdir('folder')
os.chdir('folder')
print("Текущая деректория:", os.getcwd())

cap = cv2.VideoCapture(r'C:\Users\maks_\PycharmProjects\test\video.mp4')
if not cap.isOpened():
    print("is not open video")
    exit()

saved_counter = 0
frame_interval = 0.5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = model(source=frame, verbose=False, device='cpu', stream=True)
    for result in result:
        box = result.boxes.xyxy.tolist()
        ids = result.boxes.id
        print(f"{ids} {box}")
    with open(f'test_frame_{saved_counter:05d}.txt', 'w') as file:
        file.write(' '.join(map(str, box)))


    time.sleep(frame_interval)

    cv2.imshow('frame', frame)
    cv2.imwrite(f'test_frame_{saved_counter:05d}.jpg', frame)
    print(f'video_frame_{saved_counter:05d}.jpg')
    saved_counter += 1

    if cv2.waitKey(1) == 27:
        break

print(f"Количество изображений:{saved_counter}")

cap.release()
cv2.destroyAllWindows()