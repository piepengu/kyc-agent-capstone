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
import os
from dotenv import load_dotenv

# Load environment variables before importing agents
# Try multiple paths for .env file
env_paths = [
    os.path.join(os.path.dirname(__file__), '.env'),  # Relative to this file
    os.path.join(os.getcwd(), '.env'),  # Current working directory
    '.env'  # Current directory
]

env_path = None
for path in env_paths:
    if os.path.exists(path):
        env_path = path
        break

# Always try to load from .env file directly first
if env_path:
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
    except Exception as e:
        pass  # Silent fail, will try load_dotenv

# Also try load_dotenv as backup
if env_path:
    load_dotenv(env_path, override=True)
else:
    load_dotenv(override=True)

# Final verification - only raise error if still not found
if not os.getenv('GOOGLE_API_KEY'):
    # Last resort: try to read from current directory
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GOOGLE_API_KEY='):
                    api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                    os.environ['GOOGLE_API_KEY'] = api_key
                    break
    except Exception:
        pass

from agents import SearchAgent, WatchlistAgent, AnalysisAgent
from logger import workflow_logger, performance_tracker


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
        customer_name = state.get("customer_name", "")
        if not customer_name:
            error_msg = "Customer name is required but was not provided"
            workflow_logger.error(error_msg)
            return {
                **state,
                "error": error_msg,
                "search_results": []
            }
        
        workflow_logger.info(f"Executing search_node for: {customer_name}")
        search_results = search_agent.search_adverse_media(customer_name)
        workflow_logger.info(f"Search node completed: {len(search_results)} results found")
        
        return {
            **state,
            "search_results": search_results,
            "error": state.get("error", "")
        }
    except ValueError as e:
        # Validation errors - don't retry
        error_msg = f"Invalid input: {str(e)}"
        workflow_logger.error(f"Search node validation error: {error_msg}")
        return {
            **state,
            "error": error_msg,
            "search_results": []
        }
    except Exception as e:
        error_msg = f"SearchAgent error: {str(e)}"
        workflow_logger.error(f"Search node error: {error_msg}")
        # Return empty results but continue workflow
        return {
            **state,
            "error": error_msg,
            "search_results": []
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
        customer_name = state.get("customer_name", "")
        if not customer_name:
            error_msg = "Customer name is required but was not provided"
            workflow_logger.error(error_msg)
            return {
                **state,
                "error": f"{state.get('error', '')}; {error_msg}".strip('; '),
                "watchlist_results": {"matched": False, "watchlists_checked": [], "matches": []}
            }
        
        workflow_logger.info(f"Executing watchlist_node for: {customer_name}")
        watchlist_results = watchlist_agent.check_watchlists(customer_name)
        workflow_logger.info(f"Watchlist node completed: matched={watchlist_results.get('matched', False)}")
        
        return {
            **state,
            "watchlist_results": watchlist_results,
            "error": state.get("error", "")
        }
    except ValueError as e:
        # Validation errors - don't retry
        error_msg = f"Invalid input: {str(e)}"
        workflow_logger.error(f"Watchlist node validation error: {error_msg}")
        return {
            **state,
            "error": f"{state.get('error', '')}; {error_msg}".strip('; '),
            "watchlist_results": {"matched": False, "watchlists_checked": [], "matches": []}
        }
    except Exception as e:
        error_msg = f"WatchlistAgent error: {str(e)}"
        workflow_logger.error(f"Watchlist node error: {error_msg}")
        # Return empty results but continue workflow
        return {
            **state,
            "error": f"{state.get('error', '')}; {error_msg}".strip('; '),
            "watchlist_results": {"matched": False, "watchlists_checked": [], "matches": []}
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
        customer_name = state.get("customer_name", "")
        search_results = state.get("search_results", [])
        watchlist_results = state.get("watchlist_results", {})
        
        if not customer_name:
            error_msg = "Customer name is required but was not provided"
            workflow_logger.error(error_msg)
            return {
                **state,
                "error": f"{state.get('error', '')}; {error_msg}".strip('; '),
                "final_report": f"Error: {error_msg}"
            }
        
        workflow_logger.info(f"Executing analysis_node for: {customer_name}")
        final_report = analysis_agent.generate_report(
            customer_name,
            search_results,
            watchlist_results
        )
        workflow_logger.info(f"Analysis node completed: report length={len(final_report)} characters")
        
        return {
            **state,
            "final_report": final_report,
            "error": state.get("error", "")
        }
    except Exception as e:
        error_msg = f"AnalysisAgent error: {str(e)}"
        workflow_logger.error(f"Analysis node error: {error_msg}")
        # Generate a basic error report
        fallback_report = f"""## KYC Risk Assessment Report - {state.get('customer_name', 'Unknown')}

**Error:** Unable to generate full risk assessment report.

**Error Details:** {error_msg}

**Available Data:**
- Search Results: {len(search_results)} items
- Watchlists Checked: {len(watchlist_results.get('watchlists_checked', []))}
- Watchlist Matches: {len(watchlist_results.get('matches', []))}

**Recommendation:** Please review the available data manually.
"""
        return {
            **state,
            "error": f"{state.get('error', '')}; {error_msg}".strip('; '),
            "final_report": fallback_report
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

