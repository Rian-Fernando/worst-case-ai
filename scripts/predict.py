import tensorflow as tf
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load the trained model
MODEL_PATH = "failure_prediction_model.h5"

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logging.info("✅ Model loaded successfully!")
    logging.info(f"Model input shape: {model.input_shape}")
except Exception as e:
    logging.error(f"❌ Failed to load model: {e}")
    exit()

# Simulated input (modify this based on your actual input data)
input_data = np.random.rand(1, 24)  # Adjust shape to match model requirements
logging.info(f"Input data shape: {input_data.shape}")

try:
    prediction = model.predict(input_data)
    rounded_prediction = np.round(prediction, 2)  # Rounding for better readability
    logging.info(f"🔮 Prediction: {rounded_prediction}")
except Exception as e:
    logging.error(f"❌ Prediction error: {e}")
