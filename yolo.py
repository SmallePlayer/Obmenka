from ultralytics import YOLO
model = YOLO(r'C:\Users\pes\Downloads\Telegram Desktop\n\train12\weights\best.pt')
model.predict(source=0,   # путь к файлу        # сохранение
                show=True,        # показ
                imgsz=640,        # в каком разрешении      # порогове значение детектирования
                device='cpu'      # то на каком устройстве будет производиться detect
                )

