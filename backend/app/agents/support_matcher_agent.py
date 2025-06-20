from langchain_core.runnables import RunnableLambda
from app.services.weaviate_service import get_weaviate_client

def perform_keyword_retrieval(state_dict: dict) -> dict:
    """
    Performs a direct KEYWORD filter search using multiple 'Like' operators.
    This is the most robust and reliable method.
    """
    client = get_weaviate_client()
    
    career_titles = [c.get('title', '') for c in state_dict.get('career_alternatives', {}).get('career_alternatives', [])]
    strengths_list = [s.get('strength', '') for s in state_dict.get('strengths', {}).get('strengths', [])]
    
    all_phrases = career_titles + strengths_list
    all_words = []
    for phrase in all_phrases:
        all_words.extend(phrase.lower().split())
        
    unique_keywords = list(set(w for w in all_words if len(w) > 3))

    if not unique_keywords:
        return {"support_matches": []}

    print(f"--- Performing Final Keyword Search with keywords: {unique_keywords} ---")

    # Build an "Or" filter with multiple "Like" operators for wildcard matching
    where_operands = []
    for keyword in unique_keywords:
        where_operands.append({
            "path": ["focus"],
            "operator": "Like", # Use "Like" for substring matching
            "valueText": f"*{keyword}*" # e.g., *writer*, *qa*, *automation*
        })
    
    where_filter = { "operator": "Or", "operands": where_operands }

    try:
        response = (
            client.query
            .get("Support", ["name", "type", "focus", "contact"])
            .with_where(where_filter)
            .with_limit(3)
            .do()
        )
        matches = response.get('data', {}).get('Get', {}).get('Support', [])
        print(f"--- Final Keyword Search Found {len(matches)} matches ---")
        return {"support_matches": matches}
        
    except Exception as e:
        print(f"Error during Weaviate 'where' filter query: {e}")
        return {"support_matches": []}


def get_support_matcher_agent():
    """
    Returns the Support Matchmaking Agent using a direct keyword filter.
    """
    return RunnableLambda(perform_keyword_retrieval)