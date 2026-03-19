from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import asyncio
import os
import json

# -----------------------------
# Setup
# -----------------------------
load_dotenv()

app = FastAPI(title="TalentLens AI")

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
# Main Evaluation Endpoint
# -----------------------------
@app.post("/evaluate")
async def evaluate_candidate(payload: EvaluationRequest):
    try:
        print("🚀 Starting evaluation...")

        # Run extraction in parallel
        job_data, candidate_data = await asyncio.gather(
            extract_job_requirements(payload.job_description),
            extract_candidate_profile(payload.resume)
        )

        print("✅ Job extracted")
        print("✅ Candidate extracted")

        # Final evaluation (depends on both)
        evaluation_result = await evaluate_match(job_data, candidate_data)

        print("🎯 Evaluation complete")

        return {
            "success": True,
            "data": evaluation_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Step 1: Extract Job Requirements
# -----------------------------
async def extract_job_requirements(job_description: str):
    prompt = f"""
Extract key requirements from this job description.

Return JSON:
{{
  "skills": [],
  "experience": [],
  "tools": []
}}

Job Description:
{job_description}
"""
    return await call_llm(prompt)


# -----------------------------
# Step 2: Extract Candidate Profile
# -----------------------------
async def extract_candidate_profile(resume: str):
    prompt = f"""
Extract candidate details from this resume.

Return JSON:
{{
  "skills": [],
  "experience": [],
  "projects": []
}}

Resume:
{resume}
"""
    return await call_llm(prompt)


# -----------------------------
# Step 3: Evaluate Match
# -----------------------------
async def evaluate_match(job_data: dict, candidate_data: dict):
    prompt = f"""
You are an AI recruiter evaluating a candidate.

Job Requirements:
{json.dumps(job_data, indent=2)}

Candidate Profile:
{json.dumps(candidate_data, indent=2)}

Evaluate the match and return JSON:
{{
  "score": number,
  "strengths": [],
  "weaknesses": [],
  "recommendation": ""
}}
"""
    return await call_llm(prompt)


# -----------------------------
# LLM Call Helper
# -----------------------------
async def call_llm(prompt: str):
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a structured AI recruiter system. Always return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
    )

    return json.loads(response.choices[0].message.content)