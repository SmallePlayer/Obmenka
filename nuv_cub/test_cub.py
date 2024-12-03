import cv2
import numpy as np

# Функция для вычисления расстояния до объекта (по размеру объекта на изображении)
def calculate_distance(w, focal_length, real_size):
    # Расстояние = (реальный размер * фокусное расстояние) / размер объекта в пикселях
    return (real_size * focal_length) / w

# Параметры
real_size = 0.1  # Реальный размер куба (например, 10 см)
focal_length = 500  # Фокусное расстояние камеры (необходимо откалибровать)

cap = cv2.VideoCapture(0)  # Открываем веб-камеру

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Преобразуем изображение в HSV для поиска по цвету
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Диапазон красного цвета (можно настроить)
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Создание маски для красного цвета
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Нахождение контуров
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Пороговое значение для фильтрации мелких объектов
            # Прямоугольник вокруг объекта
            x, y, w, h = cv2.boundingRect(contour)

            # Рисуем прямоугольник на изображении
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Оценка расстояния до объекта
            distance = calculate_distance(w, focal_length, real_size)
            cv2.putText(frame, f"Distance: {distance:.2f}m", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Логика избегания столкновений
            # Если расстояние меньше определенной границы, менять направление робота
            if distance < 0.5:  # Если слишком близко (например, 50 см)
                print("Too close to the cube! Avoiding collision...")
                # Можно вызвать функцию, чтобы изменить направление робота

    # Показываем результат
    cv2.imshow('Detected Cube', frame)

    # Прерывание программы при нажатии 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
