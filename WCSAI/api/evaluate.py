# evaluate.py

import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load dataset
df = pd.read_csv("datasets/dataset.csv")

# Drop rows with missing values like in training
df = df.dropna()

# Use the same features and label as in training
X = df[["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)"]]
y = df["Anomaly"]  # or "Adjusted_Anomaly" if that's what you prefer

# Load model and label encoder
model = joblib.load("model/model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Encode true labels
y_encoded = label_encoder.transform(y)

# Make predictions
y_pred_encoded = model.predict(X)

# Decode both true and predicted labels
y_pred = label_encoder.inverse_transform(y_pred_encoded)
y_true = label_encoder.inverse_transform(y_encoded)

# Print evaluation results
print("🔍 Evaluation Report:")
print(classification_report(y_true, y_pred))
print(f"✅ Accuracy: {accuracy_score(y_true, y_pred):.4f}")