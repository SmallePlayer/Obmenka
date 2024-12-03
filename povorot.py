import cv2
import numpy as np

# Захват видео с камеры
cap = cv2.VideoCapture(0)

while True:
    # Чтение кадра
    _, frame = cap.read()

    # Преобразование BGR в HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Определение диапазона синего цвета в HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Пороговое преобразование HSV изображения, чтобы получить только синие цвета
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Битовая маска и исходное изображение
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Находим контуры
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Получаем прямоугольник вокруг контура
        x, y, w, h = cv2.boundingRect(contour)

        # Определяем, находится ли контур слева или справа
        if x < frame.shape[1]//2:
            position = 'left'
        else:
            position = 'right'

        print(f'Blue color is on the {position} side')

    # Показываем изображение
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    # Выход из цикла при нажатии 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы и закрываем все окна
cap.release()
cv2.destroyAllWindows()
