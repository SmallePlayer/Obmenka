import cv2
import numpy as np
import time
from simple_pid import PID

# Настройки PID
pid = PID(1.0, 0.1, 0.05, setpoint=0)  # Параметры PID (Kp, Ki, Kd)
pid.output_limits = (-1, 1)  # Ограничение на вывод PID для коррекции

# Настройки камеры
cap = cv2.VideoCapture(0)  # Захват изображения с камеры

# Параметры изображения и управления
frame_width = 640  # Ширина кадра
frame_height = 480  # Высота кадра

# Устанавливаем разрешение камеры
cap.set(3, frame_width)
cap.set(4, frame_height)

# Параметры управления моторами (условно)
MAX_SPEED = 100  # Максимальная скорость
MIN_SPEED = 20   # Минимальная скорость

# Инициализация моторов (замените код в реальной системе)
def set_motor_speeds(left_speed, right_speed):
    # Здесь код для управления моторами
    print(f"Left motor speed: {left_speed}, Right motor speed: {right_speed}")

# Основной цикл
while True:
    ret, frame = cap.read()  # Чтение кадра с камеры
    if not ret:
        break

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Применяем бинаризацию для выделения линии
    _, thresholded = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Найдем контуры на изображении
    contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Найдем контур с наибольшей площадью (это и будет наша линия)
        largest_contour = max(contours, key=cv2.contourArea)

        # Найдем моменты для вычисления центра линии
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            # Центр линии
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Рисуем центр контуров на изображении для отладки
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            # Получаем ошибку (смещение центра линии от центра кадра)
            error = cx - frame_width // 2

            # Используем PID для вычисления корректировки мощности на моторах
            correction = pid(error)

            # Корректируем скорость моторов
            left_speed = max(min(MAX_SPEED - correction, MAX_SPEED), MIN_SPEED)
            right_speed = max(min(MAX_SPEED + correction, MAX_SPEED), MIN_SPEED)

            # Управление моторами
            set_motor_speeds(left_speed, right_speed)

        else:
            # Если линия не найдена, можно остановить робота или принять другие действия
            set_motor_speeds(0, 0)

    # Отображаем изображение для отладки
    cv2.imshow("Frame", frame)
    cv2.imshow("Thresholded", thresholded)

    # Выход при нажатии клавиши "q"
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
