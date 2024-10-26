from gettext import install
import pip


pip install fastapi uvicorn # type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import random

app = FastAPI()

class AirQualityData(BaseModel):
    location: str
    pm25: float
    pm10: float
    no2: float
    co: float

def get_db_connection():
    conn = sqlite3.connect('air_quality.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.post("/data/")
async def add_data(data: AirQualityData):
    conn = get_db_connection()
    conn.execute("INSERT INTO air_quality (location, pm25, pm10, no2, co) VALUES (?, ?, ?, ?, ?)",
                 (data.location, data.pm25, data.pm10, data.no2, data.co))
    conn.commit()
    conn.close()
    return {"status": "Data added successfully"}


@app.get("/data/{location}")
async def get_data(location: str):
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM air_quality WHERE location = ?", (location,)).fetchall()
    conn.close()
    if not data:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"data": [dict(row) for row in data]}


@app.get("/suggestions/{location}")
async def get_suggestions(location: str):
    conn = get_db_connection()
    data = conn.execute("SELECT * FROM air_quality WHERE location = ?", (location,)).fetchone()
    conn.close()
    if not data:
        raise HTTPException(status_code=404, detail="Location not found")
    
    
    suggestions = []
    if data["pm25"] > 50:
        suggestions.append("Increase vegetation in this area.")
    if data["no2"] > 30:
        suggestions.append("Reduce industrial emissions.")
    if data["co"] > 10:
        suggestions.append("Encourage use of public transport.")
    
    return {"suggestions": suggestions}

