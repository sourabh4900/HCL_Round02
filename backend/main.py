"""Career PathFinder REST API (Gemini with google.genai)."""

from __future__ import annotations

import os
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import chromadb
import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

try:
    from google import genai
except ImportError:
    genai = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

CHROMA_DIR = PROJECT_ROOT / "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "career_profiles"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

model: SentenceTransformer | None = None
chroma_collection = None
users: dict[str, dict] = {}


class OnboardRequest(BaseModel):
    skills: list[str] = Field(..., min_length=1)
    interests: list[str] = Field(default_factory=list)


class OnboardResponse(BaseModel):
    user_id: str


class RecommendRequest(BaseModel):
    user_id: Optional[str] = None
    skills: Optional[list[str]] = None
    interests: Optional[list[str]] = None


class CareerMatch(BaseModel):
    role: str
    description: str
    required_skills: str
    similarity_score: float


class RecommendResponse(BaseModel):
    careers: list[CareerMatch]


class PathRequest(BaseModel):
    user_id: str
    career: str


class PathResponse(BaseModel):
    career: str
    learning_path: str
    source: str


def average_embedding(texts: list[str]) -> list[float]:
    if model is None:
        raise RuntimeError("Embedding model is not loaded.")
    if not texts:
        raise ValueError("At least one skill or interest is required.")
    vectors = model.encode(texts)
    mean_vector = np.mean(vectors, axis=0)
    return mean_vector.tolist()


def distance_to_similarity(distance: float) -> float:
    return round(max(0.0, 1.0 - (distance**2) / 2.0), 4)


def resolve_user_profile(payload: RecommendRequest) -> tuple[list[str], list[str]]:
    if payload.user_id:
        profile = users.get(payload.user_id)
        if profile is None:
            raise HTTPException(status_code=404, detail="User not found.")
        return profile["skills"], profile["interests"]
    if payload.skills:
        return payload.skills, payload.interests or []
    raise HTTPException(
        status_code=400,
        detail="Provide either user_id or a non-empty skills list.",
    )


def build_profile_text(skills: list[str], interests: list[str]) -> list[str]:
    profile_parts = [part.strip() for part in skills + interests if part.strip()]
    if not profile_parts:
        raise HTTPException(status_code=400, detail="Profile must include skills or interests.")
    return profile_parts


def query_career_matches(profile_texts: list[str], limit: int = 5) -> list[CareerMatch]:
    if chroma_collection is None:
        raise RuntimeError("Chroma collection is not loaded.")
    query_embedding = average_embedding(profile_texts)
    results = chroma_collection.query(
        query_embeddings=[query_embedding],
        n_results=min(limit * 4, 40),
        where={"type": "career"},
        include=["metadatas", "distances"],
    )
    careers: list[CareerMatch] = []
    seen_roles: set[str] = set()
    for metadata, distance in zip(results["metadatas"][0], results["distances"][0]):
        role = metadata.get("role", "")
        if not role or role in seen_roles:
            continue
        seen_roles.add(role)
        careers.append(
            CareerMatch(
                role=role,
                description=metadata.get("description", ""),
                required_skills=metadata.get("required_skills", ""),
                similarity_score=distance_to_similarity(float(distance)),
            )
        )
        if len(careers) >= limit:
            break
    return careers


