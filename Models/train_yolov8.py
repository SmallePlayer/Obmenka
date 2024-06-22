if __name__ == '__main__':
    from ultralytics import YOLO
    model = YOLO('yolov8m.pt')
    model.to("cuda")
    model.train(data='C:/znaki/data.yaml',  # путь к data.yaml
                epochs=30,                  # количество эпох
                imgsz=640,                  # размер изображени ядо которого ужимается
                batch=2,                    # количество изображений отправляемых в память
                cache=True,                 # использование опертивной памяти
                verbose=True,               #
                plots=True,                 # создание подробных графиков
                save_period=5               # период сохранения веса модели
                )