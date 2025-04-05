import pickle
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

logging.basicConfig(level=logging.INFO)

app = FastAPI()

model_path = 'models/model.pkl'
encoder_path = 'models/label_encoder.pkl'

# Load model and encoder
def load_objects():
    try:
        with open(model_path, 'rb') as model_file, open(encoder_path, 'rb') as encoder_file:
            model = pickle.load(model_file)
            label_encoder = pickle.load(encoder_file)
        logging.info("✅ Model and Label Encoder loaded successfully!")
        return model, label_encoder
    except Exception as e:
        logging.error(f"❌ Error loading objects: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

model, label_encoder = load_objects()

class PredictionRequest(BaseModel):
    cpu_usage: float
    memory_usage: float
    network_traffic: float

@app.get("/")
def read_root():
    return {"message": "🚀 Worst-case scenario prediction AI is ready!"}

@app.post("/predict/")
async def predict(request: PredictionRequest):
    try:
        input_data = pd.DataFrame([{
            "CPU Usage (%)": request.cpu_usage,
            "Memory Usage (%)": request.memory_usage,
            "Network Traffic (B/s)": request.network_traffic
        }])

        prediction = model.predict(input_data)[0]
        prediction_label = label_encoder.inverse_transform([prediction])[0]

        description = "✅ Scenario is safe." if prediction_label == 0 else "⚠️ Scenario indicates a serious anomaly."

        response = {
            "prediction": int(prediction),
            "description": description
        }

        logging.info(f"Prediction response: {response}")
        return response

    except Exception as e:
        logging.error(f"❌ Prediction Error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")

# New endpoint for providing solutions
@app.post("/solutions/")
async def solutions(request: PredictionRequest):
    input_data = pd.DataFrame([{
        "CPU Usage (%)": request.cpu_usage,
        "Memory Usage (%)": request.memory_usage,
        "Network Traffic (B/s)": request.network_traffic
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 0:
        return {
            "solutions": ["No immediate action needed. Continue monitoring."],
            "resources": ["https://www.monitoring-guide.com/general-tips"]
        }
    else:
        return {
            "solutions": [
                "Restart affected services immediately.",
                "Check and reduce the load on CPU and memory.",
                "Inspect recent network traffic for unusual spikes."
            ],
            "resources": [
                "https://docs.system-admin-guides.com/anomaly-handling",
                "https://docs.troubleshoot-cpu-memory.com"
            ]
        }