import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers

# Define dataset path
DATASET_PATH = "datasets"
FILENAME = "dataSynthetic.csv"  # Change this if needed

def load_data(filename):
    """Loads and preprocesses dataset for training."""
    file_path = os.path.join(DATASET_PATH, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found in {DATASET_PATH}")
        return None, None
    
    # Load dataset
    df = pd.read_csv(file_path)

    # Convert timestamps
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # Select relevant features (numerical values)
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns

    # Target variable: Predicting "Pod Restarts" (Failures)
    X = df[numerical_cols].drop(columns=["Pod Restarts"], errors='ignore')
    y = df["Pod Restarts"] if "Pod Restarts" in df.columns else None

    # Handle missing values
    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)

    return X, y

def train_model(X, y):
    """Builds and trains a neural network to predict failures."""
    if y is None:
        print("Error: No target variable found.")
        return
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Define the neural network model
    model = keras.Sequential([
        layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='linear')  # Predicting failure count
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

    # Train the model
    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    # Save model
    model.save("failure_prediction_model.h5")
    print("Model trained and saved successfully!")

# Run training
if __name__ == "__main__":
    X, y = load_data(FILENAME)
    train_model(X, y)
