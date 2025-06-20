from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import config

def get_strength_finder_agent():
    """Returns the Strength Finder Agent using Gemini."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=config.GOOGLE_API_KEY)
    
    prompt = ChatPromptTemplate.from_template("""
        You are an expert career coach. Based on the student's resume and performance data, identify their key strengths.
        Extract at least 5 relevant strengths and present them in a structured JSON format.

        Inputs:
        Resume: {resume_text}
        Performance Data: {performance_data_text}

        Output a JSON object with a key 'strengths' containing a list of strengths.
    """)
    
    parser = JsonOutputParser()
    return prompt | llm | parser
