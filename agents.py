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
from tools import format_search_query, check_watchlist


class SearchAgent:
    """
    Agent responsible for searching adverse media about a customer.
    
    Uses Google Search API to find news articles, reports, and other
    information linking the customer to fraud, sanctions, or financial crimes.
    """
    
    def __init__(self):
        """Initialize the SearchAgent with Google Search capabilities."""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        # For Google Custom Search API, we'll use a simple approach
        # Note: This requires a Custom Search Engine ID (CX) for full functionality
        # For now, we'll use a mock/simulated approach that can be enhanced
        print("✅ SearchAgent initialized")
    
    def search_adverse_media(self, customer_name: str) -> List[Dict[str, str]]:
        """
        Search for adverse media related to the customer.
        
        Args:
            customer_name: The name of the customer to investigate
            
        Returns:
            List of dictionaries containing search results with 'title', 'snippet', 'link'
        """
        print(f"🔎 SearchAgent: Searching for adverse media on '{customer_name}'...")
        
        # Generate multiple search queries
        query_types = ["adverse_media", "fraud", "sanctions"]
        all_results = []
        
        for query_type in query_types:
            query = format_search_query(customer_name, query_type)
            print(f"   📝 Query: {query}")
            
            # TODO: Implement actual Google Custom Search API call
            # For now, using simulated results for testing
            # In production, this would use: googleapiclient.discovery.build("customsearch", "v1", developerKey=self.api_key)
            
            # Simulated search results for demonstration
            simulated_results = [
                {
                    "title": f"News article about {customer_name}",
                    "snippet": f"Recent news coverage related to {customer_name} and financial activities.",
                    "link": f"https://example.com/news/{customer_name.replace(' ', '-')}"
                }
            ]
            all_results.extend(simulated_results)
        
        print(f"   ✅ Found {len(all_results)} search results")
        return all_results


class WatchlistAgent:
    """
    Agent responsible for checking customer against watchlists.
    
    Uses a custom tool to check against simulated international
    sanctions databases and watchlists.
    """
    
    def __init__(self):
        """Initialize the WatchlistAgent with custom watchlist tool."""
        print("✅ WatchlistAgent initialized with custom watchlist tool")
    
    def check_watchlists(self, customer_name: str) -> Dict:
        """
        Check customer name against various watchlists.
        
        Args:
            customer_name: The name of the customer to check
            
        Returns:
            Dictionary with watchlist check results containing:
            - matched: bool
            - watchlists_checked: List[str]
            - matches: List[Dict]
        """
        print(f"📋 WatchlistAgent: Checking '{customer_name}' against watchlists...")
        
        # Use the custom check_watchlist tool
        results = check_watchlist(customer_name)
        
        if results.get("matched"):
            print(f"   ⚠️  WARNING: Match found in watchlists!")
        else:
            print(f"   ✅ No matches found in {len(results.get('watchlists_checked', []))} watchlists")
        
        return results


class AnalysisAgent:
    """
    Agent responsible for analyzing findings and generating final report.
    
    Uses Gemini 1.5 Flash model to analyze all collected information and generate
    a structured risk assessment report.
    """
    
    def __init__(self):
        """Initialize the AnalysisAgent with Gemini 1.5 Flash model."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        # Initialize Gemini 1.5 Flash model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ AnalysisAgent initialized with Gemini 1.5 Flash")
    
    def generate_report(
        self, 
        customer_name: str, 
        search_results: List[Dict[str, str]], 
        watchlist_results: Dict
    ) -> str:
        """
        Generate final risk assessment report using Gemini.
        
        Args:
            customer_name: The name of the customer
            search_results: Results from adverse media searches (list of dicts with title, snippet, link)
            watchlist_results: Results from watchlist checks
            
        Returns:
            Structured risk assessment report
        """
        print(f"📊 AnalysisAgent: Generating risk report for '{customer_name}'...")
        
        # Format search results for the prompt
        search_summary = ""
        if search_results:
            search_summary = "\n".join([
                f"- {result.get('title', 'N/A')}: {result.get('snippet', 'N/A')}"
                for result in search_results[:10]  # Limit to top 10 results
            ])
        else:
            search_summary = "No adverse media found in search results."
        
        # Format watchlist results
        watchlist_summary = f"""
Watchlist Check Results:
- Matched: {watchlist_results.get('matched', False)}
- Watchlists Checked: {', '.join(watchlist_results.get('watchlists_checked', []))}
- Number of Matches: {len(watchlist_results.get('matches', []))}
"""
        
        # Create the prompt for Gemini
        prompt = f"""You are a KYC (Know Your Customer) compliance analyst. Analyze the following information and generate a comprehensive risk assessment report.

Customer Name: {customer_name}

ADVERSE MEDIA SEARCH RESULTS:
{search_summary}

WATCHLIST CHECK RESULTS:
{watchlist_summary}

Please generate a structured risk assessment report that includes:
1. Executive Summary (2-3 sentences)
2. Risk Level: LOW, MEDIUM, or HIGH
3. Key Findings from Adverse Media Search
4. Watchlist Check Summary
5. Recommendations for Compliance Officer
6. Overall Assessment

Format the report clearly with sections and bullet points where appropriate."""

        try:
            # Generate the report using Gemini
            response = self.model.generate_content(prompt)
            report = response.text
            
            print(f"   ✅ Report generated successfully ({len(report)} characters)")
            return report
            
        except Exception as e:
            error_msg = f"Error generating report: {str(e)}"
            print(f"   ❌ {error_msg}")
            return f"Error: {error_msg}"

