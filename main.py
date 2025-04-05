# main.py

from fastapi import FastAPI
from model.predictor import predict
from schemas import PredictRequest, PredictResponse

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Worst Case AI API is live!"}

@app.post("/predict", response_model=PredictResponse)
def get_prediction(data: PredictRequest):
    features = [data.feature1, data.feature2, data.feature3]
    print("💡 Features received:", features)
    prediction = predict(features)
    return PredictResponse(prediction=prediction)