from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Load the trained ML model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'failure_prediction_model.h5')
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Could not load model: {e}")

# Input format for prediction
class PredictionInput(BaseModel):
    data: list[list[float]]

# Input format for journaling
class JournalEntry(BaseModel):
    entry: str

@app.get("/")
def home():
    return {"message": "WCSAI is live!"}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        array = np.array(input_data.data)
        predictions = model.predict(array)
        return {"predictions": predictions.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
def analyze(entry: JournalEntry):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a helpful mental health assistant."},
                {"role": "user", "content": f"Analyze the mood, give a short summary, and suggest one positive coping strategy based on this journal entry:\n\n{entry.entry}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        reply = response.choices[0].message.content
        return {"analysis": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
