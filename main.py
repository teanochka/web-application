from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from typing import List
import os
import shutil
import model
import json
import asyncpg
from datetime import datetime
import sys
from datetime import datetime, timedelta

from fastapi.staticfiles import StaticFiles

app = FastAPI()

async def connect_to_db():
    conn = await asyncpg.connect(
        user='postgres',
        password='7001',
        database='hackathon',
        host='localhost'
    )
    return conn

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output", StaticFiles(directory="output"), name="output")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

# Маршрут для загрузки
@app.post("/upload")
async def upload_photos(
    photos: List[UploadFile] = File(...),
    report_landfill: str = Form(...), 
    report_objects: str = Form(""),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    user_landfill = True if report_landfill.lower() == "yes" else False
    user_objects = report_objects

    print(f"Received report_landfill: {user_landfill}")
    print(f"Received report_objects: {user_objects}")
    print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")

    # Сохранение изображений
    save_dir = "uploads/"
    os.makedirs(save_dir, exist_ok=True)
    saved_files = []
    for photo in photos:
        file_path = os.path.join(save_dir, photo.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        saved_files.append(file_path)

    landfills_detected = False

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

    html_content = """
        <h1>Результаты анализа</h1>
        <div style="width:100%; display:grid; grid-template-columns: 1fr 1fr 1fr; gap:50px;">
        """
    for result in results:
        image_path = result["output_image_path"]
        is_landfill = result["is_landfill_prob"]
        no_landfill = result["no_landfill_prob"]

        if is_landfill > no_landfill:
            landfills_detected = True
            status = f"<p><b>Обнаружена свалка</b>, вероятность: {is_landfill:.2f}</p>"
        else:
            status = f"<p><b>Свалки не обнаружено</b>, вероятность: {no_landfill:.2f}</p>"

        html_content += f"""
        <div>
            <img src="{image_path}" alt="Processed Image" style="width:100%;">
            {status}
        </div>
        """

    html_content += """
        </div>
        <br>
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">Вернуться на главную</a>
    """

    if (landfills_detected == user_landfill):
        validation_needed = False
    else:
        validation_needed = True

    images_path_str = ",".join(saved_files)

    conn = await connect_to_db()

    try:
        await conn.execute(
            """
            INSERT INTO container_sites (latitude, longitude, has_landfill, last_disposal_date, description, confirmation_needed, images_path)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            latitude,
            longitude,
            user_landfill,
            datetime.now(),
            user_objects,
            validation_needed,
            images_path_str
        )
    finally:
        await conn.close()  # Закрываем соединение
    return HTMLResponse(content=html_content)

@app.get("/notifications", response_class=HTMLResponse)
async def get_notifications():
    conn = await connect_to_db()
    try:
        query = """
        SELECT id, latitude, longitude, images_path, last_disposal_date, confirmation_needed, has_landfill
        FROM container_sites
        WHERE confirmation_needed = true
           OR (last_disposal_date <= NOW() - INTERVAL '3 days')
           OR (confirmation_needed = false AND has_landfill = true)
        """
        rows = await conn.fetch(query)

        # Генерация HTML
        notifications_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Уведомления</title>
            <style>
                body {
                font-family: Verdana, Geneva, Tahoma, sans-serif;
                }
                .collapsible { 
                cursor: pointer;
                background: none;
                border: none;
                padding: 0;
                outline: none;
                }
                
                .collapsible img {
                width: 24px;
                transition: transform 0.3s;
                }

                .collapsible.active img {
                transform: rotate(180deg);
                }

                .content { display: none; overflow: hidden; }
                img { max-width: 300px; }
                div { margin-bottom: 5px; }
            </style>
        </head>
        <body>
        <div style="display: grid;">
        """
        
        for row in rows:
            pub_id = row["id"]
            latitude = row["latitude"]
            longitude = row["longitude"]
            images_path = row["images_path"]
            last_disposal_date = row["last_disposal_date"]
            confirmation_needed = row["confirmation_needed"]
            has_landfill = row["has_landfill"]

            if not latitude or not longitude:
                print(f"Ошибка: Не удалось сформировать запись по публикации {pub_id}, так как отсутствуют координаты", file=sys.stderr)
                continue

            if not last_disposal_date:
                print(f"Ошибка: Не удалось сформировать запись по публикации {pub_id}, так как отсутствует дата", file=sys.stderr)
                continue

            if confirmation_needed and not images_path:
                print(f"Ошибка: Не удалось сформировать запись по публикации {pub_id}, так как отсутствуют фото", file=sys.stderr)
                continue

            coordinates = f"{latitude} {longitude}"
            date = last_disposal_date.strftime("%Y-%m-%d")

            if confirmation_needed:
                images = images_path.split(',') if images_path else []
                notifications_html += f"""
                <div style="border-radius: 10px; background-color: #bbd7b8; padding: 10px;">
                    <h3>Подтвердите данные</h3>
                    <p style="font-weight: lighter; font-size: small;">Координаты: {coordinates}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <p style="font-weight: bold; font-size: small;">Дата: {date}</p>
                        <button type="button" class="collapsible">
                            <img src="/static/img/arrow-bottom.png" alt="развернуть" />
                        </button>
                    </div>
                    <div class="content">
                        <div style="display: flex; gap: 5px; overflow-x: auto;">
                        {"".join([f'<img style="max-width: 300px;" src="{img}" />' for img in images])}
                        </div>
                        <form action="/update_landfill_status" method="post">
                            <input type="hidden" name="id" value="{pub_id}" />
                            <label>Наличие несанкционированной свалки:</label><br />
                            <label>
                                <input
                                    type="radio"
                                    name="report_landfill"
                                    value="yes"
                                    onchange="enableSubmit();"
                                    required
                                />
                                Да
                            </label>
                            <label>
                                <input
                                    type="radio"
                                    name="report_landfill"
                                    value="no"
                                    onchange="enableSubmit();"
                                    required
                                />
                                Нет
                            </label>
                            <button id="submitBtn" type="submit" disabled>Отправить</button>
                        </form>
                    </div>
                </div>
                """
            elif has_landfill:
                notifications_html += f"""
                <div style="border-radius: 10px; background-color: #efb4a6; padding: 10px;">
                    <h3>Требуется устранение свалки</h3>
                    <p style="font-weight: lighter; font-size: small;">Координаты: {coordinates}</p>
                    <p style="font-weight: bold; font-size: small;">Дата: {date}</p>
                </div>
                """
            else:
                notifications_html += f"""
                <div style="border-radius: 10px; background-color: #f1efbb; padding: 10px;">
                    <h3>На площадке требуется вывоз</h3>
                    <p style="font-weight: lighter; font-size: small;">Координаты: {coordinates}</p>
                    <p style="font-weight: bold; font-size: small;">Дата: {date}</p>
                </div>
                """
        
        notifications_html += """
        </div>
        <script>
        function enableSubmit() {
            const submitButton = document.getElementById("submitBtn");
            submitButton.disabled = false;
        }

        var coll = document.getElementsByClassName("collapsible");

        for (var i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.parentElement.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
            });
        }
        </script>
        </body>
        </html>
        """

        return HTMLResponse(content=notifications_html)
    finally:
        await conn.close()

@app.post("/update_landfill_status")
async def update_landfill_status(
    id: int = Form(...), 
    report_landfill: str = Form(...)
):
    conn = await connect_to_db()
    try:
        has_landfill = True if report_landfill == "yes" else False
        query = """
        UPDATE container_sites
        SET has_landfill = $1, confirmation_needed = false
        WHERE id = $2
        """
        await conn.execute(query, has_landfill, id)
        return {"status": "success", "message": "Данные успешно обновлены"}
    finally:
        await conn.close()
