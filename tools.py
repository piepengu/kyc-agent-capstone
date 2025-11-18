"""
Custom tools for the KYC Bot system.

This module contains custom tools that agents can use, including
the watchlist checking tool with fuzzy matching and alias support.
"""

from typing import Dict, List, Tuple
import json
from difflib import SequenceMatcher


# Realistic sample watchlist data (fictional but realistic)
# In production, this would connect to actual sanctions databases
WATCHLIST_DATA = {
    "OFAC": [
        {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov", "Vladimir P. Petrov"],
            "reason": "Sanctions evasion, money laundering",
            "date_added": "2022-03-15",
            "country": "Russia"
        },
        {
            "name": "Ahmed Al-Mansouri",
            "aliases": ["Ahmed Mansouri", "A. Al-Mansouri", "Ahmed Mansur"],
            "reason": "Terrorism financing",
            "date_added": "2021-11-20",
            "country": "Syria"
        },
        {
            "name": "Maria Rodriguez",
            "aliases": ["Maria R. Rodriguez", "M. Rodriguez"],
            "reason": "Drug trafficking, money laundering",
            "date_added": "2023-06-10",
            "country": "Colombia"
        },
        {
            "name": "Chen Wei",
            "aliases": ["Wei Chen", "C. Wei"],
            "reason": "Sanctions violations, export control",
            "date_added": "2022-09-05",
            "country": "China"
        }
    ],
    "UN_Sanctions": [
        {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "UN Security Council sanctions",
            "date_added": "2022-03-20",
            "country": "Russia"
        },
        {
            "name": "Hassan Al-Zahrani",
            "aliases": ["Hassan Zahrani", "H. Al-Zahrani"],
            "reason": "Terrorism-related activities",
            "date_added": "2020-05-12",
            "country": "Yemen"
        },
        {
            "name": "Kim Jong-il",
            "aliases": ["Kim Jong Il", "K. Jong-il"],
            "reason": "Nuclear proliferation",
            "date_added": "2006-10-14",
            "country": "North Korea"
        }
    ],
    "EU_Sanctions": [
        {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "EU sanctions - Ukraine conflict",
            "date_added": "2022-02-28",
            "country": "Russia"
        },
        {
            "name": "Sergei Volkov",
            "aliases": ["Sergey Volkov", "S. Volkov"],
            "reason": "EU sanctions - human rights violations",
            "date_added": "2023-01-15",
            "country": "Russia"
        },
        {
            "name": "Fatima Al-Hashimi",
            "aliases": ["Fatima Hashimi", "F. Al-Hashimi"],
            "reason": "EU sanctions - terrorism financing",
            "date_added": "2021-08-30",
            "country": "Iraq"
        }
    ],
    "UK_Sanctions": [
        {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "UK sanctions - Ukraine conflict",
            "date_added": "2022-03-01",
            "country": "Russia"
        },
        {
            "name": "James O'Brien",
            "aliases": ["Jim O'Brien", "J. O'Brien", "James O Brien"],
            "reason": "UK sanctions - corruption",
            "date_added": "2022-11-22",
            "country": "UK"
        },
        {
            "name": "Mohammed Al-Rashid",
            "aliases": ["Mohammed Rashid", "M. Al-Rashid", "Mohammad Al-Rashid"],
            "reason": "UK sanctions - terrorism",
            "date_added": "2020-12-10",
            "country": "Saudi Arabia"
        }
    ]
}


def normalize_name(name: str) -> str:
    """
    Normalize a name for comparison.
    
    Args:
        name: Name to normalize
        
    Returns:
        Normalized name (lowercase, stripped, extra spaces removed)
    """
    if not name:
        return ""
    # Convert to lowercase, strip, and remove extra spaces
    normalized = " ".join(name.lower().strip().split())
    # Remove common punctuation
    normalized = normalized.replace(".", "").replace(",", "").replace("-", " ")
    # Remove extra spaces again
    normalized = " ".join(normalized.split())
    return normalized


def calculate_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity between two names using SequenceMatcher.
    
    Args:
        name1: First name
        name2: Second name
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    name1_norm = normalize_name(name1)
    name2_norm = normalize_name(name2)
    
    # Exact match after normalization
    if name1_norm == name2_norm:
        return 1.0
    
    # Use SequenceMatcher for fuzzy matching
    similarity = SequenceMatcher(None, name1_norm, name2_norm).ratio()
    
    # Check if one name contains the other (for partial matches)
    if name1_norm in name2_norm or name2_norm in name1_norm:
        # Boost similarity for substring matches
        similarity = max(similarity, 0.85)
    
    return similarity


def check_name_match(customer_name: str, watchlist_entry: Dict, threshold: float = 0.85) -> Tuple[bool, float]:
    """
    Check if customer name matches a watchlist entry (including aliases).
    
    Args:
        customer_name: Name to check
        watchlist_entry: Watchlist entry with name and aliases
        threshold: Similarity threshold for match (default 0.85)
        
    Returns:
        Tuple of (is_match, similarity_score)
    """
    # Check main name
    main_similarity = calculate_similarity(customer_name, watchlist_entry["name"])
    if main_similarity >= threshold:
        return True, main_similarity
    
    # Check aliases
    max_similarity = main_similarity
    for alias in watchlist_entry.get("aliases", []):
        alias_similarity = calculate_similarity(customer_name, alias)
        if alias_similarity >= threshold:
            return True, alias_similarity
        max_similarity = max(max_similarity, alias_similarity)
    
    return False, max_similarity


def check_watchlist(customer_name: str, similarity_threshold: float = 0.85) -> Dict:
    """
    Custom tool to check a customer name against watchlists with fuzzy matching.
    
    This is a simulated watchlist database with realistic sample data.
    In a real implementation, this would connect to actual sanctions databases like:
    - OFAC (Office of Foreign Assets Control)
    - UN Sanctions List
    - EU Sanctions List
    - UK Sanctions List
    
    Features:
    - Fuzzy matching to handle name variations
    - Alias support (checks known aliases)
    - Normalized name comparison
    - Similarity scoring
    
    Args:
        customer_name: The name to check against watchlists
        similarity_threshold: Minimum similarity score for a match (0.0-1.0, default 0.85)
        
    Returns:
        Dictionary containing:
        - matched: bool - Whether name matched any watchlist
        - watchlists_checked: List[str] - List of watchlists checked
        - matches: List[Dict] - Details of any matches found, each with:
            - watchlist: str - Name of watchlist
            - name: str - Matched name from watchlist
            - similarity: float - Similarity score (0.0-1.0)
            - reason: str - Reason for listing
            - date_added: str - Date added to watchlist
            - country: str - Country of origin
    """
    if not customer_name or not customer_name.strip():
        return {
            "matched": False,
            "watchlists_checked": list(WATCHLIST_DATA.keys()),
            "matches": []
        }
    
    matches = []
    watchlists_checked = list(WATCHLIST_DATA.keys())
    
    # Check each watchlist
    for watchlist_name, entries in WATCHLIST_DATA.items():
        for entry in entries:
            is_match, similarity = check_name_match(customer_name, entry, similarity_threshold)
            
            if is_match:
                match_info = {
                    "watchlist": watchlist_name,
                    "name": entry["name"],
                    "similarity": round(similarity, 3),
                    "reason": entry.get("reason", "Not specified"),
                    "date_added": entry.get("date_added", "Unknown"),
                    "country": entry.get("country", "Unknown")
                }
                matches.append(match_info)
    
    result = {
        "matched": len(matches) > 0,
        "watchlists_checked": watchlists_checked,
        "matches": matches
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

