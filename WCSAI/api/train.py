# train.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("datasets/dataset.csv")

# Select features and drop NaNs
X = df[["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)"]]
y = df["Anomaly"]

# Drop rows with any NaNs
df_clean = df[["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)", "Anomaly"]].dropna()
X = df_clean[["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)"]]
y = df_clean["Anomaly"]

# Encode target labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y_encoded)

# Save model and label encoder
joblib.dump(model, "model/model.pkl")
joblib.dump(le, "model/label_encoder.pkl")

print("✅ Cleaned, trained, and saved model + label encoder!")