from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import config

def get_rejection_analyzer_agent():
    """Returns the Rejection Pattern Analyzer Agent using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=config.GOOGLE_API_KEY)
    
    prompt = ChatPromptTemplate.from_template("""
        You are an expert in analyzing job rejection feedback. Analyze the provided resume, coding test results, and interview feedback.
        Identify key patterns of rejection and structure them into a JSON object.
        Focus on actionable insights and filter out generic comments.
        
        Inputs:
        Resume: {resume_text}
        Coding Test Results: {coding_results_text}
        Interview Feedback: {interview_feedback_text}
        
        Output a JSON object with a key 'rejection_patterns' containing a list of identified patterns.
    """)
    
    parser = JsonOutputParser()
    return prompt | llm | parser