# Improved mock – same as before (kept for fallback)
def mock_learning_path(career: str, skills: list[str], interests: list[str]) -> str:
    skill_summary = ", ".join(skills) if skills else "your current skills"
    interest_summary = ", ".join(interests) if interests else "your interests"
    highlight = ", ".join(skills[:3]) if skills else "your foundational skills"

    career_info = {
        "Business Intelligence Analysts": {
            "courses": [
                "Google Data Analytics Professional Certificate – Coursera",
                "Microsoft Power BI Data Analyst (PL-300) – Microsoft Learn",
                "SQL for Data Science – Coursera",
                "Tableau Business Intelligence – Udemy"
            ],
            "projects": [
                "Build a sales dashboard using Power BI with real-world data.",
                "Write complex SQL queries to extract insights from a retail database.",
                "Create an interactive Tableau story for executive decision-making.",
                "Automate a weekly reporting pipeline using Python and SQL."
            ],
            "certs": ["Microsoft PL-300", "Tableau Desktop Specialist", "Google Data Analytics"]
        },
        "Data Scientists": {
            "courses": [
                "Machine Learning A-Z – Udemy",
                "Python for Data Science – Coursera",
                "Deep Learning Specialization – Coursera",
                "Kaggle Learn – Machine Learning"
            ],
            "projects": [
                "Predict customer churn using logistic regression.",
                "Build a recommendation system with collaborative filtering.",
                "Perform sentiment analysis on product reviews.",
                "Deploy a ML model as a REST API using FastAPI."
            ],
            "certs": ["Google Professional ML Engineer", "AWS Machine Learning Specialty"]
        },
        "Web Developers": {
            "courses": [
                "The Complete Web Developer Bootcamp – Udemy",
                "CS50 Web Programming – edX",
                "React – The Complete Guide – Udemy",
                "Node.js & Express – Coursera"
            ],
            "projects": [
                "Build a full‑stack e‑commerce site with React and Node.",
                "Create a real‑time chat app using WebSockets.",
                "Develop a blog platform with user authentication.",
                "Deploy a serverless web app on AWS."
            ],
            "certs": ["AWS Certified Developer", "MongoDB Developer"]
        },
        "Graphic Designers": {
            "courses": [
                "Graphic Design Specialization – Coursera",
                "Adobe Photoshop CC – Udemy",
                "Illustrator for Beginners – LinkedIn Learning",
                "UI/UX Design – Google UX Design Certificate"
            ],
            "projects": [
                "Create a brand identity package (logo, business cards, style guide).",
                "Design a responsive website mockup in Figma.",
                "Produce a series of social media graphics for a fictional brand.",
                "Redesign a mobile app interface with a focus on usability."
            ],
            "certs": ["Adobe Certified Associate", "Google UX Design Certificate"]
        },
        "Natural Sciences Managers": {
            "courses": [
                "Project Management for Scientists – Coursera",
                "Leadership in Science & Technology – edX",
                "Data Management for Research – Udemy",
                "Research Lab Management – LinkedIn Learning"
            ],
            "projects": [
                "Develop a research project proposal with budget and timeline.",
                "Create a data management plan for a multi‑year study.",
                "Build a dashboard to track laboratory KPIs.",
                "Write a case study on managing a cross‑functional scientific team."
            ],
            "certs": ["Project Management Professional (PMP)", "Certified Research Administrator"]
        }
    }

    info = career_info.get(career, {})
    courses = info.get("courses", [
        f"Introduction to {career} – Coursera",
        f"Foundations of {career} – Udemy",
        f"Advanced {career} Tools – LinkedIn Learning"
    ])
    projects = info.get("projects", [
        f"Build a project that solves a problem related to {career}",
        f"Create a portfolio piece showcasing your {highlight} skills",
        f"Develop a case study or prototype for {career} role"
    ])
    certs = info.get("certs", [f"Industry‑recognised {career} certification"])

    return f"""
## 🧭 6-Month Learning Path: {career}

### Your starting point
- **Current skills:** {skill_summary}
- **Interests:** {interest_summary}
- **Goal:** Transition into a {career} role by building practical, job‑ready skills.

---

### Month 1 – Foundations
**Focus:** Build the core knowledge required for {career}.
- **Courses:** {courses[0]}, {courses[1]}
- **Projects:** {projects[0]}
- **Soft skills:** Practice giving and receiving constructive feedback on your work.
- **Milestone:** Complete the first course and a small portfolio artifact.

---

### Month 2 – Applied Practice
**Focus:** Apply your {highlight} skills in a real‑world context.
- **Projects:** {projects[1]}
- **Networking:** Join a community or forum for {career} professionals.
- **Milestone:** Publish project #1 with a demo and reflection notes.

---

### Month 3 – Tooling & Workflow
**Focus:** Master the tools commonly used by {career}s.
- **Courses:** {courses[2]}
- **Activity:** Contribute to an open‑source project or collaborate with a peer.
- **Workflow:** Automate a repetitive task.
- **Milestone:** Deliver a working automation or workflow improvement.

---

### Month 4 – Intermediate Depth
**Focus:** Deepen your expertise and start building a professional network.
- **Courses:** One advanced course and one industry‑recognised certification module ({certs[0]}).
- **Networking:** Conduct 3 informational interviews with professionals in {career}.
- **Projects:** {projects[2]}
- **Milestone:** Complete the advanced course and finalise the second project.

---

### Month 5 – Interview & Portfolio Readiness
**Focus:** Prepare for job applications and interviews.
- **Resume & LinkedIn:** Tailor your CV and profile to highlight {career}-relevant skills and projects.
- **Mock interviews:** Practice with a peer or use platforms like Pramp / Interviewing.io.
- **Portfolio:** Polish your portfolio site with 3 projects and a 2‑minute pitch video.
- **Milestone:** Have a ready‑to‑share portfolio and a set of tailored application materials.

---

### Month 6 – Job Transition
**Focus:** Actively apply for roles and prepare for your first weeks on the job.
- **Applications:** Apply to 5–10 targeted roles per week; track responses and feedback.
- **Capstone:** Complete an end‑to‑end project that simulates real on‑the‑job deliverables for a {career}.
- **On‑boarding plan:** Create a 90‑day learning plan for your first role.
- **Milestone:** Submit your application packet and receive at least one interview or callback.

> 💡 **Tip:** Your existing {highlight} skills give you a strong head start. Focus on projects that demonstrate how you can apply those skills to solve {career}‑specific problems. Good luck!
"""


