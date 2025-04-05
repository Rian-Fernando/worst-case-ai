# train.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
df = pd.read_csv("datasets/dataset.csv")

# Features and target
X = df[["CPU Usage (%)", "Memory Usage (%)", "Pod Restarts"]]
y_raw = df["Pod Status"]

# Encode the labels
le = LabelEncoder()
y = le.fit_transform(y_raw)

# Train the model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save model and label encoder
joblib.dump(model, "model/model.pkl")
joblib.dump(le, "model/label_encoder.pkl")

print("✅ Model and label encoder saved!")