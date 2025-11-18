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
from logger import (
    search_logger, watchlist_logger, analysis_logger, api_logger,
    track_execution, track_api_call, log_search_query, log_search_results,
    log_watchlist_check, log_report_generation
)


class SearchAgent:
    """
    Agent responsible for searching adverse media about a customer.
    
    Uses Google Search API to find news articles, reports, and other
    information linking the customer to fraud, sanctions, or financial crimes.
    """
    
    def __init__(self):
        """Initialize the SearchAgent with Google Search capabilities."""
        # Try to get API key from environment
        self.api_key = os.getenv("GOOGLE_API_KEY")
        
        # If not found, try to load from .env file directly
        if not self.api_key:
            try:
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_path):
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('GOOGLE_API_KEY='):
                                self.api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                os.environ['GOOGLE_API_KEY'] = self.api_key
                                break
            except Exception:
                pass
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in .env file or as environment variable.")
        
        # Initialize Google Custom Search API
        self.search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        # If not found, try to load from .env file directly
        if not self.search_engine_id:
            try:
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_path):
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('GOOGLE_SEARCH_ENGINE_ID='):
                                self.search_engine_id = line.split('=', 1)[1].strip().strip('"').strip("'")
                                os.environ['GOOGLE_SEARCH_ENGINE_ID'] = self.search_engine_id
                                break
            except Exception:
                pass
        
        # Try to import Google API client
        try:
            from googleapiclient.discovery import build
            self.search_service = build("customsearch", "v1", developerKey=self.api_key)
            self.use_real_search = True
            if not self.search_engine_id:
                print("[!] Warning: GOOGLE_SEARCH_ENGINE_ID not set, using simulated search")
                self.use_real_search = False
            else:
                print(f"[+] SearchAgent initialized with Google Custom Search (CX: {self.search_engine_id[:10]}...)")
        except ImportError:
            print("[!] Warning: google-api-python-client not properly installed, using simulated search")
            self.use_real_search = False
            self.search_service = None
    
    def search_adverse_media(self, customer_name: str) -> List[Dict[str, str]]:
        """
        Search for adverse media related to the customer.
        
        Args:
            customer_name: The name of the customer to investigate
            
        Returns:
            List of dictionaries containing search results with 'title', 'snippet', 'link'
        """
        with track_execution("SearchAgent", search_logger):
            print(f"[*] SearchAgent: Searching for adverse media on '{customer_name}'...")
            search_logger.info(f"Starting adverse media search for: {customer_name}")
            
            # Generate multiple search queries
            query_types = ["adverse_media", "fraud", "sanctions"]
            all_results = []
            
            for query_type in query_types:
                query = format_search_query(customer_name, query_type)
                log_search_query(search_logger, customer_name, query)
                print(f"   [*] Query: {query}")
                
                # Try to use real Google Custom Search API
                if self.use_real_search and self.search_service and self.search_engine_id:
                    try:
                        # Execute Google Custom Search with API tracking
                        with track_api_call("Google Custom Search", f"query: {query}", api_logger):
                            result = self.search_service.cse().list(
                                q=query,
                                cx=self.search_engine_id,
                                num=3  # Get top 3 results per query
                            ).execute()
                        
                        # Extract results
                        if 'items' in result:
                            result_count = len(result['items'])
                            for item in result['items']:
                                all_results.append({
                                    "title": item.get('title', ''),
                                    "snippet": item.get('snippet', ''),
                                    "link": item.get('link', '')
                                })
                            log_search_results(search_logger, query, result_count, is_real=True)
                            print(f"   [+] Found {result_count} real search results")
                        else:
                            search_logger.warning(f"No results found for query: {query}")
                            print(f"   [!] No results found for query")
                    except Exception as e:
                        search_logger.error(f"Search API error for query '{query}': {str(e)}")
                        print(f"   [!] Search API error: {str(e)}, using simulated results")
                        # Fallback to simulated results
                        simulated_results = [
                            {
                                "title": f"News article about {customer_name}",
                                "snippet": f"Recent news coverage related to {customer_name} and financial activities.",
                                "link": f"https://example.com/news/{customer_name.replace(' ', '-')}"
                            }
                        ]
                        all_results.extend(simulated_results)
                        log_search_results(search_logger, query, len(simulated_results), is_real=False)
                else:
                    # Simulated search results for demonstration
                    simulated_results = [
                        {
                            "title": f"News article about {customer_name}",
                            "snippet": f"Recent news coverage related to {customer_name} and financial activities.",
                            "link": f"https://example.com/news/{customer_name.replace(' ', '-')}"
                        }
                    ]
                    all_results.extend(simulated_results)
                    log_search_results(search_logger, query, len(simulated_results), is_real=False)
            
            search_logger.info(f"Search completed: {len(all_results)} total results found")
            print(f"   [+] Found {len(all_results)} search results")
            return all_results