def generate_learning_path(career: str, skills: list[str], interests: list[str]) -> tuple[str, str]:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_key_here" or genai is None:
        return mock_learning_path(career, skills, interests), "mock"

    skill_str = ", ".join(skills) if skills else "none yet"
    interest_str = ", ".join(interests) if interests else "none yet"

    prompt = f"""You are a career coach and learning path designer.

The user wants to become a **{career}**.
Their current skills are: {skill_str}.
Their interests are: {interest_str}.

Create a personalised 6‑month learning roadmap. 
- Break it down month by month.
- For each month, list specific courses (with real platform names like Coursera, Udemy, edX), projects, and milestones.
- Include soft skills and portfolio‑building activities.
- Make it practical and actionable.
- Reference the user's existing skills and show how they connect to the target career.
- Keep the tone encouraging and supportive.

Format the output as clear sections with month headings and bullet points.
"""

    try:
        # Keep the client scoped to this request so reloads cannot reuse a closed client.
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
        content = response.text.strip()
        if not content:
            return mock_learning_path(career, skills, interests), "mock"
        return content, "gemini"
    except Exception as e:
        print(f"Gemini error: {e}")
        return mock_learning_path(career, skills, interests), "mock"


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model, chroma_collection
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    chroma_collection = client.get_or_create_collection(COLLECTION_NAME)
    yield
    model = None
    chroma_collection = None


app = FastAPI(title="Career PathFinder API", version="1.0.0", lifespan=lifespan)

# --- CORS ---
# In production set CORS_ORIGINS to the deployed frontend URL, e.g.
#   CORS_ORIGINS=https://pathfinder.example.com
# For local development the Vite proxy handles CORS, but we allow all
# origins by default so the production frontend can call the API directly.
_origins = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins.split(",") if _origins != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/onboard", response_model=OnboardResponse)
def onboard(payload: OnboardRequest) -> OnboardResponse:
    user_id = str(uuid.uuid4())
    users[user_id] = {"skills": payload.skills, "interests": payload.interests}
    return OnboardResponse(user_id=user_id)


@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
    skills, interests = resolve_user_profile(payload)
    profile_texts = build_profile_text(skills, interests)
    careers = query_career_matches(profile_texts, limit=5)
    return RecommendResponse(careers=careers)


@app.post("/path", response_model=PathResponse)
def path(payload: PathRequest) -> PathResponse:
    profile = users.get(payload.user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User not found.")
    learning_path, source = generate_learning_path(
        career=payload.career,
        skills=profile["skills"],
        interests=profile["interests"],
    )
    return PathResponse(career=payload.career, learning_path=learning_path, source=source)