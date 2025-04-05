import pandas as pd
import os

# Define dataset path
DATASET_PATH = "datasets"  # Make sure the datasets are inside this folder

# Function to load a dataset
def load_dataset(filename):
    file_path = os.path.join(DATASET_PATH, filename)
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found in {DATASET_PATH}")
        return None
    df = pd.read_csv(file_path)
    print(f"Loaded dataset: {filename}")
    print(df.head())  # Show first 5 rows
    return df

# Example usage
if __name__ == "__main__":
    dataset_name = "dataSynthetic.csv"  # Your dataset file name
    df = load_dataset(dataset_name)
