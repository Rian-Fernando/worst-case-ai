import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define dataset path
DATASET_PATH = "datasets"
FILENAME = "dataSynthetic.csv"  # Change this if needed

def load_and_visualize_data(filename):
    """Loads dataset and generates key visualizations."""
    file_path = os.path.join(DATASET_PATH, filename)
    
    if not os.path.exists(file_path):
        print(f"Error: {filename} not found in {DATASET_PATH}")
        return None

    # Load dataset
    df = pd.read_csv(file_path)

    # Convert timestamps
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    # Set plot style
    sns.set(style="whitegrid")

    # Plot CPU Usage Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["CPU Usage (%)"], bins=50, kde=True, color="blue")
    plt.title("CPU Usage Distribution")
    plt.xlabel("CPU Usage (%)")
    plt.ylabel("Frequency")
    plt.savefig("cpu_usage_distribution.png")
    plt.show()

    # Plot Memory Usage Distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Memory Usage (%)"], bins=50, kde=True, color="green")
    plt.title("Memory Usage Distribution")
    plt.xlabel("Memory Usage (%)")
    plt.ylabel("Frequency")
    plt.savefig("memory_usage_distribution.png")
    plt.show()

    # Plot Failures Over Time
    plt.figure(figsize=(12, 6))
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df.set_index("Timestamp")["Pod Restarts"].resample("D").sum().plot(kind="line", color="red")
    plt.title("Pod Restarts Over Time")
    plt.xlabel("Date")
    plt.ylabel("Total Restarts")
    plt.grid(True)
    plt.savefig("pod_restarts_over_time.png")
    plt.show()

# Run visualization
if __name__ == "__main__":
    load_and_visualize_data(FILENAME)
