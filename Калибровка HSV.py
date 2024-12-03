import cv2

cap = cv2.VideoCapture(0)
def nothing(args):pass

cv2.namedWindow("setup")

cv2.createTrackbar("Hmin", "setup", 0, 255, nothing)
cv2.createTrackbar("Smin", "setup", 0, 255, nothing)
cv2.createTrackbar("Vmin", "setup", 0, 255, nothing)
cv2.createTrackbar("Hmax", "setup", 255, 255, nothing)
cv2.createTrackbar("Smax", "setup", 255, 255, nothing)
cv2.createTrackbar("Vmax", "setup", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    Hmin = cv2.getTrackbarPos('Hmin', 'setup')
    Smin = cv2.getTrackbarPos('Smin', 'setup')
    Vnim = cv2.getTrackbarPos('Vmin', 'setup')
    Hmax = cv2.getTrackbarPos('Hmax', 'setup')
    Smax = cv2.getTrackbarPos('Smax', 'setup')
    Vmax = cv2.getTrackbarPos('Vmax', 'setup')

    min_p = (Hmin, Smin, Vnim)
    max_p = (Hmax, Smax, Vmax)

    frame_mask = cv2.inRange(frame_HSV, min_p, max_p)
    frame_m = cv2.bitwise_and(frame, frame_HSV, mask = frame_mask)  # создание фильтра
    cv2.imshow('img', frame_m)

    if (cv2.waitKey(1) == 27):
        break
cap.release()
cv2.destroyAllWindows()