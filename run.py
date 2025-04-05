import argparse
import subprocess
import os

def train():
    print("🧠 Training model...")
    subprocess.run(["python3", "scripts/train_model.py"])

def evaluate():
    print("📊 Evaluating model...")
    subprocess.run(["python3", "api/evaluate.py"])

def serve():
    print("🚀 Starting API server at http://127.0.0.1:8000/docs ...")
    subprocess.run(["uvicorn", "api.main:app", "--reload"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run WCSAI project tasks.")
    parser.add_argument("mode", choices=["train", "eval", "serve"], help="Select a mode: train, eval, or serve")

    args = parser.parse_args()

    if args.mode == "train":
        train()
    elif args.mode == "eval":
        evaluate()
    elif args.mode == "serve":
        serve()