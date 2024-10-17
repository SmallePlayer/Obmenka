import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters()

    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    corners, ids, rejected = detector.detectMarkers(gray)

    print("Detected markers:", ids)
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('Detected Markers', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cv2.destroyAllWindows()