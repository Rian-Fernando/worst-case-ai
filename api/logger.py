import csv
from datetime import datetime
import os

LOG_PATH = "datasets/logged_scenarios.csv"

def log_scenario(input_scenario: str, worst_case: str, solution: str):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    file_exists = os.path.isfile(LOG_PATH)
    
    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "scenario", "worst_case", "solution"])
        writer.writerow([datetime.now().isoformat(), input_scenario, worst_case, solution])