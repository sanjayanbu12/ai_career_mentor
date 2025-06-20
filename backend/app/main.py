from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import docx
import io

from app.graph.agent_graph import create_agentic_workflow

app = FastAPI()

# CORS Middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compile the agentic workflow
agentic_workflow = create_agentic_workflow()

async def read_file_content(file: UploadFile) -> str:
    """A helper function to robustly read the content of uploaded files."""
    content = ""
    file_bytes = await file.read()
    file_stream = io.BytesIO(file_bytes)
    
    try:
        if file.filename.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(file_stream)
            for page in pdf_reader.pages:
                content += page.extract_text() or ""
        elif file.filename.endswith(".docx"):
            doc = docx.Document(file_stream)
            for para in doc.paragraphs:
                content += para.text + "\n"
        else:  # Default to plain text for .txt, .csv, etc.
            content = file_bytes.decode('utf-8')
    except Exception as e:
        print(f"Error reading file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {file.filename}")
    finally:
        await file.close()
        
    return content

@app.post("/analyze")
async def analyze_student_data(
    resume: UploadFile = File(...),
    coding_results: UploadFile = File(...),
    interview_feedback: UploadFile = File(...),
    performance_data: UploadFile = File(...)
):
    """
    This endpoint receives student documents, processes them through the AI agentic workflow,
    and returns a comprehensive analysis.
    """
    try:
        # Use the helper function to read content robustly
        resume_text = await read_file_content(resume)
        coding_results_text = await read_file_content(coding_results)
        interview_feedback_text = await read_file_content(interview_feedback)
        performance_data_text = await read_file_content(performance_data)

        initial_state = {
            "resume_text": resume_text,
            "coding_results_text": coding_results_text,
            "interview_feedback_text": interview_feedback_text,
            "performance_data_text": performance_data_text,
        }

        # Invoke the agentic workflow
        final_state = agentic_workflow.invoke(initial_state)

        return {
            "rejection_patterns": final_state.get("rejection_patterns"),
            "strengths": final_state.get("strengths"),
            "career_alternatives": final_state.get("career_alternatives"),
            "upskilling_plan": final_state.get("upskilling_plan"),
            "support_matches": final_state.get("support_matches"),
        }
    except Exception as e:
        print(f"An error occurred in the /analyze endpoint: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred during analysis.")

@app.get("/")
def read_root():
    return {"message": "AI Career Redirection Mentor API"}