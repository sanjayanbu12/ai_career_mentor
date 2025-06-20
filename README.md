# AI Career Redirection Mentor

---

## 🚀 Project Objective

Build an agentic, AI-powered Career Redirection Mentor that helps students who face repeated rejections pivot to realistic and promising career paths. The system analyzes rejection patterns, identifies strengths, suggests alternative careers, plans upskilling, and connects users to relevant support networks.

---

## 🛠️ Tech Stack

- **Frontend:** React.js
- **Backend:** Python, FastAPI
- **AI Agent Framework:** LangChain, LangGraph
- **LLM:** Google Gemini
- **Vector Database (RAG):** Weaviate Cloud Service (WCS)

---

## 🏗️ Architecture Overview

The application is built on a decoupled architecture:

- **Frontend (React.js):** User interface for document upload and dashboard visualization.
- **Backend (Python/FastAPI):** API server that orchestrates the agentic workflow.
- **Agentic Core (LangGraph):** Manages state and sequential execution of five specialized AI agents.
- **Database (Weaviate):** Stores career and support network data, enabling Retrieval-Augmented Generation (RAG) and hybrid search.

---

## 🤖 Agentic Workflow

The core workflow is a pipeline of five AI agents, triggered when a user uploads their documents:

1. **Rejection Pattern Analyzer Agent**
   - **Function:** Analyzes rejection feedback, resume, and coding test results to identify recurring patterns (e.g., weak algorithms, poor communication).
   - **Input:** Rejection feedback, resume, coding test results.
   - **Output:** Structured JSON with labeled rejection patterns and actionable insights.

2. **Strength Finder Agent**
   - **Function:** Identifies strong areas based on resume and performance data (projects, certifications, hackathons).
   - **Input:** Resume, performance data.
   - **Output:** Structured JSON with specific, evidence-backed strengths.

3. **Career Alternative Generator Agent (RAG-enabled)**
   - **Function:** Suggests realistic, market-aligned career paths using strengths and weaknesses, powered by RAG search against a career database.
   - **Input:** Strengths JSON, rejection patterns JSON.
   - **Output:** Structured JSON with at least three alternative career recommendations.

4. **Upskill Planner Agent**
   - **Function:** Designs a personalized, multi-milestone upskilling roadmap for each suggested career, including resources like courses and project ideas.
   - **Input:** Career recommendations JSON, strengths JSON.
   - **Output:** Detailed, structured upskilling plan.

5. **Support Matchmaking Agent**
   - **Function:** Connects the student to relevant support networks (mentors, bootcamps, peer groups) via hybrid search.
   - **Input:** Career recommendations JSON, strengths JSON.
   - **Output:** Structured JSON with actionable support network details.

**All agent outputs are aggregated and displayed on the user's dashboard.**

---

## 🖥️ How to Run

### Prerequisites

- Node.js and npm
- Python 3.9+ and pip
- Weaviate Cloud Service (WCS) instance
- Google Gemini API Key

### Backend Setup

1. Navigate to the `backend` directory.
2. Create a `.env` file with your `GOOGLE_API_KEY`, `WEAVIATE_URL`, and `WEAVIATE_API_KEY`.
3. Create and activate a Python virtual environment.
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Initialize the database schema and populate it with vectorized data:
   ```sh
   python3 setup_database.py
   ```
6. Start the backend server:
   ```sh
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the `frontend` directory.
2. Create a `.env` file with:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```
3. Install dependencies:
   ```sh
   npm install
   ```
4. Start the frontend:
   ```sh
   npm start
   ```

---

## 🗺️ Workflow Diagram

graph TD
    subgraph "Phase 1: Initial Setup"
        A[Create Weaviate Cloud Service Instance] --> B[Get API Keys: Weaviate & Google Gemini];
        B --> C{Setup Local Environment};
        C --> D[1. Create `backend/.env` file with keys];
        D --> E[2. Run `pip install -r requirements.txt`];
        E --> F[3. Run `python3 setup_database.py` to populate DB];
        C --> G[4. Create `frontend/.env` file];
        G --> H[5. Run `npm install`];
    end

    subgraph "Phase 2: Running the Application"
        I[6. Start Backend Server: `uvicorn app.main:app`] --> J{API is Live};
        K[7. Start Frontend Server: `npm start`] --> L{UI is Live};
    end
    
    subgraph "Phase 3: User Interaction & AI Workflow"
        M[8. User opens `localhost:3000` and uploads documents] --> N{9. Frontend sends files to Backend};
        N --> O(10. Agentic Workflow is Triggered);
        O --> P[Agent 1: Analyzes Rejections];
        P --> Q[Agent 2: Finds Strengths];
        Q --> R[Agent 3: Generates Career Paths (RAG)];
        R --> S[Agent 4: Plans Upskilling];
        S --> T[Agent 5: Matches Support Network];
        T --> U((11. Aggregated JSON Result is created));
    end

    subgraph "Phase 4: Final Output"
        V{12. Backend returns result to Frontend} --> W[13. React UI displays the full analysis on the dashboard];
    end

    %% Connecting the Phases
    H --> K;
    F --> I;
    J --> N;
    L --> M;
    U --> V;

---

## 📄 More Information

For detailed documentation and design notes, see:  
[Project Design Doc (Google Docs)](https://docs.google.com/document/d/1Xz7tzkMCA2C5qda8ivp40LkcldJvhwmiQ_MvitCVYMU/edit?usp=sharing)

## Demo Video

https://drive.google.com/drive/folders/11CN3RBl9I39qe6XVrfVmpIT_emi6Ezoe?usp=sharing

---