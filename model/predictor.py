# model/predictor.py

import joblib

MODEL_PATH = "model/model.pkl"
ENCODER_PATH = "model/label_encoder.pkl"

# Load model and label encoder
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

def predict(features):
    prediction_encoded = model.predict([features])[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]
    return prediction_label