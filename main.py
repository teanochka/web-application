from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
import os
import shutil
import model
import json

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключение папки со статическими файлами
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Возвращаем содержимое index.html
    with open("static/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Маршрут для загрузки
@app.post("/upload")
async def upload_photos(
    photos: List[UploadFile] = File(...),
    confirm: bool = Form(...)
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Подтверждение обязательно")

    # Сохранение изображений
    save_dir = "uploads/"
    os.makedirs(save_dir, exist_ok=True)
    saved_files = []
    for photo in photos:
        file_path = os.path.join(save_dir, photo.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        saved_files.append(file_path)

    # Анализ каждого изображения
    results = []
    for file_path in saved_files:
        analysis_result = model.analyze_image(file_path)
        results.append({
            "output_image_path": analysis_result["output_image_path"],
            "is_landfill_prob": float(analysis_result["is_landfill_prob"]),
            "no_landfill_prob": float(analysis_result["no_landfill_prob"]),
            "detected_objects": analysis_result["detected_objects"],
        })

    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "analysis_log.json")

    with open(log_file, "w", encoding="utf-8") as log:
        json.dump(results, log, ensure_ascii=False, indent=4)

    html_content = "<h1>Результаты анализа</h1>"
    for result in results:
        image_path = result["output_image_path"]
        is_landfill = result["is_landfill_prob"]
        no_landfill = result["no_landfill_prob"]

        if is_landfill > no_landfill:
            status = f"<p><b>Обнаружена свалка</b>, вероятность: {is_landfill:.2f}</p>"
        else:
            status = f"<p><b>Свалки не обнаружено</b>, вероятность: {no_landfill:.2f}</p>"

        html_content += f"""
        <div>
            <img src="{image_path}" alt="Processed Image" style="width:300px;">
            {status}
        </div>
        """
    return HTMLResponse(content=html_content)
