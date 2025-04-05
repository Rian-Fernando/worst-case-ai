import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("datasets/dataset.csv")

# Features and label
X = df[["CPU Usage (%)", "Memory Usage (%)", "Pod Restarts"]]
y = df["Pod Status"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Load trained model
model = joblib.load("model/model.pkl")

# Predict and evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy on test set: {acc:.4f}")

