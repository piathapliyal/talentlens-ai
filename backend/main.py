from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# Load environment variables
load_dotenv()

# Initialize app
app = FastAPI(title="TalentLens AI")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# Request Schema
# -----------------------------
class EvaluationRequest(BaseModel):
    resume: str
    job_description: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "TalentLens AI running"}


# -----------------------------
# AI Evaluation Endpoint
# -----------------------------
@app.post("/evaluate")
def evaluate_candidate(payload: EvaluationRequest):
    try:
        prompt = build_prompt(payload.resume, payload.job_description)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You are a precise AI recruiter."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content

        # Try parsing response into JSON
        parsed = safe_parse_json(content)

        return {
            "success": True,
            "data": parsed if parsed else content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Prompt Builder (clean separation)
# -----------------------------
def build_prompt(resume: str, job_description: str) -> str:
    return f"""
You are an AI recruiter evaluating a candidate.

Follow these steps:
1. Extract key requirements from the job description
2. Analyze the candidate's resume
3. Compare candidate skills with job requirements
4. Assign a score from 0 to 100
5. Provide strengths, weaknesses, and a hiring recommendation

Return ONLY valid JSON in this format:
{{
  "score": number,
  "strengths": ["..."],
  "weaknesses": ["..."],
  "recommendation": "..."
}}

Job Description:
{job_description}

Resume:
{resume}
"""


# -----------------------------
# JSON Safety Parser
# -----------------------------
def safe_parse_json(content: str):
    try:
        return json.loads(content)
    except Exception:
        return None