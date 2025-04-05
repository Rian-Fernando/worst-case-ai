import csv
import os

LOG_FILE = "datasets/scenario_logs.csv"

def log_scenario(scenario: str, worst_case: str, solution: str):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["scenario", "worst_case", "solution"])
        writer.writerow([scenario, worst_case, solution])