class WatchlistAgent:
    """
    Agent responsible for checking customer against watchlists.
    
    Uses a custom tool to check against simulated international
    sanctions databases and watchlists.
    """
    
    def __init__(self):
        """Initialize the WatchlistAgent with custom watchlist tool."""
        print("[+] WatchlistAgent initialized with custom watchlist tool")
    
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
        with track_execution("WatchlistAgent", watchlist_logger):
            print(f"[*] WatchlistAgent: Checking '{customer_name}' against watchlists...")
            watchlist_logger.info(f"Starting watchlist check for: {customer_name}")
            
            # Use the custom check_watchlist tool
            results = check_watchlist(customer_name)
            
            watchlists_checked = results.get('watchlists_checked', [])
            matches = results.get('matches', [])
            
            log_watchlist_check(watchlist_logger, customer_name, watchlists_checked, matches)
            
            if results.get("matched"):
                watchlist_logger.warning(f"Watchlist match found for {customer_name}: {matches}")
                print(f"   [!] WARNING: Match found in watchlists!")
            else:
                watchlist_logger.info(f"No watchlist matches found for {customer_name}")
                print(f"   [+] No matches found in {len(watchlists_checked)} watchlists")
            
            return results


class AnalysisAgent:
    """
    Agent responsible for analyzing findings and generating final report.
    
    Uses Gemini 1.5 Flash model to analyze all collected information and generate
    a structured risk assessment report.
    """
    
    def __init__(self):
        """Initialize the AnalysisAgent with Gemini 1.5 Flash model."""
        # Try to get API key from environment
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # If not found, try to load from .env file directly
        if not api_key:
            try:
                env_path = os.path.join(os.path.dirname(__file__), '.env')
                if os.path.exists(env_path):
                    with open(env_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith('GOOGLE_API_KEY='):
                                api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                                os.environ['GOOGLE_API_KEY'] = api_key
                                break
            except Exception:
                pass
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in .env file or as environment variable.")
        
        genai.configure(api_key=api_key)
        # Initialize Gemini 2.0 Flash model (using available model)
        self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
        print("[+] AnalysisAgent initialized with Gemini 2.0 Flash")
    
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
        with track_execution("AnalysisAgent", analysis_logger):
            print(f"[*] AnalysisAgent: Generating risk report for '{customer_name}'...")
            analysis_logger.info(f"Starting report generation for: {customer_name}")
            analysis_logger.info(f"Input data: {len(search_results)} search results, "
                               f"{len(watchlist_results.get('watchlists_checked', []))} watchlists checked")
            
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
                # Generate the report using Gemini with API tracking
                with track_api_call("Gemini API", "generate_content", api_logger):
                    response = self.model.generate_content(prompt)
                    report = response.text
                
                # Extract risk level from report (if present)
                risk_level = None
                if "Risk Level:" in report or "risk level:" in report.lower():
                    # Try to extract risk level
                    import re
                    risk_match = re.search(r'Risk Level[:\s]+(LOW|MEDIUM|HIGH)', report, re.IGNORECASE)
                    if risk_match:
                        risk_level = risk_match.group(1).upper()
                
                log_report_generation(analysis_logger, customer_name, len(report), risk_level)
                print(f"   [+] Report generated successfully ({len(report)} characters)")
                return report
                
            except Exception as e:
                error_msg = f"Error generating report: {str(e)}"
                analysis_logger.error(f"Report generation failed for {customer_name}: {error_msg}")
                print(f"   [ERROR] {error_msg}")
                return f"Error: {error_msg}"

