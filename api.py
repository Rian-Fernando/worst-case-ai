from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Tuple
from openai import OpenAI
import os

# Load API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Allow CORS (for frontend use later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class MessageRequest(BaseModel):
    message: str

# Categories (optional if you want future classification)
categories = [
    "Financial loss",
    "Legal issues",
    "Reputation damage",
    "Operational failure",
    "Security breach"
]

# Function to ask OpenAI and get worst-case + solution
def get_openai_worst_case_and_solution(message: str) -> Tuple[str, str]:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're a Worst-Case Scenario AI. Predict the worst-case outcome of any situation "
                        "and provide a thoughtful, practical solution. Format your response like this:\n\n"
                        "Worst-case: <summary>\nSolution: <detailed advice>"
                    )
                },
                {"role": "user", "content": message}
            ],
            temperature=0.8,
            max_tokens=500
        )

        full_reply = response.choices[0].message.content.strip()

        # Attempt to parse it
        if "Worst-case:" in full_reply and "Solution:" in full_reply:
            try:
                worst_case = full_reply.split("Worst-case:")[1].split("Solution:")[0].strip()
                solution = full_reply.split("Solution:")[1].strip()
            except Exception:
                worst_case = "Could not parse"
                solution = full_reply
        else:
            worst_case = "Could not parse"
            solution = full_reply

        return worst_case, solution

    except Exception as e:
        return "Error calling OpenAI", str(e)

# Prediction endpoint with full debug
@app.post("/predict")
async def predict(request: MessageRequest):
    try:
        message = request.message
        worst_case, solution = get_openai_worst_case_and_solution(message)

        return {
            "prediction": worst_case,
            "suggested_solution": solution
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Optional root endpoint
@app.get("/")
def read_root():
    return {"message": "Worst-Case Scenario AI is running."}
