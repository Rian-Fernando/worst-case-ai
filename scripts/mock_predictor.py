import random

def get_mock_response(scenario: str) -> dict:
    scenario_lower = scenario.lower()

    if "exam" in scenario_lower or "semester" in scenario_lower:
        return {
            "worst_case": "Semester failure resulting in course retake.",
            "solution": "Discuss course retake policies. See if partial credit or alternate assessments can be arranged."
        }
    elif "job" in scenario_lower or "internship" in scenario_lower:
        return {
            "worst_case": "Lost opportunity and delay in career progression.",
            "solution": "Apply to backup roles, improve your resume, and contact recruiters for referrals."
        }
    elif "relationship" in scenario_lower or "friend" in scenario_lower:
        return {
            "worst_case": "Permanent damage to the relationship.",
            "solution": "Communicate openly, apologize if needed, and consider mediation or counseling."
        }
    elif "health" in scenario_lower or "sick" in scenario_lower:
        return {
            "worst_case": "Condition worsens without timely care.",
            "solution": "Seek medical advice immediately. Follow prescribed treatment and rest."
        }
    else:
        return random.choice([
            {
                "worst_case": "Reputational risk or emotional stress.",
                "solution": "Seek help from mentors or professionals, and journal your feelings to clear your head."
            },
            {
                "worst_case": "Short-term failure leading to self-doubt.",
                "solution": "Reflect on lessons learned, talk to someone you trust, and make a recovery plan."
            },
            {
                "worst_case": "Delayed progress on goals.",
                "solution": "Reorganize your timeline and identify what’s still in your control to act on."
            }
        ])