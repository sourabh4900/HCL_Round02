<![CDATA[<div align="center">

# 🧭 Career PathFinder
 
### AI-Powered Career Guidance & Personalised Learning Roadmaps

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-4.3-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-FF6F00)](https://www.trychroma.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

**Enter your skills → Get AI-matched career recommendations → Receive a personalised 6-month learning roadmap.**

[Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture) · [API Reference](#-api-reference) · [Data Pipeline](#-data-pipeline)

</div>

---

## 📖 Overview

Career PathFinder is a full-stack web application that bridges the gap between *"I have these skills"* and *"here's a concrete plan to reach that career."* Users enter their skills and interests, and the system uses **semantic vector search** (sentence-transformer embeddings stored in ChromaDB) to match them against **1,000+ real-world occupations** sourced from the U.S. Department of Labor's **O\*NET** database. For each recommended career, the app generates a **personalised 6-month learning path** — either via **Google Gemini AI** or via a built-in template engine as a fallback.

### Who Is This For?

| Audience | Use Case |
|---|---|
| 🎓 **Students** | Discover career paths aligned with their coursework |
| 💼 **Professionals** | Plan a data-driven career pivot |
| 🔍 **Job Seekers** | Get personalised recommendations, not generic advice |
| 🧑‍🏫 **Career Counsellors** | Augment their practice with AI-powered tools |

---

## ✨ Features

- **Semantic Career Matching** — Uses NLP embeddings (`all-MiniLM-L6-v2`) instead of keyword search, so "machine learning" and "deep learning" are recognised as related
- **1,017 Real-World Occupations** — Sourced from the U.S. O\*NET database with 8,920 associated skills
- **AI-Generated Learning Paths** — Google Gemini produces personalised 6-month roadmaps with real courses, projects, and milestones
- **Graceful Degradation** — Works without a Gemini API key by falling back to detailed template-based learning paths
- **Modern UI** — React 19 + Tailwind CSS 4 with custom typography (DM Sans, Space Grotesk), smooth animations, and responsive design
- **Fast & Lightweight** — ChromaDB vector search returns recommendations in seconds; Vite provides instant HMR during development

---

## 🏗 Architecture

Career PathFinder follows a **three-tier architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ☁️  External Services                        │
│  ┌──────────────────────┐    ┌──────────────────────────────┐  │
│  │  HuggingFace API     │    │  Google Gemini API            │  │
│  │  (Sentence Embeddings│    │  (Learning Path Generation)   │  │
│  └──────────┬───────────┘    └──────────────┬───────────────┘  │
└─────────────┼───────────────────────────────┼──────────────────┘
              │                               │
┌─────────────┼───────────────────────────────┼──────────────────┐
│  ⚙️  Backend│(FastAPI — port 8000)          │                  │
│  ┌──────────┴───────────────────────────────┴───────────────┐  │
│  │  REST API: /onboard · /recommend · /path · /health       │  │
│  │  Pydantic Models · Embedding Logic · LLM Integration     │  │
│  └──────────┬───────────────────────────────────────────────┘  │
│             │                                                   │
│  ┌──────────┴──────────┐    ┌────────────────────────────────┐ │
│  │  In-Memory Users    │    │  ChromaDB (chroma_db/)          │ │
│  │  (dict)             │    │  1,017 careers + 8,920 skills   │ │
│  └─────────────────────┘    └────────────────────────────────┘ │
└────────────────────────────────────┬───────────────────────────┘
                                     │  HTTP (Axios via Vite proxy)
┌────────────────────────────────────┴───────────────────────────┐
│  🖥️  Frontend (React SPA — port 5173)                          │
│  Landing → Onboarding → Recommendations → Learning Path        │
│  React 19 · Vite 8 · Tailwind CSS 4 · react-markdown           │
└────────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Onboarding** — User enters skills and selects interest areas
2. **Embedding** — Skills/interests are sent to the HuggingFace Inference API, which returns 384-dim vectors
3. **Vector Search** — Vectors are averaged and compared against pre-computed career embeddings in ChromaDB
4. **Recommendations** — Top 5 career matches are returned with similarity scores (0–100%)
5. **Learning Path** — When the user selects a career, Gemini generates a personalised 6-month roadmap (or a template-based fallback is used)

---

## 📂 Project Structure

```
hcl_round2/
├── .env                          # API keys (git-ignored)
├── .env.example                  # Template — copy this to .env
├── .gitignore
├── requirements.txt              # Python dependencies
│
├── backend/
│   └── main.py                   # FastAPI app (routes, models, AI logic)
│
├── data/
│   ├── occupation_data.csv       # O*NET occupations (1,017 roles)
│   ├── essential_skills.csv      # O*NET essential skills
│   ├── transferable_skills.csv   # O*NET transferable skills
│   ├── software_skills.csv       # O*NET software/tools
│   ├── careers.csv               # Processed: role + description + skills
│   ├── skills.csv                # Processed: deduplicated skill list (8,920)
│   └── courses.csv               # Synthetic course catalog
│
├── scripts/
│   ├── prepare_data.py           # ETL: raw O*NET → processed CSVs
│   └── embedding.py              # Builds ChromaDB vector index
│
├── chroma_db/                    # Pre-built vector index (~14 MB)
│
└── frontend/
    ├── index.html                # HTML entry point
    ├── package.json              # Node.js dependencies
    ├── vite.config.js            # Vite config (dev proxy, plugins)
    ├── public/
    │   ├── favicon.svg
    │   └── icons.svg
    └── src/
        ├── main.jsx              # React entry point
        ├── App.jsx               # Root component & routing
        ├── api.js                # Axios API client
        ├── index.css             # Global styles & Tailwind import
        └── components/
            ├── Landing.jsx       # Hero page with CTA
            ├── Onboarding.jsx    # Skills & interests input form
            ├── Recommendations.jsx  # Career match cards
            └── PathView.jsx      # 6-month learning path viewer
```

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.10+ | Backend runtime |
| **Node.js** | 18+ | Frontend build tooling |
| **npm** | 9+ | Package management |
| **Git** | Any | Clone the repo |

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hcl_round2
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```dotenv
# Required — powers career recommendations
HUGGINGFACE_API_KEY=hf_your_token_here

# Optional — enables AI-generated learning paths (falls back to templates without it)
GEMINI_API_KEY=your_gemini_api_key_here
```

> **Where to get keys:**
> - **HuggingFace**: [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (free tier works)
> - **Gemini**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 3. Install & Start the Backend

```bash
pip install -r requirements.txt

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Install & Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Open the App

Navigate to **[http://localhost:5173](http://localhost:5173)** in your browser. 🎉

---

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `HUGGINGFACE_API_KEY` | **Yes** | `""` | HuggingFace Inference API token for embedding computation |
| `GEMINI_API_KEY` | No | `""` | Google Gemini API key. If absent, template-based learning paths are used |
| `GEMINI_MODEL` | No | `gemini-3.6-flash` | Override the Gemini model name |
| `CORS_ORIGINS` | No | `*` | Comma-separated allowed origins. Restrict in production |
| `VITE_API_URL` | No | `/api` | Backend URL for the frontend in production builds |

> ⚠️ **Never commit `.env` to version control.** It is already listed in `.gitignore`.

---

## 📡 API Reference

The backend runs at `http://127.0.0.1:8000`. All endpoints accept and return JSON.

### `GET /health`

Health check / readiness probe.

**Response:**
```json
{ "status": "ok" }
```

---

### `POST /onboard`

Register a new user profile with skills and interests.

**Request Body:**
```json
{
  "skills": ["Python", "SQL", "Data Analysis"],
  "interests": ["Data Science", "Software Engineering"]
}
```

**Response:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

| Field | Type | Constraints |
|---|---|---|
| `skills` | `list[str]` | **Required**, min 1 item |
| `interests` | `list[str]` | Optional, defaults to `[]` |

---

### `POST /recommend`

Get career recommendations based on a user profile.

**Request Body (option A — use saved profile):**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

**Request Body (option B — inline skills):**
```json
{
  "skills": ["Python", "SQL"],
  "interests": ["Data Science"]
}
```

**Response:**
```json
{
  "careers": [
    {
      "role": "Data Scientists",
      "description": "Develop and implement techniques or analytics...",
      "required_skills": "Machine Learning, Python, SQL, Statistics...",
      "similarity_score": 0.8742
    }
  ]
}
```

---

### `POST /path`

Generate a personalised 6-month learning path for a specific career.

**Request Body:**
```json
{
  "user_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "career": "Data Scientists"
}
```

**Response:**
```json
{
  "career": "Data Scientists",
  "learning_path": "## 🧭 6-Month Learning Path: Data Scientists\n\n...",
  "source": "gemini"
}
```

| `source` Value | Meaning |
|---|---|
| `"gemini"` | Generated by Google Gemini AI |
| `"mock"` | Generated by the built-in template engine |

---

## 🔬 Data Pipeline

The data pipeline transforms raw O\*NET government data into a searchable vector index. It consists of two stages:

### Stage 1: Data Preparation (`scripts/prepare_data.py`)

```bash
python scripts/prepare_data.py
```

**What it does:**
1. Reads 4 raw O\*NET CSV files from `data/`
2. Filters skills by importance threshold (≥ 3.5)
3. Prioritises "Hot Technology" software skills
4. Produces 3 processed CSVs:

| Output | Records | Description |
|---|---|---|
| `careers.csv` | 1,017 | Role name + description + required skills |
| `skills.csv` | 8,920 | Deduplicated skill names from all sources |
| `courses.csv` | 13 | Synthetic course catalog for priority skills |

### Stage 2: Embedding & Indexing (`scripts/embedding.py`)

```bash
python scripts/embedding.py
```

**What it does:**
1. Loads the `all-MiniLM-L6-v2` sentence-transformer model locally (~90 MB download)
2. Encodes all 1,017 career profiles and 8,920 skills into 384-dim vectors
3. Stores vectors + metadata in ChromaDB (persistent SQLite-backed storage)
4. Uses batch inserts (256 per batch) for efficiency

> **Note:** The pre-built `chroma_db/` is included in the repository. You only need to run these scripts if you want to rebuild the index from scratch.

---

## 🧠 AI & ML Components

### 1. Semantic Embeddings (Career Matching)

| Property | Detail |
|---|---|
| **Model** | `all-MiniLM-L6-v2` (Sentence-Transformers) |
| **Dimension** | 384 |
| **Offline use** | Local `SentenceTransformer` class (index building) |
| **Online use** | HuggingFace Inference API (runtime queries) |
| **Distance metric** | Euclidean → converted to similarity via `max(0, 1 - d²/2)` |

### 2. LLM Generation (Learning Paths)

| Property | Detail |
|---|---|
| **Model** | `gemini-3.6-flash` (configurable) |
| **SDK** | `google-genai` Python client |
| **Fallback** | Template engine with hand-crafted plans for 5 careers + generic template |
| **Output** | Markdown-formatted 6-month roadmap |

---

## 🛠 Tech Stack

### Backend

| Technology | Purpose |
|---|---|
| **FastAPI** 0.141 | REST API framework |
| **Uvicorn** 0.52 | ASGI server |
| **ChromaDB** 1.5 | Vector database (SQLite-backed) |
| **Pydantic** 2.13 | Request/response validation |
| **NumPy** 2.5 | Embedding vector operations |
| **Requests** 2.34 | HuggingFace API calls |
| **google-genai** | Gemini SDK |
| **python-dotenv** 1.2 | Environment variable management |

### Frontend

| Technology | Purpose |
|---|---|
| **React** 19 | UI component library |
| **Vite** 8 | Dev server, bundling, HMR |
| **Tailwind CSS** 4 | Utility-first styling |
| **React Router** 7 | Client-side routing |
| **Axios** 1.19 | HTTP client |
| **react-markdown** 10 | Markdown → styled HTML |
| **OxLint** 1.75 | JavaScript/React linting |

### Data & ML

| Technology | Purpose |
|---|---|
| **pandas** 3.0 | CSV processing & ETL |
| **sentence-transformers** | Local embedding model |
| **O\*NET Database** | Real-world occupation data (U.S. Dept. of Labor) |

---

## 🖥 Frontend Pages

| Route | Component | Description |
|---|---|---|
| `/` | `Landing.jsx` | Hero section with project tagline and "Find my path →" CTA |
| `/onboard` | `Onboarding.jsx` | Skill input (tag chips) + interest selection (8 toggle buttons) |
| `/recommendations` | `Recommendations.jsx` | Top 5 career cards with match %, skills, and "View Path" button |
| `/path` | `PathView.jsx` | Rendered 6-month learning roadmap with source badge |

### Design System

| Element | Value |
|---|---|
| **Body font** | DM Sans (Google Fonts) |
| **Heading font** | Space Grotesk (Google Fonts) |
| **Primary colour** | `#ef7656` (warm coral) |
| **Accent colour** | `#2a9d8f` (teal) |
| **Background** | `#f6f7f2` with subtle gradients |
| **Dark accent** | `#172033` (near-black navy) |

---

## 🔒 Security Considerations

### ✅ Implemented

- **CORS middleware** — Configurable origins via `CORS_ORIGINS` env var
- **Pydantic validation** — All API inputs validated with type checking and constraints
- **Environment variables** — API keys loaded from `.env`, never hard-coded
- **`.gitignore` for `.env`** — Secrets excluded from version control
- **Request timeouts** — 30-second timeout on HuggingFace API calls
- **Graceful error handling** — Gemini failures fall back silently to template paths

### ⚠️ Areas for Improvement (Production)

- No user authentication or rate limiting
- CORS defaults to `*` (should be restricted)
- In-memory user store (not persistent)
- No HTTPS enforcement at the application level
- No input sanitisation beyond Pydantic type validation

---

## 🧪 Rebuilding the Vector Index

If you modify the source data or want to rebuild from scratch:

```bash
# Step 1 — Transform raw O*NET data into processed CSVs
python scripts/prepare_data.py

# Step 2 — Generate embeddings and populate ChromaDB
python scripts/embedding.py
```

> ⚠️ Step 2 requires the `sentence-transformers` package and will download the model (~90 MB) on first run.

---

## 📋 Available Scripts

### Backend

```bash
# Start the development server with hot reload
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Run the data preparation pipeline
python scripts/prepare_data.py

# Build the ChromaDB vector index
python scripts/embedding.py
```

### Frontend

```bash
cd frontend

npm run dev       # Start Vite dev server (port 5173)
npm run build     # Build production bundle → dist/
npm run preview   # Preview production build locally
npm run lint      # Run OxLint
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational and demonstration purposes. See the repository for license details.

---

<div align="center">

**Built with ❤️ using FastAPI, React, ChromaDB, and Google Gemini**

</div>
]]>
