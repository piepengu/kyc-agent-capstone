"""
Pytest configuration and fixtures for KYC Bot tests.
"""

import pytest
import os
from unittest.mock import patch


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    with patch.dict(os.environ, {
        'GOOGLE_API_KEY': 'test_api_key_for_testing',
        'GOOGLE_SEARCH_ENGINE_ID': 'test_search_engine_id'
    }):
        yield


@pytest.fixture
def sample_search_results():
    """Fixture providing sample search results."""
    return [
        {
            "title": "Test Article",
            "snippet": "This is a test snippet about the customer.",
            "link": "https://example.com/article1"
        },
        {
            "title": "Another Article",
            "snippet": "Another test snippet with relevant information.",
            "link": "https://example.com/article2"
        }
    ]


@pytest.fixture
def sample_watchlist_results_no_match():
    """Fixture providing sample watchlist results with no match."""
    return {
        "matched": False,
        "watchlists_checked": ["OFAC", "UN_Sanctions", "EU_Sanctions", "UK_Sanctions"],
        "matches": []
    }


@pytest.fixture
def sample_watchlist_results_with_match():
    """Fixture providing sample watchlist results with match."""
    return {
        "matched": True,
        "watchlists_checked": ["OFAC", "UN_Sanctions", "EU_Sanctions", "UK_Sanctions"],
        "matches": [
            {
                "watchlist": "OFAC",
                "name": "Vladimir Petrov",
                "similarity": 1.0,
                "reason": "Sanctions evasion, money laundering",
                "date_added": "2022-03-15",
                "country": "Russia"
            }
        ]
    }

