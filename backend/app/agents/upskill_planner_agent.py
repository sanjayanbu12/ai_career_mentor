from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import config

def get_upskill_planner_agent():
    """Returns the Upskill Planner Agent using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=config.GOOGLE_API_KEY)
    
    prompt = ChatPromptTemplate.from_template("""
        You are a learning and development specialist. Create a personalized upskilling roadmap for the suggested career paths.
        For each career, define at least 5 milestones with specific resources (e.g., courses, project ideas).

        Career Alternatives: {career_alternatives}
        Student's Strengths: {strengths}

        Output a JSON object with a key 'upskilling_plan'.
    """)
    
    parser = JsonOutputParser()
    return prompt | llm | parser