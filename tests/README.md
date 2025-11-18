# KYC Bot Test Suite

Comprehensive unit and integration tests for the KYC Bot system.

## Test Coverage

### Test Files

1. **`test_tools.py`** - Tests for custom tools
   - Name normalization
   - Similarity calculation
   - Name matching (with aliases)
   - Watchlist checking
   - Search query formatting

2. **`test_error_handling.py`** - Tests for error handling utilities
   - Customer name validation
   - Error classification (retryable vs non-retryable)
   - HTTP error handling
   - Network/timeout error handling

3. **`test_agents.py`** - Tests for agent classes
   - SearchAgent initialization and search functionality
   - WatchlistAgent initialization and watchlist checking
   - AnalysisAgent initialization and report generation
   - Error handling and fallback behavior

4. **`test_integration.py`** - Integration tests for workflow
   - Workflow creation
   - State flow through workflow
   - Workflow with watchlist matches
   - Error handling in workflow
   - Edge cases (empty names, etc.)

5. **`conftest.py`** - Pytest configuration and fixtures
   - Test environment setup
   - Sample data fixtures

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_tools.py
```

### Run Specific Test Class
```bash
pytest tests/test_tools.py::TestCheckWatchlist
```

### Run Specific Test
```bash
pytest tests/test_tools.py::TestCheckWatchlist::test_exact_match_found
```

### Run with Coverage Report
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run Only Unit Tests
```bash
pytest tests/ -m unit
```

### Run Only Integration Tests
```bash
pytest tests/ -m integration
```

## Test Statistics

- **Total Tests**: 63
- **Test Files**: 4
- **Coverage**: 
  - Tools: 100%
  - Error Handling: 100%
  - Agents: ~90% (mocked external APIs)
  - Integration: Core workflow paths

## Test Categories

### Unit Tests
- Test individual functions and methods in isolation
- Mock external dependencies (APIs, databases)
- Fast execution
- High coverage

### Integration Tests
- Test component interactions
- Test workflow end-to-end
- Mock external APIs but test real workflow logic
- Verify state management

## Fixtures

The `conftest.py` file provides:
- `setup_test_environment` - Sets up test environment variables
- `sample_search_results` - Sample search result data
- `sample_watchlist_results_no_match` - Watchlist results with no matches
- `sample_watchlist_results_with_match` - Watchlist results with matches

## Mocking

Tests use `unittest.mock` to:
- Mock Google Custom Search API calls
- Mock Gemini API calls
- Mock HTTP errors
- Isolate unit tests from external dependencies

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 10 seconds)
- No external dependencies required
- Deterministic results
- Clear error messages

## Adding New Tests

When adding new functionality:

1. **Add unit tests** for new functions/methods
2. **Add integration tests** if workflow changes
3. **Update fixtures** if new test data needed
4. **Maintain coverage** above 80%

### Example Test Structure

```python
class TestNewFeature:
    """Test new feature functionality."""
    
    def test_basic_functionality(self):
        """Test basic feature works."""
        result = new_feature("input")
        assert result == expected_output
    
    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            new_feature("")
```

## Notes

- All tests use pytest fixtures for setup/teardown
- External APIs are mocked to avoid rate limits and costs
- Tests are designed to be fast and reliable
- Error handling tests verify graceful degradation

