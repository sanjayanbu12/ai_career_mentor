from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.agents.rejection_analyzer_agent import get_rejection_analyzer_agent
from app.agents.strength_finder_agent import get_strength_finder_agent
from app.agents.career_generator_agent import get_career_generator_agent
from app.agents.upskill_planner_agent import get_upskill_planner_agent
from app.agents.support_matcher_agent import get_support_matcher_agent

class AgentState(TypedDict):
    resume_text: str
    coding_results_text: str
    interview_feedback_text: str
    performance_data_text: str
    rejection_patterns: dict
    strengths: dict
    career_alternatives: dict
    upskilling_plan: dict
    support_matches: dict

def create_agentic_workflow():
    # Agent Initialization
    rejection_analyzer = get_rejection_analyzer_agent()
    strength_finder = get_strength_finder_agent()
    career_generator = get_career_generator_agent()
    upskill_planner = get_upskill_planner_agent()
    support_matcher = get_support_matcher_agent()

    # Node Functions
    def analyze_rejections(state):
        result = rejection_analyzer.invoke({
            "resume_text": state["resume_text"],
            "coding_results_text": state["coding_results_text"],
            "interview_feedback_text": state["interview_feedback_text"]
        })
        return {"rejection_patterns": result}

    def find_strengths(state):
        result = strength_finder.invoke({
            "resume_text": state["resume_text"],
            "performance_data_text": state["performance_data_text"]
        })
        return {"strengths": result}
    
    def generate_careers(state):
        result = career_generator.invoke({
            "strengths": state["strengths"],
            "rejection_patterns": state["rejection_patterns"]
        })
        return {"career_alternatives": result}

    def plan_upskilling(state):
        result = upskill_planner.invoke({
            "career_alternatives": state["career_alternatives"],
            "strengths": state["strengths"]
        })
        return {"upskilling_plan": result}

    def match_support(state):
        # ---- THIS IS THE FIX ----
        # The agent now correctly receives both the strengths and career alternatives
        # to perform the most effective search possible.
        result = support_matcher.invoke({
            "career_alternatives": state["career_alternatives"],
            "strengths": state["strengths"] 
        })
        # -------------------------
        return {"support_matches": result}

    # Graph Definition
    workflow = StateGraph(AgentState)
    workflow.add_node("analyze_rejections", analyze_rejections)
    workflow.add_node("find_strengths", find_strengths)
    workflow.add_node("generate_careers", generate_careers)
    workflow.add_node("plan_upskilling", plan_upskilling)
    workflow.add_node("match_support", match_support)

    # Edge Definition
    workflow.set_entry_point("analyze_rejections")
    workflow.add_edge("analyze_rejections", "find_strengths")
    workflow.add_edge("find_strengths", "generate_careers")
    workflow.add_edge("generate_careers", "plan_upskilling")
    workflow.add_edge("plan_upskilling", "match_support")
    workflow.add_edge("match_support", END)
    
    return workflow.compile()