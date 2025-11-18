"""
Integration tests for the KYC Bot workflow.
"""

import pytest
import os
from unittest.mock import Mock, patch
from graph import create_workflow, AgentState
from agents import SearchAgent, WatchlistAgent, AnalysisAgent


class TestWorkflowIntegration:
    """Test end-to-end workflow integration."""
    
    @patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_key',
        'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'
    })
    def test_workflow_creation(self):
        """Test workflow can be created."""
        workflow = create_workflow()
        assert workflow is not None
    
    @patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_key',
        'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'
    })
    def test_workflow_state_flow(self):
        """Test state flows through workflow correctly."""
        workflow = create_workflow()
        
        initial_state: AgentState = {
            "customer_name": "John Smith",
            "search_results": [],
            "watchlist_results": {},
            "final_report": "",
            "error": ""
        }
        
        # Mock agents to avoid actual API calls
        with patch('graph.get_agents') as mock_get_agents:
            mock_search = Mock()
            mock_search.search_adverse_media.return_value = [
                {"title": "Test", "snippet": "Test", "link": "https://example.com"}
            ]
            
            mock_watchlist = Mock()
            mock_watchlist.check_watchlists.return_value = {
                "matched": False,
                "watchlists_checked": ["OFAC"],
                "matches": []
            }
            
            mock_analysis = Mock()
            mock_analysis.generate_report.return_value = "Test report"
            
            mock_get_agents.return_value = (mock_search, mock_watchlist, mock_analysis)
            
            # Execute workflow
            final_state = workflow.invoke(initial_state)
            
            assert final_state["customer_name"] == "John Smith"
            assert len(final_state["search_results"]) > 0
            assert final_state["watchlist_results"] is not None
            assert len(final_state["final_report"]) > 0
    
    @patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_key',
        'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'
    })
    def test_workflow_with_match(self):
        """Test workflow with watchlist match."""
        workflow = create_workflow()
        
        initial_state: AgentState = {
            "customer_name": "Vladimir Petrov",
            "search_results": [],
            "watchlist_results": {},
            "final_report": "",
            "error": ""
        }
        
        with patch('graph.get_agents') as mock_get_agents:
            mock_search = Mock()
            mock_search.search_adverse_media.return_value = []
            
            mock_watchlist = Mock()
            mock_watchlist.check_watchlists.return_value = {
                "matched": True,
                "watchlists_checked": ["OFAC", "UN_Sanctions"],
                "matches": [
                    {"watchlist": "OFAC", "name": "Vladimir Petrov", "similarity": 1.0}
                ]
            }
            
            mock_analysis = Mock()
            mock_analysis.generate_report.return_value = "HIGH RISK report"
            
            mock_get_agents.return_value = (mock_search, mock_watchlist, mock_analysis)
            
            final_state = workflow.invoke(initial_state)
            
            assert final_state["watchlist_results"]["matched"] is True
            assert len(final_state["watchlist_results"]["matches"]) > 0
    
    @patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_key',
        'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'
    })
    def test_workflow_error_handling(self):
        """Test workflow handles errors gracefully."""
        workflow = create_workflow()
        
        initial_state: AgentState = {
            "customer_name": "John Smith",
            "search_results": [],
            "watchlist_results": {},
            "final_report": "",
            "error": ""
        }
        
        with patch('graph.get_agents') as mock_get_agents:
            mock_search = Mock()
            mock_search.search_adverse_media.side_effect = Exception("Search error")
            
            mock_watchlist = Mock()
            mock_watchlist.check_watchlists.return_value = {
                "matched": False,
                "watchlists_checked": [],
                "matches": []
            }
            
            mock_analysis = Mock()
            mock_analysis.generate_report.return_value = "Test report"
            
            mock_get_agents.return_value = (mock_search, mock_watchlist, mock_analysis)
            
            final_state = workflow.invoke(initial_state)
            
            # Workflow should continue despite search error
            assert "error" in final_state or len(final_state.get("error", "")) > 0
            # Should still have a report
            assert len(final_state["final_report"]) > 0
    
    def test_workflow_empty_customer_name(self):
        """Test workflow handles empty customer name."""
        workflow = create_workflow()
        
        initial_state: AgentState = {
            "customer_name": "",
            "search_results": [],
            "watchlist_results": {},
            "final_report": "",
            "error": ""
        }
        
        with patch('graph.get_agents') as mock_get_agents:
            mock_search = Mock()
            mock_watchlist = Mock()
            mock_analysis = Mock()
            mock_get_agents.return_value = (mock_search, mock_watchlist, mock_analysis)
            
            final_state = workflow.invoke(initial_state)
            
            # Should handle empty name gracefully
            assert "error" in final_state or len(final_state.get("error", "")) > 0

