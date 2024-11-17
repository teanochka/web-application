from ultralytics import YOLO
from cv2 import imread, imwrite, rectangle, putText, FONT_HERSHEY_SIMPLEX
import os

with open("coco.yaml", "r") as f:
    import yaml
    class_names = yaml.safe_load(f)["names"]

def analyze_image(image_path):

    cls_model = YOLO("yolo11n-cls.pt")
    cls_model = YOLO("runs/classify/train2/weights/best.pt")

    dtc_model = YOLO("yolov8n.pt")
    dtc_model = YOLO("runs/detect/train3/weights/best.pt")

    landfill_results = cls_model(image_path)
    probabilities = landfill_results[0].probs.data.cpu().numpy() 

    # Сохранение вероятностей в переменные
    is_landfill_prob = probabilities[0]
    no_landfill_prob = probabilities[1]

    landfill = (is_landfill_prob > no_landfill_prob)

    print(f"Probability of is-landfill: {is_landfill_prob:.2f}")
    print(f"Probability of no-landfill: {no_landfill_prob:.2f}")

    results = dtc_model(image_path)
    
    detected_objects = []

    img = imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    for result in results[0].boxes:
        class_id = int(result.cls.item())
        class_name = class_names[class_id]
        confidence = result.conf.item()
        bbox = result.xyxy.tolist()

        detected_objects.append(class_name)

        x1, y1, x2, y2 = map(int, bbox[0])

        # Рисуем прямоугольник
        rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Подписываем объект
        label = f"{class_name} {confidence:.2f}"
        putText(img, label, (x1, y1 - 10), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Сохраняем изображение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_image_path = os.path.join(output_dir, f"{name}-analysis{ext}")

    if not imwrite(output_image_path, img):
        raise RuntimeError(f"Failed to save output image: {output_image_path}")

    # Возвращаем результаты
    return {
        "is_landfill_prob": is_landfill_prob,
        "no_landfill_prob": no_landfill_prob,
        "detected_objects": detected_objects,
        "output_image_path": output_image_path,
    }

# print(analyze_image(
#     image_path="test-image.jpg",  # Путь к изображению
# ))