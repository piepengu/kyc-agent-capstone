"""
Unit tests for custom tools (watchlist checking, search query formatting).
"""

import pytest
from tools import (
    check_watchlist,
    format_search_query,
    normalize_name,
    calculate_similarity,
    check_name_match,
    WATCHLIST_DATA
)


class TestNormalizeName:
    """Test name normalization function."""
    
    def test_normalize_basic_name(self):
        """Test basic name normalization."""
        assert normalize_name("John Smith") == "john smith"
        assert normalize_name("  John   Smith  ") == "john smith"
    
    def test_normalize_with_punctuation(self):
        """Test normalization removes some punctuation."""
        # Apostrophes are preserved (O'Brien stays as o'brien)
        assert normalize_name("John O'Brien") == "john o'brien"
        # Hyphens are converted to spaces
        assert normalize_name("Ahmed Al-Mansouri") == "ahmed al mansouri"
        # Dots and commas are removed
        assert normalize_name("John, Smith.") == "john smith"
    
    def test_normalize_empty_string(self):
        """Test normalization of empty string."""
        assert normalize_name("") == ""
        assert normalize_name("   ") == ""
    
    def test_normalize_case_insensitive(self):
        """Test normalization is case insensitive."""
        assert normalize_name("JOHN SMITH") == "john smith"
        assert normalize_name("John Smith") == "john smith"
        assert normalize_name("john smith") == "john smith"


class TestCalculateSimilarity:
    """Test similarity calculation function."""
    
    def test_exact_match(self):
        """Test exact match returns 1.0."""
        assert calculate_similarity("John Smith", "John Smith") == 1.0
        assert calculate_similarity("Vladimir Petrov", "Vladimir Petrov") == 1.0
    
    def test_case_insensitive(self):
        """Test similarity is case insensitive."""
        assert calculate_similarity("John Smith", "john smith") == 1.0
        assert calculate_similarity("VLADIMIR PETROV", "vladimir petrov") == 1.0
    
    def test_similar_names(self):
        """Test similar names return high similarity."""
        similarity = calculate_similarity("Vlad Petrov", "Vladimir Petrov")
        assert similarity > 0.8  # Should be high similarity
    
    def test_different_names(self):
        """Test different names return low similarity."""
        similarity = calculate_similarity("John Smith", "Vladimir Petrov")
        assert similarity < 0.5  # Should be low similarity
    
    def test_substring_match(self):
        """Test substring matches get boosted similarity."""
        similarity = calculate_similarity("Vlad", "Vladimir Petrov")
        assert similarity >= 0.85  # Should be boosted for substring


class TestCheckNameMatch:
    """Test name matching against watchlist entries."""
    
    def test_exact_match(self):
        """Test exact match against watchlist entry."""
        entry = {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "Test",
            "date_added": "2022-01-01",
            "country": "Russia"
        }
        is_match, similarity = check_name_match("Vladimir Petrov", entry)
        assert is_match is True
        assert similarity == 1.0
    
    def test_alias_match(self):
        """Test match via alias."""
        entry = {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "Test",
            "date_added": "2022-01-01",
            "country": "Russia"
        }
        is_match, similarity = check_name_match("Vlad Petrov", entry)
        assert is_match is True
        assert similarity >= 0.85
    
    def test_no_match(self):
        """Test no match for different name."""
        entry = {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "Test",
            "date_added": "2022-01-01",
            "country": "Russia"
        }
        is_match, similarity = check_name_match("John Smith", entry)
        assert is_match is False
        assert similarity < 0.5
    
    def test_lower_threshold(self):
        """Test with lower threshold."""
        entry = {
            "name": "Vladimir Petrov",
            "aliases": ["Vlad Petrov", "V. Petrov"],
            "reason": "Test",
            "date_added": "2022-01-01",
            "country": "Russia"
        }
        # With very low threshold, even partial matches should match
        is_match, similarity = check_name_match("Vlad", entry, threshold=0.5)
        assert is_match is True


class TestCheckWatchlist:
    """Test watchlist checking function."""
    
    def test_exact_match_found(self):
        """Test exact match is found."""
        result = check_watchlist("Vladimir Petrov")
        assert result["matched"] is True
        assert len(result["matches"]) > 0
        assert "OFAC" in [m["watchlist"] for m in result["matches"]]
    
    def test_alias_match_found(self):
        """Test alias match is found."""
        result = check_watchlist("Vlad Petrov")
        assert result["matched"] is True
        assert len(result["matches"]) > 0
    
    def test_no_match(self):
        """Test no match for clean name."""
        result = check_watchlist("John Smith")
        assert result["matched"] is False
        assert len(result["matches"]) == 0
    
    def test_all_watchlists_checked(self):
        """Test all watchlists are checked."""
        result = check_watchlist("John Smith")
        assert len(result["watchlists_checked"]) == 4
        assert "OFAC" in result["watchlists_checked"]
        assert "UN_Sanctions" in result["watchlists_checked"]
        assert "EU_Sanctions" in result["watchlists_checked"]
        assert "UK_Sanctions" in result["watchlists_checked"]
    
    def test_match_details(self):
        """Test match details are correct."""
        result = check_watchlist("Vladimir Petrov")
        if result["matched"]:
            match = result["matches"][0]
            assert "watchlist" in match
            assert "name" in match
            assert "similarity" in match
            assert "reason" in match
            assert "date_added" in match
            assert "country" in match
            assert 0.0 <= match["similarity"] <= 1.0
    
    def test_empty_name(self):
        """Test empty name returns no match."""
        result = check_watchlist("")
        assert result["matched"] is False
        assert len(result["matches"]) == 0
    
    def test_whitespace_only_name(self):
        """Test whitespace-only name returns no match."""
        result = check_watchlist("   ")
        assert result["matched"] is False
    
    def test_custom_threshold(self):
        """Test custom similarity threshold."""
        # With very high threshold, should find fewer matches
        result_high = check_watchlist("Vlad Petrov", similarity_threshold=0.99)
        # With lower threshold, should find more matches
        result_low = check_watchlist("Vlad Petrov", similarity_threshold=0.5)
        # Lower threshold should find at least as many matches
        assert len(result_low["matches"]) >= len(result_high["matches"])


class TestFormatSearchQuery:
    """Test search query formatting function."""
    
    def test_adverse_media_query(self):
        """Test adverse media query formatting."""
        query = format_search_query("John Smith", "adverse_media")
        assert "John Smith" in query
        assert "fraud" in query.lower() or "sanctions" in query.lower()
    
    def test_fraud_query(self):
        """Test fraud query formatting."""
        query = format_search_query("John Smith", "fraud")
        assert "John Smith" in query
        assert "fraud" in query.lower() or "scam" in query.lower()
    
    def test_sanctions_query(self):
        """Test sanctions query formatting."""
        query = format_search_query("John Smith", "sanctions")
        assert "John Smith" in query
        assert "sanctions" in query.lower() or "ofac" in query.lower()
    
    def test_default_query(self):
        """Test default query type."""
        query = format_search_query("John Smith")
        assert "John Smith" in query
    
    def test_unknown_query_type(self):
        """Test unknown query type uses default."""
        query = format_search_query("John Smith", "unknown_type")
        assert "John Smith" in query
    
    def test_special_characters_in_name(self):
        """Test query formatting with special characters."""
        query = format_search_query("O'Brien", "adverse_media")
        assert "O'Brien" in query or "obrien" in query.lower()

