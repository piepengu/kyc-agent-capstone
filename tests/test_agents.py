"""
Unit tests for agent classes (SearchAgent, WatchlistAgent, AnalysisAgent).
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from agents import SearchAgent, WatchlistAgent, AnalysisAgent
from error_handling import validate_customer_name


class TestSearchAgent:
    """Test SearchAgent functionality."""
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key', 'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'})
    def test_initialization_with_api_key(self):
        """Test SearchAgent initializes with API key."""
        agent = SearchAgent()
        assert agent is not None
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_api_key(self):
        """Test SearchAgent raises error without API key."""
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            SearchAgent()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key', 'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'})
    def test_search_adverse_media_valid_name(self):
        """Test search with valid customer name."""
        agent = SearchAgent()
        # Mock the search service to avoid actual API calls
        agent.search_service = Mock()
        agent.search_service.cse.return_value.list.return_value.execute.return_value = {
            'items': [
                {
                    'title': 'Test Result',
                    'snippet': 'Test snippet',
                    'link': 'https://example.com'
                }
            ]
        }
        
        results = agent.search_adverse_media("John Smith")
        assert isinstance(results, list)
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key', 'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'})
    def test_search_adverse_media_invalid_name(self):
        """Test search with invalid customer name."""
        agent = SearchAgent()
        agent.search_service = Mock()
        
        with pytest.raises(ValueError):
            agent.search_adverse_media("")  # Empty name
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key', 'GOOGLE_SEARCH_ENGINE_ID': 'test_cx'})
    def test_search_fallback_on_error(self):
        """Test search falls back to simulated results on error."""
        agent = SearchAgent()
        agent.search_service = Mock()
        agent.search_service.cse.return_value.list.return_value.execute.side_effect = Exception("API Error")
        
        results = agent.search_adverse_media("John Smith")
        assert isinstance(results, list)
        assert len(results) > 0  # Should have fallback results


class TestWatchlistAgent:
    """Test WatchlistAgent functionality."""
    
    def test_initialization(self):
        """Test WatchlistAgent initializes correctly."""
        agent = WatchlistAgent()
        assert agent is not None
    
    def test_check_watchlists_valid_name(self):
        """Test watchlist check with valid name."""
        agent = WatchlistAgent()
        results = agent.check_watchlists("John Smith")
        assert isinstance(results, dict)
        assert "matched" in results
        assert "watchlists_checked" in results
        assert "matches" in results
    
    def test_check_watchlists_invalid_name(self):
        """Test watchlist check with invalid name."""
        agent = WatchlistAgent()
        with pytest.raises(ValueError):
            agent.check_watchlists("")  # Empty name
    
    def test_check_watchlists_match_found(self):
        """Test watchlist check finds matches."""
        agent = WatchlistAgent()
        results = agent.check_watchlists("Vladimir Petrov")
        assert results["matched"] is True
        assert len(results["matches"]) > 0
    
    def test_check_watchlists_no_match(self):
        """Test watchlist check finds no matches."""
        agent = WatchlistAgent()
        results = agent.check_watchlists("John Smith")
        assert results["matched"] is False
        assert len(results["matches"]) == 0


class TestAnalysisAgent:
    """Test AnalysisAgent functionality."""
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_initialization(self):
        """Test AnalysisAgent initializes correctly."""
        agent = AnalysisAgent()
        assert agent is not None
        assert agent.model is not None
    
    @patch.dict(os.environ, {}, clear=True)
    def test_initialization_without_api_key(self):
        """Test AnalysisAgent raises error without API key."""
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            AnalysisAgent()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_report_valid_input(self):
        """Test report generation with valid input."""
        agent = AnalysisAgent()
        
        # Mock the Gemini model
        mock_response = Mock()
        mock_response.text = "Test report content with Risk Level: LOW"
        agent.model = Mock()
        agent.model.generate_content.return_value = mock_response
        
        search_results = [
            {"title": "Test", "snippet": "Test snippet", "link": "https://example.com"}
        ]
        watchlist_results = {
            "matched": False,
            "watchlists_checked": ["OFAC"],
            "matches": []
        }
        
        report = agent.generate_report("John Smith", search_results, watchlist_results)
        assert isinstance(report, str)
        assert len(report) > 0
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_report_with_match(self):
        """Test report generation with watchlist match."""
        agent = AnalysisAgent()
        
        # Create a longer mock response to pass validation (must be > 100 chars)
        mock_response = Mock()
        mock_response.text = """## KYC Risk Assessment Report

**Customer Name:** Vladimir Petrov

**Risk Level:** HIGH

This is a comprehensive risk assessment report that exceeds the minimum length requirement. The customer has been found on multiple watchlists and presents a high risk profile. Additional details and recommendations are provided below for compliance review."""
        agent.model = Mock()
        agent.model.generate_content.return_value = mock_response
        
        search_results = []
        watchlist_results = {
            "matched": True,
            "watchlists_checked": ["OFAC"],
            "matches": [{"watchlist": "OFAC", "name": "Test", "similarity": 1.0}]
        }
        
        report = agent.generate_report("Vladimir Petrov", search_results, watchlist_results)
        assert isinstance(report, str)
        assert "HIGH" in report or "high" in report.lower()
    
    @patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'})
    def test_generate_report_fallback_on_error(self):
        """Test report generation falls back on error."""
        agent = AnalysisAgent()
        
        # Mock the model to raise an error
        agent.model = Mock()
        agent.model.generate_content.side_effect = Exception("API Error")
        
        search_results = []
        watchlist_results = {
            "matched": False,
            "watchlists_checked": ["OFAC"],
            "matches": []
        }
        
        report = agent.generate_report("John Smith", search_results, watchlist_results)
        assert isinstance(report, str)
        assert "Error" in report or "error" in report.lower() or "UNABLE TO DETERMINE" in report

