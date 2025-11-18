# Logging and Observability Guide

## Overview

The KYC Bot includes comprehensive logging and observability features to track agent execution, API calls, and performance metrics. This is a **required concept** for the competition.

## Features

### 1. Structured Logging
- **Timestamps**: All logs include precise timestamps
- **Log Levels**: INFO, WARNING, ERROR, DEBUG
- **Component Loggers**: Separate loggers for each agent and component
  - `kyc_bot.search_agent`
  - `kyc_bot.watchlist_agent`
  - `kyc_bot.analysis_agent`
  - `kyc_bot.workflow`
  - `kyc_bot.api`

### 2. Dual Output
- **Console Handler**: Real-time feedback during execution (INFO level)
- **File Handler**: Detailed logs saved to `logs/kyc_bot_YYYYMMDD.log` (DEBUG level)

### 3. Performance Tracking

#### Agent Execution Tracking
- Tracks execution time for each agent
- Records success/failure status
- Calculates average execution times

#### API Call Tracking
- Monitors all external API calls
- Tracks response times
- Records success/error rates
- Tracks endpoints called

### 4. Performance Metrics Summary

At the end of each investigation, a comprehensive summary is displayed:

```
[PERFORMANCE METRICS]
  Total Time: 7.09s
  SearchAgent: 1.85s avg
  WatchlistAgent: 0.00s avg
  AnalysisAgent: 5.20s avg
  Google Custom Search: 0.61s avg
  Gemini API: 5.20s avg
  Log file: logs/kyc_bot_20251118.log
```

## Log File Location

Logs are stored in the `logs/` directory:
- Format: `kyc_bot_YYYYMMDD.log`
- Example: `logs/kyc_bot_20251118.log`
- Encoding: UTF-8
- Level: DEBUG (more detailed than console)

## What Gets Logged

### SearchAgent
- Search query execution
- Query text and customer name
- Number of results found
- Real vs simulated results
- API call timing
- Errors and fallbacks

### WatchlistAgent
- Watchlist check initiation
- Watchlists checked
- Matches found
- Execution time

### AnalysisAgent
- Report generation start
- Input data summary (search results, watchlists)
- Report length
- Risk level assessment
- API call timing

### Workflow
- Investigation start/end
- Node execution
- State transitions
- Errors and exceptions

### API Calls
- Google Custom Search API
  - Query text
  - Response time
  - Success/failure
  - Error messages
- Gemini API
  - Endpoint called
  - Response time
  - Success/failure

## Example Log Output

```
2025-11-18 13:42:04 - kyc_bot.workflow - INFO - Starting investigation for: Test Logging
2025-11-18 13:42:04 - kyc_bot.search_agent - INFO - SearchAgent execution started
2025-11-18 13:42:04 - kyc_bot.search_agent - INFO - Search query for 'Test Logging': "Test Logging" fraud OR sanctions OR financial crime
2025-11-18 13:42:04 - kyc_bot.api - INFO - API call started: Google Custom Search - query: "Test Logging" fraud OR sanctions OR financial crime
2025-11-18 13:42:05 - kyc_bot.api - INFO - API call completed: Google Custom Search - query: "Test Logging" fraud OR sanctions OR financial crime (1.01s)
2025-11-18 13:42:05 - kyc_bot.search_agent - INFO - Search query '"Test Logging" fraud OR sanctions OR financial crime' returned 3 real results
2025-11-18 13:42:06 - kyc_bot.search_agent - INFO - SearchAgent execution completed in 1.85s
```

## Code Implementation

### Using the Logger

```python
from logger import search_logger, track_execution, track_api_call

# Track agent execution
with track_execution("SearchAgent", search_logger):
    # Agent code here
    search_logger.info("Starting search...")
    # ...

# Track API calls
with track_api_call("Google Custom Search", "query: test", api_logger):
    # API call here
    result = search_service.cse().list(...).execute()
```

### Performance Tracker

```python
from logger import performance_tracker

# Start investigation
performance_tracker.start_investigation("Customer Name")

# Track agent execution (automatic with track_execution)
# Track API calls (automatic with track_api_call)

# End investigation and log summary
performance_tracker.end_investigation()
performance_tracker.log_summary()
```

## Benefits

1. **Debugging**: Detailed logs help identify issues quickly
2. **Performance Monitoring**: Track which agents/APIs are slow
3. **Audit Trail**: Complete record of all operations
4. **Compliance**: Logs can be used for compliance reporting
5. **Optimization**: Identify bottlenecks and optimize accordingly

## Configuration

Logging is configured in `logger.py`:
- Console level: INFO
- File level: DEBUG
- Format: Timestamp - Logger Name - Level - Message
- File format includes function name and line number

## Log Rotation

Logs are created daily (one file per day). For production, consider:
- Log rotation (keep last N days)
- Log compression for old files
- Centralized logging (e.g., Cloud Logging)

## Security Note

⚠️ **Important**: Log files may contain sensitive information (customer names, search queries). Ensure:
- Log files are excluded from git (already in `.gitignore`)
- Log files are stored securely
- Log retention policies are followed
- Access to logs is restricted

