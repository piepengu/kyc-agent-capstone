"""
Agent definitions for the KYC Bot system.

This module contains the three main agents:
1. SearchAgent - Searches for adverse media using Google Search
2. WatchlistAgent - Checks customer against watchlists
3. AnalysisAgent - Analyzes findings and generates final report
"""

from typing import List, Dict
import os
import google.generativeai as genai


class SearchAgent:
    """
    Agent responsible for searching adverse media about a customer.
    
    Uses Google Search tool to find news articles, reports, and other
    information linking the customer to fraud, sanctions, or financial crimes.
    """
    
    def __init__(self):
        """Initialize the SearchAgent with Google Search capabilities."""
        # TODO: Initialize Google Search tool
        # This will use built-in tools from the course
        pass
    
    def search_adverse_media(self, customer_name: str) -> List[str]:
        """
        Search for adverse media related to the customer.
        
        Args:
            customer_name: The name of the customer to investigate
            
        Returns:
            List of search results (URLs, snippets, etc.)
        """
        # TODO: Implement search logic
        # Generate multiple search queries dynamically
        # Execute searches using Google Search tool
        # Return aggregated results
        
        print(f"🔎 SearchAgent: Searching for adverse media on '{customer_name}'...")
        return []


class WatchlistAgent:
    """
    Agent responsible for checking customer against watchlists.
    
    Uses a custom tool to check against simulated international
    sanctions databases and watchlists.
    """
    
    def __init__(self):
        """Initialize the WatchlistAgent with custom watchlist tool."""
        # TODO: Initialize custom watchlist checking tool
        pass
    
    def check_watchlists(self, customer_name: str) -> Dict:
        """
        Check customer name against various watchlists.
        
        Args:
            customer_name: The name of the customer to check
            
        Returns:
            Dictionary with watchlist check results
        """
        # TODO: Implement watchlist checking logic
        # Use custom check_watchlist tool
        # Return structured results
        
        print(f"📋 WatchlistAgent: Checking '{customer_name}' against watchlists...")
        return {}


class AnalysisAgent:
    """
    Agent responsible for analyzing findings and generating final report.
    
    Uses Gemini model to analyze all collected information and generate
    a structured risk assessment report.
    """
    
    def __init__(self):
        """Initialize the AnalysisAgent with Gemini model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        # TODO: Initialize Gemini model (gemini-2.5-flash or similar)
        self.model = None  # Will be initialized with genai.GenerativeModel()
    
    def generate_report(
        self, 
        customer_name: str, 
        search_results: List[str], 
        watchlist_results: Dict
    ) -> str:
        """
        Generate final risk assessment report.
        
        Args:
            customer_name: The name of the customer
            search_results: Results from adverse media searches
            watchlist_results: Results from watchlist checks
            
        Returns:
            Structured risk assessment report
        """
        # TODO: Implement report generation
        # Use Gemini model to analyze all findings
        # Generate structured risk report
        
        print(f"📊 AnalysisAgent: Generating risk report for '{customer_name}'...")
        return ""

