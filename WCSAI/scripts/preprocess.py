import pandas as pd
import os

# Define dataset path
DATASET_PATH = "datasets"
FILENAME = "dataSynthetic.csv"  # Change this if your dataset file has a different name

def preprocess_data(filename):
    """Loads and preprocesses dataset for analysis and training."""
    file_path = os.path.join(DATASET_PATH, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found in {DATASET_PATH}")
        return None

    # Load dataset
    df = pd.read_csv(file_path)

    # Display basic info
    print("Dataset Info:")
    print(df.info())

    # Handle missing values by filling with 0
    df.fillna(0, inplace=True)

    # Convert timestamps to datetime format
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # Drop duplicate entries
    df.drop_duplicates(inplace=True)

    # Show cleaned dataset
    print("\nCleaned Dataset Preview:")
    print(df.head())

    return df

# Run preprocessing when script is executed
if __name__ == "__main__":
    df_cleaned = preprocess_data(FILENAME)
