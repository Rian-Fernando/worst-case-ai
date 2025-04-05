# schemas.py

from pydantic import BaseModel

class PredictRequest(BaseModel):
    feature1: float  # CPU Usage (%)
    feature2: float  # Memory Usage (%)
    feature3: float  # Pod Restarts

class PredictResponse(BaseModel):
    prediction: str