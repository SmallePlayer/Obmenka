import numpy as np
import math
import time
import serial

# Класс для модели робота
class Robot:
    def __init__(self, x=0, y=0, theta=0, left_wheel_diameter=0.1, right_wheel_diameter=0.1, encoder_ticks_per_rev=360):
        self.x = x  # позиция по X
        self.y = y  # позиция по Y
        self.theta = theta  # угол ориентации робота (в радианах)

        # Параметры колес и энкодеров
        self.left_wheel_diameter = left_wheel_diameter  # диаметр левого колеса (м)
        self.right_wheel_diameter = right_wheel_diameter  # диаметр правого колеса (м)
        self.encoder_ticks_per_rev = encoder_ticks_per_rev  # количество импульсов на один оборот энкодера

        # Коэффициенты для вычисления пройденного пути
        self.distance_per_pulse_left = math.pi * self.left_wheel_diameter / self.encoder_ticks_per_rev  # расстояние за один импульс (левой колесо)
        self.distance_per_pulse_right = math.pi * self.right_wheel_diameter / self.encoder_ticks_per_rev  # расстояние за один импульс (правое колесо)

        # Состояния энкодеров
        self.last_encoder_left = 0
        self.last_encoder_right = 0

        # Скорости (м/с)
        self.speed_left = 0
        self.speed_right = 0
        self.speed = 0  # Средняя скорость робота

    def update_position(self, delta_left, delta_right, wheel_base):
        # Обновление позиции робота на основе изменений энкодеров
        delta_dist = (delta_left + delta_right) / 2
        delta_theta = (delta_right - delta_left) / wheel_base

        self.theta += delta_theta
        self.x += delta_dist * math.cos(self.theta)
        self.y += delta_dist * math.sin(self.theta)

    def update_orientation_with_gyro(self, gyro_rate, time_step):
        # Обновление ориентации робота с использованием гироскопа
        # gyro_rate в градусах в секунду, но нужно перевести в радианы.
        delta_theta = math.radians(gyro_rate) * time_step
        self.theta += delta_theta

    def update_speed(self, encoder_left, encoder_right, time_step):
        # Обновление скорости робота на основе показаний энкодеров
        delta_left = (encoder_left - self.last_encoder_left) * self.distance_per_pulse_left
        delta_right = (encoder_right - self.last_encoder_right) * self.distance_per_pulse_right

        # Считываем скорости для обоих колес
        self.speed_left = delta_left / time_step
        self.speed_right = delta_right / time_step

        # Средняя скорость робота
        self.speed = (self.speed_left + self.speed_right) / 2

        # Обновляем последние показания энкодеров
        self.last_encoder_left = encoder_left
        self.last_encoder_right = encoder_right


# Класс для карты
class Map:
    def __init__(self, width=40, height=40, resolution=0.5):
        self.width = width  # ширина карты
        self.height = height  # высота карты
        self.resolution = resolution  # разрешение карты в метрах
        self.grid = [['.' for _ in range(width)] for _ in range(height)]  # сетка карты

    def add_point(self, x, y):
        # Добавление точки на карту
        grid_x = int(x / self.resolution) + self.width // 2
        grid_y = int(y / self.resolution) + self.height // 2

        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            self.grid[grid_y][grid_x] = '#'

    def show_map(self, robot_x, robot_y):
        # Отображение карты в терминале
        grid_x = int(robot_x / self.resolution) + self.width // 2
        grid_y = int(robot_y / self.resolution) + self.height // 2

        for y in range(self.height):
            for x in range(self.width):
                if x == grid_x and y == grid_y:
                    print('*', end='')  # Позиция робота
                else:
                    print(self.grid[y][x], end='')  # Обозначение для карты
            print()  # Переход на новую строку


# Функция для чтения данных с Arduino
def read_data_from_arduino(ser):
    data = ser.readline().decode('utf-8').strip()
    return data


# Основной цикл
def run_simulation():
    # Настройка робота и карты
    robot = Robot(x=0, y=0, theta=0, left_wheel_diameter=0.1, right_wheel_diameter=0.1, encoder_ticks_per_rev=360)
    robot_speed_left = 0.1  # скорость левого колеса (м/с)
    robot_speed_right = 0.1  # скорость правого колеса (м/с)
    wheel_base = 0.5  # расстояние между колесами робота (м)
    time_step = 0.1  # шаг времени для симуляции

    # Создаем объект карты
    map_obj = Map(width=40, height=40, resolution=0.5)

    # Открываем последовательный порт для связи с Arduino
    ser = serial.Serial('COM3', 9600, timeout=1)  # Укажите правильный порт для вашей системы

    while True:
        # Чтение данных с Arduino
        data = read_data_from_arduino(ser)
        encoder_left, encoder_right, gyro_rate, laser_left, laser_right, laser_front, laser_back = map(float, data.split(','))

        # Обновление скорости робота на основе показаний энкодеров
        robot.update_speed(encoder_left, encoder_right, time_step)

        # Обновление позиции робота на основе показаний энкодеров
        robot.update_position(encoder_left * 0.01, encoder_right * 0.01, wheel_base)  # Коэффициент масштабирования

        # Обновляем угол робота с помощью гироскопа
        robot.update_orientation_with_gyro(gyro_rate, time_step)

        # Добавляем данные с лазеров в карту
        map_obj.add_point(robot.x + laser_left * math.cos(robot.theta - math.pi / 4), robot.y + laser_left * math.sin(robot.theta - math.pi / 4))
        map_obj.add_point(robot.x + laser_right * math.cos(robot.theta + math.pi / 4), robot.y + laser_right * math.sin(robot.theta + math.pi / 4))
        map_obj.add_point(robot.x + laser_front * math.cos(robot.theta), robot.y + laser_front * math.sin(robot.theta))
        map_obj.add_point(robot.x + laser_back * math.cos(robot.theta + math.pi), robot.y + laser_back * math.sin(robot.theta + math.pi))

        # Выводим информацию о скорости
        print(f"Скорость левого колеса: {robot.speed_left:.2f} м/с")
        print(f"Скорость правого колеса: {robot.speed_right:.2f} м/с")
        print(f"Средняя скорость робота: {robot.speed:.2f} м/с")

        # Отображаем карту в терминале
        map_obj.show_map(robot.x, robot.y)

        time.sleep(time_step)


if __name__ == "__main__":
    run_simulation()

