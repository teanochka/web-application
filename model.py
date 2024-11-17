from ultralytics import YOLO
from cv2 import imread, imwrite, rectangle, resize, putText, FONT_HERSHEY_SIMPLEX
import os
import yaml

with open("containers.yaml", "r") as f:
    class_names = yaml.safe_load(f)["names"]

def analyze_image(image_path):
    # Загрузка моделей
    cls_model = YOLO("runs/classify/train2/weights/best.pt")
    dtc_model = YOLO("runs/detect/train3/weights/best.pt")

    # Классификация на наличие свалки
    landfill_results = cls_model(image_path)
    probabilities = landfill_results[0].probs.data.cpu().numpy()
    is_landfill_prob = probabilities[0]
    no_landfill_prob = probabilities[1]
    landfill = (is_landfill_prob > no_landfill_prob)

    print(f"Probability of is-landfill: {is_landfill_prob:.2f}")
    print(f"Probability of no-landfill: {no_landfill_prob:.2f}")

    # Обнаружение объектов
    results = dtc_model(image_path)
    detected_objects = []
    container_boxes = []
    plastic_bag_boxes = []

    img = imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    img = resize(img, (640, 640))

    # Анализ объектов
    for result in results[0].boxes:
        class_id = int(result.cls.item())
        class_name = class_names[class_id]
        confidence = result.conf.item()
        bbox = result.xyxy.tolist()

        detected_objects.append(class_name)

        if class_name == "trash-bag":
            plastic_bag_boxes.append((bbox, confidence))
        elif class_name != "trash-bag": 
            container_boxes.append((bbox, confidence))

        x1, y1, x2, y2 = map(int, bbox[0])
        rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_name} {confidence:.2f}"
        putText(img, label, (x1, y1 - 10), FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    def is_intersecting(box1, box2):
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)

    containers_full = False
    for container_bbox, _ in container_boxes:
        for plastic_bag_bbox, _ in plastic_bag_boxes:
            if is_intersecting(container_bbox[0], plastic_bag_bbox[0]):
                containers_full = True
                break
        if containers_full:
            break

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_image_path = os.path.join(output_dir, f"{name}-analysis{ext}")

    if not imwrite(output_image_path, img):
        raise RuntimeError(f"Failed to save output image: {output_image_path}")

    return {
        "containers_full": containers_full,
        "is_landfill_prob": is_landfill_prob,
        "no_landfill_prob": no_landfill_prob,
        "detected_objects": detected_objects,
        "output_image_path": output_image_path,
    }
