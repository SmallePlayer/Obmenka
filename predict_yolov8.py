if __name__ == '__main__':
    from ultralytics import YOLO
    model = YOLO(r'C:\Users\maks_\Downloads\Telegram Desktop\best.pt')
    model.predict(source='1.jpg',   # путь к файлу
                  save=True,        # сохранение
                  show=True,        # показ
                  imgsz=640,        # в каком разрешении
                  conf=0.25,        # порогове значение детектирования
                  device='cpu'      # то на каком устройстве будет производиться detect
                  )