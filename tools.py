"""
Custom tools for the KYC Bot system.

This module contains custom tools that agents can use, including
the watchlist checking tool.
"""

from typing import Dict, List
import json


def check_watchlist(customer_name: str) -> Dict:
    """
    Custom tool to check a customer name against watchlists.
    
    This is a simulated watchlist database. In a real implementation,
    this would connect to actual sanctions databases like:
    - OFAC (Office of Foreign Assets Control)
    - UN Sanctions List
    - EU Sanctions List
    - Other international watchlists
    
    Args:
        customer_name: The name to check against watchlists
        
    Returns:
        Dictionary containing:
        - matched: bool - Whether name matched any watchlist
        - watchlists_checked: List[str] - List of watchlists checked
        - matches: List[Dict] - Details of any matches found
    """
    # TODO: Implement actual watchlist checking logic
    # For now, this is a placeholder that simulates the check
    
    # Simulated watchlist data
    watchlists = {
        "OFAC": [],
        "UN_Sanctions": [],
        "EU_Sanctions": [],
        "UK_Sanctions": []
    }
    
    # Simulated check logic
    # In real implementation, this would query actual databases
    
    result = {
        "matched": False,
        "watchlists_checked": list(watchlists.keys()),
        "matches": []
    }
    
    return result


def format_search_query(customer_name: str, query_type: str = "adverse_media") -> str:
    """
    Helper function to format search queries for adverse media searches.
    
    Args:
        customer_name: The customer name to search for
        query_type: Type of query (adverse_media, fraud, sanctions, etc.)
        
    Returns:
        Formatted search query string
    """
    query_templates = {
        "adverse_media": f'"{customer_name}" fraud OR sanctions OR financial crime',
        "fraud": f'"{customer_name}" fraud OR scam OR embezzlement',
        "sanctions": f'"{customer_name}" sanctions OR OFAC OR blacklist',
        "general": f'"{customer_name}" news OR investigation OR charges'
    }
    
    return query_templates.get(query_type, query_templates["adverse_media"])

