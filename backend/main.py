from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from pathlib import Path
import asyncio
import os
import json

# -----------------------------
# Setup
# -----------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="TalentLens AI")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))




# -----------------------------
# Request Schemas
# -----------------------------
class EvaluationRequest(BaseModel):
    resume: str
    job_description: str


class BatchEvaluationRequest(BaseModel):
    resumes: list[str]
    job_description: str


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "TalentLens AI running"}


# -----------------------------
# Single Candidate Evaluation
# -----------------------------
@app.post("/evaluate")
async def evaluate_candidate(payload: EvaluationRequest):
    try:
        print("Starting evaluation...")

        # Run extraction in parallel
        job_data, candidate_data = await asyncio.gather(
            extract_job_requirements(payload.job_description),
            extract_candidate_profile(payload.resume)
        )

        print("Extraction complete")

        # Final evaluation
        evaluation = await evaluate_match(job_data, candidate_data)

        print("Evaluation complete")

        return {
            "success": True,
            "data": evaluation
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Batch Evaluation + Ranking
# -----------------------------
@app.post("/evaluate/rank")
async def evaluate_and_rank(payload: BatchEvaluationRequest):
    try:
        print(f"Evaluating {len(payload.resumes)} candidates")

        # Extract job requirements once
        job_data = await extract_job_requirements(payload.job_description)

        # Process all candidates in parallel
        tasks = [
            process_candidate(resume, job_data)
            for resume in payload.resumes
        ]

        results = await asyncio.gather(*tasks)

        # Sort by score safely
        ranked = sorted(
            results,
            key=lambda x: float(x.get("score", 0)),
            reverse=True
        )

        return {
            "success": True,
            "top_candidate": ranked[0] if ranked else None,
            "ranked_candidates": ranked
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# AI Pipeline Steps
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


async def evaluate_match(job_data: dict, candidate_data: dict):
    prompt = f"""
You are an AI recruiter evaluating a candidate.

Job Requirements:
{json.dumps(job_data, indent=2)}

Candidate Profile:
{json.dumps(candidate_data, indent=2)}

Return JSON:
{{
  "score": number,
  "strengths": [],
  "weaknesses": [],
  "recommendation": ""
}}
"""
    return await call_llm(prompt)


async def process_candidate(resume: str, job_data: dict):
    candidate_data = await extract_candidate_profile(resume)
    return await evaluate_match(job_data, candidate_data)


# -----------------------------
# LLM Helper (Gemini)
# -----------------------------
async def call_llm(prompt: str):
    """
    Executes Gemini call safely and extracts valid JSON from response.
    """
    loop = asyncio.get_running_loop()

    def _make_request():
         response = client.models.generate_content(
         model="gemini-2.5-flash",
         contents=prompt,
         )
         return response.text 

    try:
        raw_output = await loop.run_in_executor(None, _make_request)

        cleaned = raw_output.strip()

        # Remove markdown blocks if present
        if "```" in cleaned:
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()

        # Extract JSON portion
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1

        if start == -1 or end == -1:
            raise ValueError("No valid JSON found in response")

        json_str = cleaned[start:end]

        return json.loads(json_str)

    except Exception as e:
        print("Gemini parsing failed:", str(e))
        print("Raw output:", raw_output)
        raise