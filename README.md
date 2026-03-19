# TalentLens AI 🚀

TalentLens AI is an AI-powered backend system that evaluates how well a candidate’s resume matches a job description and ranks candidates accordingly.

It simulates a real-world **AI recruiter workflow**, where resumes are analyzed, structured, and scored automatically using LLMs.

---

## 💡 What it does

* Parses job descriptions to extract requirements
* Analyzes resumes to extract candidate profiles
* Compares candidates against job requirements
* Generates:

  * match score (0–100)
  * strengths
  * weaknesses
  * hiring recommendation
* Ranks multiple candidates based on fit

---

## 🧠 Why this project

Most AI projects stop at simple chat interfaces.

This project focuses on:

* building a **multi-step AI system**
* structuring unstructured data (resume → JSON)
* designing a pipeline closer to real-world products

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Language:** Python
* **AI:** Gemini (Google GenAI)
* **Concurrency:** AsyncIO (parallel execution)
* **Validation:** Pydantic

---

## 🏗️ System Design

The system is built as a pipeline of independent steps:

### 1. Job Requirement Extraction

Extracts structured data from job descriptions:

* skills
* tools
* experience

### 2. Candidate Profiling

Extracts structured information from resumes:

* skills
* experience
* projects

### 3. Evaluation Engine

Compares job requirements with candidate data and generates:

* score
* strengths
* weaknesses
* recommendation

### 4. Ranking Engine

* Processes multiple candidates in parallel
* Sorts candidates based on score

---

## ⚡ Key Features

* Async parallel processing using `asyncio.gather`
* Modular AI pipeline design
* Robust handling of inconsistent LLM outputs
* Batch evaluation + ranking system
* Clean API design with FastAPI

---

## 📡 API Endpoints

### Evaluate a single candidate

**POST** `/evaluate`

```json
{
  "resume": "Candidate resume text",
  "job_description": "Job description text"
}
```

---

### Evaluate and rank multiple candidates

**POST** `/evaluate/rank`

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

## 🧪 Run Locally

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

## 🎯 What this project demonstrates

* Designing AI systems beyond simple prompts
* Working with LLM limitations (non-structured outputs)
* Building scalable backend APIs
* Applying concurrency for performance
* Structuring real-world problem pipelines

---

## 🚀 Future Improvements

* Add lightweight frontend for interaction
* Store evaluations in a database
* Improve scoring logic with feedback loops
* Add authentication & user sessions

---

## 📌 Note

This project focuses on system design and backend AI workflows rather than UI, reflecting how real AI-powered services are built.
