import pickle
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import logging
from databases import Database
import os

# ====== Logging Setup ======
logging.basicConfig(level=logging.INFO)

# ====== FastAPI Init ======
app = FastAPI()

# ====== CORS Middleware ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====== API Key Protection ======
API_KEY = "rian-secret-key"
API_KEY_NAME = "access-token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="❌ Invalid or missing API Key")

# ====== Database Connection ======
database = Database("sqlite:///./conversation_history.db")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# ====== Load Model and Encoder ======
model_path = "models/model.pkl"
encoder_path = "models/label_encoder.pkl"

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)
    logging.info("✅ Model and Label Encoder loaded successfully!")
except Exception as e:
    logging.error(f"❌ Error loading model or encoder: {e}")
    raise e

# ====== Pydantic Data Model ======
class DataModel(BaseModel):
    CPU_Usage: float
    Memory_Usage: float
    Network_Traffic: float

# ====== Prediction Endpoint ======
@app.post("/predict", dependencies=[Depends(verify_api_key)])
async def predict(data: DataModel):
    try:
        df = pd.DataFrame([{
            "CPU Usage (%)": data.CPU_Usage,
            "Memory Usage (%)": data.Memory_Usage,
            "Network Traffic (B/s)": data.Network_Traffic
        }])

        prediction = model.predict(df)
        prediction_label = encoder.inverse_transform(prediction)[0]

        return {
            "prediction": int(prediction[0]),
            "label": prediction_label
        }

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")