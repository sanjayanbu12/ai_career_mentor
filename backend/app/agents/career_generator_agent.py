from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from app.services.weaviate_service import get_weaviate_client
from langchain_community.vectorstores import Weaviate
import config

def format_retriever_input(state_dict: dict) -> str:
    """Formats the state dictionary into a simple string for vectorization."""
    strengths_list = [s.get('strength', '') for s in state_dict.get('strengths', {}).get('strengths', [])]
    patterns_list = [p.get('pattern', '') for p in state_dict.get('rejection_patterns', {}).get('rejection_patterns', [])]
    strengths_text = "Strengths: " + ", ".join(strengths_list)
    patterns_text = "Weaknesses: " + ", ".join(patterns_list)
    return f"{strengths_text}. {patterns_text}"

def get_career_generator_agent():
    """Returns the RAG-enabled agent that now creates its own vectors."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, google_api_key=config.GOOGLE_API_KEY)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=config.GOOGLE_API_KEY)
    client = get_weaviate_client()
    vectorstore = Weaviate(client, "Career", "title")

    def retrieve_careers_with_vector(text: str):
        """Creates a vector and performs a similarity search."""
        vector = embeddings.embed_query(text)
        # Use similarity_search_by_vector instead of a text-based retriever
        return vectorstore.similarity_search_by_vector(vector, k=4)

    template = """
        You are a career advisor... (Your original prompt here)
        Strengths: {strengths}
        Rejection Patterns: {rejection_patterns}
        Relevant Career Info: {context}
        Output a JSON object with a key 'career_alternatives'...
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {
            "context": RunnableLambda(format_retriever_input) | RunnableLambda(retrieve_careers_with_vector),
            "strengths": lambda x: x["strengths"],
            "rejection_patterns": lambda x: x["rejection_patterns"]
        }
        | prompt
        | llm
        | JsonOutputParser()
    )
    return rag_chain