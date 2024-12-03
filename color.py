import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_red = np.array([0, 100, 50])
    up_red = np.array([15, 255, 255])
    mask_red = cv2.inRange(frame_HSV, low_red , up_red)

    result = cv2.bitwise_and(frame, frame_HSV, mask=mask_red)

    cv2.imshow('Original', frame)
    cv2.imshow('red_mask', result)

    if (cv2.waitKey(1) == 27):
        break

cap.release()
cv2.destroyAllWindows()