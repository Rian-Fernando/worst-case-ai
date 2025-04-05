from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Allow all CORS origins (you can restrict this later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify frontend URL here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define model and encoder paths
MODEL_PATH = os.path.join("models", "model.pkl")
ENCODER_PATH = os.path.join("models", "label_encoder.pkl")

# Load the model and label encoder
try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    print("✅ Model and Label Encoder loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model or encoder: {e}")
    raise

# Root endpoint (just for checking the backend is up)
@app.get("/")
def read_root():
    return {"message": "Worst-case AI backend is live 🚀"}

# Predict endpoint
@app.post("/predict")
def predict(features: dict):
    try:
        # Ensure required keys exist
        required_keys = ["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)"]
        for key in required_keys:
            if key not in features:
                raise HTTPException(status_code=400, detail=f"Missing input: {key}")

        # Extract and prepare input data
        input_data = [
            features["CPU Usage (%)"],
            features["Memory Usage (%)"],
            features["Network Traffic (B/s)"]
        ]

        # Reshape and predict
        input_array = np.array(input_data).reshape(1, -1)
        prediction = model.predict(input_array)[0]
        decoded_label = label_encoder.inverse_transform([prediction])[0]

        return {"worst_case": decoded_label}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")