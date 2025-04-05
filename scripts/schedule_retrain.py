import sys
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging

# Set up logging to capture debug messages
logging.basicConfig(filename='retrain_model.log', level=logging.DEBUG)

# Add scripts to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from retrain_model import retrain_model  # Import the retrain function from retrain_model.py

# Function to retrain model
def retrain_model_periodically():
    logging.debug("📚 Retraining model on new scenarios...")
    retrain_model()  # Call the retrain function (already created in retrain_model.py)
    logging.debug("✅ Model retrained and saved.")

# Start the scheduler and schedule retraining every 24 hours
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(retrain_model_periodically, 'interval', days=1)  # Retrain every day
    scheduler.start()
    print("Scheduler started...")  # Confirm that the scheduler is running

# Keep the scheduler running
if __name__ == "__main__":
    start_scheduler()
    while True:
        time.sleep(1)  # Keep the scheduler running indefinitely