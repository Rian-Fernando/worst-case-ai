import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import sqlalchemy
import datetime
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "sqlite:///conversation_history.db"
database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define your database table for storing conversation history
conversations = sqlalchemy.Table(
    "conversations",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("timestamp", sqlalchemy.String),
    sqlalchemy.Column("cpu_usage", sqlalchemy.Float),
    sqlalchemy.Column("memory_usage", sqlalchemy.Float),
    sqlalchemy.Column("network_traffic", sqlalchemy.Float),
    sqlalchemy.Column("prediction", sqlalchemy.Integer),
    sqlalchemy.Column("description", sqlalchemy.String)
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

app = FastAPI()

model_path = 'models/model.pkl'
encoder_path = 'models/label_encoder.pkl'

with open(model_path, 'rb') as f:
    model = pickle.load(f)

with open(encoder_path, 'rb') as f:
    label_encoder = pickle.load(f)

logging.info("✅ Model and Label Encoder loaded successfully!")

class PredictionRequest(BaseModel):
    cpu_usage: float
    memory_usage: float
    network_traffic: float

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/predict/")
async def predict(data: PredictionRequest):
    input_data = pd.DataFrame([{
        "CPU Usage (%)": data.cpu_usage,
        "Memory Usage (%)": data.memory_usage,
        "Network Traffic (B/s)": data.network_traffic
    }])
    prediction = model.predict(input_data)[0]
    description = "⚠️ Scenario indicates a serious anomaly." if prediction == 1 else "✅ Scenario is normal."

    # Save prediction details to database
    query = conversations.insert().values(
        timestamp=str(datetime.datetime.now()),
        cpu_usage=data.cpu_usage,
        memory_usage=data.memory_usage,
        network_traffic=data.network_traffic,
        prediction=int(prediction),
        description=description
    )
    await database.execute(query)

    return {
        "prediction": int(prediction),
        "description": description
    }

@app.post("/solutions/")
async def solutions(data: PredictionRequest):
    prediction = model.predict(pd.DataFrame([{
        "CPU Usage (%)": data.cpu_usage,
        "Memory Usage (%)": data.memory_usage,
        "Network Traffic (B/s)": data.network_traffic
    }]))[0]

    if prediction == 1:
        solutions = [
            "Restart affected services immediately.",
            "Check and reduce the load on CPU and memory.",
            "Inspect recent network traffic for unusual spikes."
        ]
        resources = [
            "https://docs.system-admin-guides.com/anomaly-handling",
            "https://docs.troubleshoot-cpu-memory.com"
        ]
    else:
        solutions = ["No action required."]
        resources = []

    return {
        "solutions": solutions,
        "resources": resources
    }

@app.get("/")
async def root():
    return {"status": "🚀 API Running!"}