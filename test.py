# Используйте, когда надо проверить модель на большом количесте данных

import os
import json
from model import analyze_image 
import numpy as np

def convert_to_serializable(result):
    return {
        key: (float(value) if isinstance(value, (float, np.float32)) else value)
        for key, value in result.items()
    }

def process_images(input_folder, output_file):
    results = []
    for file_name in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file_name)

        if not (file_path.lower().endswith((".png", ".jpg", ".jpeg"))):
            continue

        print(f"Processing {file_path}...")

        try:
            result = analyze_image(file_path)
            result["image_path"] = file_path 
            results.append(convert_to_serializable(result))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    input_folder = "uploads"
    output_file = "results.json"

    process_images(input_folder, output_file)
