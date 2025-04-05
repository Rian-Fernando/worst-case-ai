# api/main.py

from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import numpy as np
import joblib
import os
import sqlite3

app = FastAPI()

# Load the trained model and encoder
model_path = "models/logistic_model.pkl"
encoder_path = "models/label_encoder.pkl"

try:
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    print("✅ Model and Label Encoder loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or encoder: {e}")
    raise e

# Input model
class InputData(BaseModel):
    cpu_usage: float
    memory_usage: float
    network_traffic: float

# API Key verification
API_KEY = "rian-secret-key"

@app.post("/predict/")
async def predict(data: InputData, access_token: str = Header(...)):
    if access_token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # Convert input to numpy array
        features = np.array([[data.cpu_usage, data.memory_usage, data.network_traffic]])
        prediction = model.predict(features)[0]
        decoded = encoder.inverse_transform([prediction])[0]

        # Description
        description = (
            "✅ Scenario looks stable."
            if prediction == 0
            else "⚠️ Scenario indicates a serious anomaly."
        )

        # Save to database
        conn = sqlite3.connect("conversation_history.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversation_history (user_input, prediction, description)
            VALUES (?, ?, ?)
        ''', (f"{data.dict()}", int(prediction), description))
        conn.commit()
        conn.close()

        return {"prediction": int(prediction), "description": description}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/")
async def get_history(access_token: str = Header(...)):
    if access_token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        conn = sqlite3.connect("conversation_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversation_history ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()

        # Format as list of dicts
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "user_input": row[1],
                "prediction": row[2],
                "description": row[3],
                "timestamp": row[4],
            })
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))