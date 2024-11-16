import torch
from torchvision import transforms
from PIL import Image
from ultralytics import YOLO
import model

with open("coco.yaml", "r") as f:
    import yaml
    class_names = yaml.safe_load(f)["names"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

resnet = model.resnet_load(device)

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.ToTensor(),
    ])    
    image = Image.open(image_path)
    return transform(image).unsqueeze(0)  

# Функция для оценки изображения через ResNet
def evaluate_with_resnet(image_path, resnet_model, device):
    image_tensor = preprocess_image(image_path).to(device)
    with torch.no_grad():
        output = resnet_model(image_tensor)
        probability = torch.sigmoid(output).item()  # Преобразование логитов в вероятность
    return probability

# Функция для обнаружения объектов через YOLO
def detect_with_yolo(image_path, yolo_model):
    results = yolo_model(image_path)
    return results

# Основная функция
def analyze_image(image_path, yolo_weights_path):
    yolo_model = YOLO(yolo_weights_path)
    
    landfill_probability = evaluate_with_resnet(image_path, resnet,device)
    print(f"Probability of landfill: {landfill_probability:.2f}")

    results = detect_with_yolo(image_path, yolo_model)
    print("Objects detected by YOLO:")
    for result in results[0].boxes:
        class_id = int(result.cls.item())
        class_name = class_names[class_id]
        confidence = result.conf.item()
        bbox = result.xyxy.tolist()
        print(f"Class: {class_name}, Confidence: {confidence:.2f}, Bbox: {bbox}")

    results[0].plot()

# Пример вызова функции
analyze_image(
    image_path="test-image.jpg",  # Путь к изображению
    yolo_weights_path="runs/detect/train3/weights/best.pt"  # Весы YOLO
)
