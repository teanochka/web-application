from ultralytics import YOLO

model = YOLO("yolo11n-cls.pt")

results = model.train(data="datasets/dataset-resnet", epochs=100, imgsz=64)