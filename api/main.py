from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.logger import log_scenario

app = FastAPI()

# Allow all origins (can be restricted to your frontend domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class ScenarioRequest(BaseModel):
    scenario: str

# Root check
@app.get("/")
def read_root():
    return {"message": "Worst-Case AI is up and running 🚀"}

# Main prediction endpoint
@app.post("/predict")
def predict_scenario(request: ScenarioRequest):
    scenario = request.scenario

    try:
        # 🔮 Mocked AI logic (replace with real AI logic when needed)
        if "exam" in scenario.lower():
            worst_case = "Semester failure resulting in course retake."
            solution = "Discuss course retake policies. See if partial credit or alternate assessments can be arranged."
        elif "job" in scenario.lower():
            worst_case = "Lost opportunity and delay in career progression."
            solution = "Apply to backup roles, improve your resume, and contact recruiters for referrals."
        else:
            worst_case = "Unforeseen complications affecting personal or professional life."
            solution = "Seek expert advice, evaluate alternatives, and document everything for future clarity."

        # 📝 Log this scenario + result
        log_scenario(scenario, worst_case, solution)

        return {
            "input_scenario": scenario,
            "worst_case": worst_case,
            "solution": solution
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")