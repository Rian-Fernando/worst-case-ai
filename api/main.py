import os
import json
import joblib
import datetime
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import databases

# Constants
MODEL_PATH = "models/failure_model.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
DATABASE_URL = "sqlite:///./conversation_history.db"
API_KEY = "rian-secret-key"  # Simple token for now

# Database connection
database = databases.Database(DATABASE_URL)

# FastAPI app setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load model and encoder
try:
    with open(MODEL_PATH, "rb") as f:
        model = joblib.load(f)
    with open(ENCODER_PATH, "rb") as f:
        encoder = joblib.load(f)
    print("✅ Model and Label Encoder loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model or encoder: {e}")
    raise e

# Input schema
class InputData(BaseModel):
    cpu_usage: float
    memory_usage: float
    network_traffic: float

# Connect to DB on startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect from DB on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Prediction route
@app.post("/predict/")
async def predict(data: InputData, access_token: str = Header(...)):
    if access_token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid access token")

    features = [[data.cpu_usage, data.memory_usage, data.network_traffic]]
    prediction = model.predict(features)[0]
    label = encoder.inverse_transform([prediction])[0]

    description = {
        0: "✅ System operating normally.",
        1: "⚠️ Scenario indicates a serious anomaly.",
        2: "🚨 Worst-case failure likely imminent!"
    }.get(prediction, "Unknown result")

    # Save to DB
    user_input = json.dumps(data.dict())
    query = "INSERT INTO predictions (user_input, prediction, description, timestamp) VALUES (:user_input, :prediction, :description, :timestamp)"
    values = {
        "user_input": user_input,
        "prediction": int(prediction),
        "description": description,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    await database.execute(query=query, values=values)

    return {"prediction": int(prediction), "description": description}

# View prediction history
@app.get("/history/")
async def get_history(access_token: str = Header(...)):
    if access_token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid access token")

    query = "SELECT * FROM predictions ORDER BY timestamp DESC"
    rows = await database.fetch_all(query)

    history = [
        {
            "id": row["id"],
            "user_input": row["user_input"],
            "prediction": row["prediction"],
            "description": row["description"],
            "timestamp": row["timestamp"]
        }
        for row in rows
    ]

    return {"history": history}