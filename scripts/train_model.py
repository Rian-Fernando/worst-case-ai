import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

FILENAME = "datasets/dataSynthetic.csv"

def load_data(filepath):
    df = pd.read_csv(filepath)
    df.dropna(inplace=True)

    X = df[["CPU Usage (%)", "Memory Usage (%)", "Network Traffic (B/s)"]]
    y = df["Adjusted_Anomaly"]

    return X, y

def train_model(X, y):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    model = LogisticRegression(max_iter=1000, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("Model evaluation:")
    print(classification_report(y_test, predictions))

    return model, label_encoder

def save_model(model, encoder):
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open("models/label_encoder.pkl", "wb") as f:
        pickle.dump(encoder, f)

if __name__ == "__main__":
    X, y = load_data(FILENAME)
    model, encoder = train_model(X, y)
    save_model(model, encoder)