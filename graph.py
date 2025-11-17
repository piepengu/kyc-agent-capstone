"""
LangGraph workflow definition for the KYC Bot multi-agent system.

This module defines the sequential workflow using LangGraph StateGraph
to coordinate the three agents: SearchAgent, WatchlistAgent, and AnalysisAgent.
"""

from typing import List, Dict
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from agents import SearchAgent, WatchlistAgent, AnalysisAgent


# AgentState TypedDict for managing state between agents
class AgentState(TypedDict):
    """State management for the multi-agent workflow."""
    customer_name: str
    search_results: List[Dict[str, str]]
    watchlist_results: Dict
    final_report: str
    error: str


# Initialize agents (will be initialized once)
_search_agent = None
_watchlist_agent = None
_analysis_agent = None


def get_agents():
    """Lazy initialization of agents."""
    global _search_agent, _watchlist_agent, _analysis_agent
    
    if _search_agent is None:
        _search_agent = SearchAgent()
    if _watchlist_agent is None:
        _watchlist_agent = WatchlistAgent()
    if _analysis_agent is None:
        _analysis_agent = AnalysisAgent()
    
    return _search_agent, _watchlist_agent, _analysis_agent


def search_node(state: AgentState) -> AgentState:
    """
    LangGraph node for SearchAgent.
    
    Searches for adverse media about the customer.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with search_results
    """
    search_agent, _, _ = get_agents()
    
    try:
        customer_name = state["customer_name"]
        search_results = search_agent.search_adverse_media(customer_name)
        
        return {
            **state,
            "search_results": search_results,
            "error": ""
        }
    except Exception as e:
        return {
            **state,
            "error": f"SearchAgent error: {str(e)}"
        }


def watchlist_node(state: AgentState) -> AgentState:
    """
    LangGraph node for WatchlistAgent.
    
    Checks customer against watchlists.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with watchlist_results
    """
    _, watchlist_agent, _ = get_agents()
    
    try:
        customer_name = state["customer_name"]
        watchlist_results = watchlist_agent.check_watchlists(customer_name)
        
        return {
            **state,
            "watchlist_results": watchlist_results,
            "error": state.get("error", "")
        }
    except Exception as e:
        return {
            **state,
            "error": f"{state.get('error', '')}; WatchlistAgent error: {str(e)}"
        }


def analysis_node(state: AgentState) -> AgentState:
    """
    LangGraph node for AnalysisAgent.
    
    Generates final risk assessment report.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with final_report
    """
    _, _, analysis_agent = get_agents()
    
    try:
        customer_name = state["customer_name"]
        search_results = state.get("search_results", [])
        watchlist_results = state.get("watchlist_results", {})
        
        final_report = analysis_agent.generate_report(
            customer_name,
            search_results,
            watchlist_results
        )
        
        return {
            **state,
            "final_report": final_report,
            "error": state.get("error", "")
        }
    except Exception as e:
        return {
            **state,
            "error": f"{state.get('error', '')}; AnalysisAgent error: {str(e)}",
            "final_report": f"Error generating report: {str(e)}"
        }


def create_workflow() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Returns:
        Compiled StateGraph ready for execution
    """
    # Create the StateGraph
    workflow = StateGraph(AgentState)
    
    # Add nodes for each agent
    workflow.add_node("search_agent", search_node)
    workflow.add_node("watchlist_agent", watchlist_node)
    workflow.add_node("analysis_agent", analysis_node)
    
    # Define the sequential flow
    workflow.set_entry_point("search_agent")
    workflow.add_edge("search_agent", "watchlist_agent")
    workflow.add_edge("watchlist_agent", "analysis_agent")
    workflow.add_edge("analysis_agent", END)
    
    # Compile the workflow
    return workflow.compile()

