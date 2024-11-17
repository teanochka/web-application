from ultralytics import YOLO

# Замените "yolo11n-cls.pt" на путь к другой модели
model = YOLO("yolo11n-cls.pt")

# Замените "datasets/dataset-resnet" на путь к датасету или .yaml файлу
results = model.train(data="datasets/dataset-resnet", epochs=100, imgsz=64)
