from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
import datetime
import shutil
from sqlalchemy import create_engine, Integer, Column, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import model

async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })

app = FastAPI()

DATABASE_URL = "mysql+pymysql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WasteDisposal(Base):
    __tablename__ = "waste_disposals"
    id = Column(Integer, primary_key=True, index=True)
    location_lat = Column(Float, nullable=False)
    location_lng = Column(Float, nullable=False)
    disposal_date = Column(DateTime, default=datetime.datetime.utcnow)
    landfill_detected = Column(Boolean, nullable=False)

Base.metadata.create_all(bind=engine)

# Маршрут для загрузки
@app.post("/upload")
async def upload_photos(
    photos: List[UploadFile] = File(...),
    location_lat: float = Form(...),
    location_lng: float = Form(...),
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

    ai_results = model.process_images(saved_files)
    landfill_detected = ai_results["landfill"]
    cleanliness_score = ai_results["score"]

    # Сохранение данных в БД
    db = SessionLocal()
    disposal = WasteDisposal(
        location_lat=location_lat,
        location_lng=location_lng,
        landfill_detected=landfill_detected
    )
    db.add(disposal)
    db.commit()

    return JSONResponse(content={
        "output_images": ai_results["output_images"],
        "cleanliness_score": cleanliness_score
    })
