# TalentLens AI

TalentLens AI is a backend system that evaluates how well a candidate’s resume matches a job description using AI.

Instead of manually screening resumes, this system automatically analyzes candidates, assigns a score, and even ranks multiple candidates — similar to how an AI recruiter would work.

---

## What this project does

* Takes a resume and a job description
* Extracts important skills and requirements
* Compares both using an AI model
* Returns:

  * match score (0–100)
  * strengths
  * weaknesses
  * hiring recommendation

It can also evaluate multiple candidates at once and rank them based on how well they fit the role.

---

## Why I built this

I wanted to understand how AI can be used in real-world systems beyond simple chatbots.

This project simulates an **AI recruiter workflow**, where:

* raw text is converted into structured data
* multiple AI steps are combined into a pipeline
* results are processed and ranked

---

## Tech Stack

* Python
* FastAPI
* Gemini (Google AI)
* AsyncIO (for parallel processing)
* Pydantic

---

## How it works (simple)

The system runs in 3 steps:

1. **Job Analysis**
   Extracts required skills, tools, and experience from the job description

2. **Candidate Analysis**
   Extracts skills, experience, and projects from the resume

3. **Evaluation**
   Compares both and generates a score + feedback

For multiple candidates, everything runs in parallel and gets ranked automatically.

---

## API Endpoints

### Evaluate one candidate

POST `/evaluate`

```json
{
  "resume": "Your resume text",
  "job_description": "Job description text"
}
```

---

### Evaluate and rank multiple candidates

POST `/evaluate/rank`

```json
{
  "resumes": [
    "Resume 1",
    "Resume 2",
    "Resume 3"
  ],
  "job_description": "Job description"
}
```

---

## How to run locally

```bash
git clone <your-repo-url>
cd backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

Run the server:

```bash
uvicorn main:app --reload
```

Open:
http://127.0.0.1:8000/docs

---

## What I focused on

* Building a clean AI pipeline instead of a single API call
* Handling messy AI outputs (JSON parsing issues)
* Running tasks in parallel for better performance
* Designing something close to a real-world use case

---

## Future improvements

* Add a simple frontend UI
* Store results in a database
* Improve scoring logic with feedback loops

---

## Final note

This project is not just about calling an AI model — it's about designing a system around it.
