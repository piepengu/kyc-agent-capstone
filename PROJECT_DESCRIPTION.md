# KYC Bot - Automated KYC Compliance Agent

## Problem Statement

Know Your Customer (KYC) compliance is a critical requirement for financial institutions, but the process is time-consuming, error-prone, and resource-intensive. Compliance officers must manually search for adverse media, check multiple sanctions watchlists, and synthesize information from various sources to assess customer risk. This manual process can take hours per customer, is subject to human error, and doesn't scale efficiently.

The problem becomes even more challenging with name variations, information overload from hundreds of search results, multiple disconnected data sources, inconsistent assessments, and slow processing that delays customer onboarding.

This is an important problem because:
1. **Regulatory compliance**: Financial institutions face severe penalties for non-compliance with KYC regulations
2. **Risk management**: Inadequate KYC checks can lead to onboarding high-risk customers, resulting in financial and reputational damage
3. **Operational efficiency**: Manual processes are costly and don't scale with business growth
4. **Customer experience**: Slow KYC processes delay customer onboarding and impact user satisfaction

## Why Agents?

Agents are the perfect solution for this problem because KYC compliance requires **intelligent orchestration of multiple specialized tasks** that benefit from autonomous decision-making and tool usage.

### Multi-Task Coordination
KYC compliance involves distinct sequential tasks: adverse media search, watchlist screening, and risk assessment. Each task has different requirements and data sources, making a multi-agent system ideal where specialized agents handle each domain.

### Tool Integration
Agents excel at using tools, which is essential for KYC. The system integrates Google Custom Search API for real-time searches, a custom watchlist tool with fuzzy matching, and Gemini AI for report generation. Agents autonomously select and use these tools, making the system flexible and extensible.

### State Management & Decision-Making
Agents orchestrated by LangGraph maintain state throughout the investigation, allowing each agent to build upon previous findings. The AnalysisAgent uses Gemini AI to intelligently assess risk, understanding context and generating human-readable reports - tasks that benefit from AI-powered agents rather than rigid rule-based systems. Agent-based systems can process multiple customers in parallel and maintain consistent quality, addressing scalability and consistency challenges.

## What we Created

### Overall Architecture

KYC Bot is a **sequential multi-agent system** built with LangGraph that automates the entire KYC compliance workflow. The system consists of three specialized agents working together:

```
┌─────────────────────────────────────────────────────────────┐
│                    KYC Bot Workflow                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Customer Name  │
                    └────────┬────────┘
                             │
                             ▼
        ┌──────────────────────────────────────┐
        │      SearchAgent                     │
        │  - Google Custom Search API          │
        │  - Multiple query types              │
        │  - Adverse media discovery           │
        └────────────┬─────────────────────────┘
                     │ search_results
                     ▼
        ┌──────────────────────────────────────┐
        │      WatchlistAgent                  │
        │  - Custom watchlist tool             │
        │  - Fuzzy matching                    │
        │  - Alias support                     │
        │  - OFAC, UN, EU, UK sanctions        │
        └────────────┬─────────────────────────┘
                     │ watchlist_results
                     ▼
        ┌──────────────────────────────────────┐
        │      AnalysisAgent                   │
        │  - Gemini 2.0 Flash                  │
        │  - Risk assessment                   │
        │  - Report generation                 │
        └────────────┬─────────────────────────┘
                     │ final_report
                     ▼
        ┌──────────────────────────────────────┐
        │      Risk Assessment Report          │
        │  - Risk level (LOW/MEDIUM/HIGH)      │
        │  - Key findings                      │
        │  - Recommendations                   │
        └──────────────────────────────────────┘
```

### Core Components

**1. SearchAgent**
- Searches for adverse media using Google Custom Search API
- Generates multiple query types (fraud, sanctions, financial crime)
- Collects and structures search results (title, snippet, link)
- Falls back to simulated results if API fails

**2. WatchlistAgent**
- Checks customer against 4 international sanctions lists (OFAC, UN, EU, UK)
- Uses fuzzy matching with SequenceMatcher for name variations
- Supports alias matching (e.g., "Vlad Petrov" matches "Vladimir Petrov")
- Returns similarity scores and detailed match information

**3. AnalysisAgent**
- Synthesizes search results and watchlist matches
- Uses Gemini 2.0 Flash to generate comprehensive risk assessment reports
- Provides structured output with risk level, findings, and recommendations
- Includes fallback report generation on errors

**4. State Management**
- Uses LangGraph's TypedDict for type-safe state management
- State flows through: customer_name → search_results → watchlist_results → final_report

**5. Error Handling & Observability**
- Comprehensive error handling with retry logic (exponential backoff)
- Error classification (retryable vs non-retryable)
- Structured logging and performance tracking

## Demo

### Example 1: High-Risk Customer (Watchlist Match)

**Input:** `Vladimir Petrov`

**Output:**
```
[!] WARNING: 4 match(es) found in watchlists!
   - OFAC: Vladimir Petrov (similarity: 100.0%)
     Reason: Sanctions evasion, money laundering
   - UN_Sanctions: Vladimir Petrov (similarity: 100.0%)
     Reason: UN Security Council sanctions
   - EU_Sanctions: Vladimir Petrov (similarity: 100.0%)
     Reason: EU sanctions - Ukraine conflict
   - UK_Sanctions: Vladimir Petrov (similarity: 100.0%)
     Reason: UK sanctions - Ukraine conflict

Risk Level: HIGH
```

The system successfully identifies the customer across all four watchlists and generates a comprehensive report with recommendations for Enhanced Due Diligence.

### Example 2: Alias Matching

**Input:** `Vlad Petrov` (alias of Vladimir Petrov)

**Output:**
```
[!] WARNING: 4 match(es) found in watchlists!
   - OFAC: Vladimir Petrov (similarity: 100.0%)
```

The fuzzy matching algorithm correctly identifies this as an alias match, demonstrating the system's ability to handle name variations.

### Example 3: Low-Risk Customer

**Input:** `Grigor Dimitrov`

**Output:**
```
[+] No matches found in 4 watchlists
Risk Level: LOW
```

The system completes the investigation, finds no adverse media or watchlist matches, and recommends standard KYC procedures.

### Key Features Demonstrated:
- ✅ Real-time adverse media search using Google Custom Search
- ✅ Intelligent watchlist matching with fuzzy logic
- ✅ AI-powered risk assessment and report generation
- ✅ Comprehensive error handling and performance tracking

## The Build

### Technologies & Tools

**Core Framework:**
- **LangGraph** - Agent orchestration and workflow management
- **LangChain** - Agent framework and tool integration
- **Python 3.13** - Primary programming language

**AI & APIs:**
- **Google Gemini 2.0 Flash** - Risk assessment and report generation
- **Google Custom Search API** - Real-time adverse media searches
- **Google Generative AI SDK** - Gemini integration

**Custom Tools:**
- **Watchlist Tool** - Custom implementation with fuzzy matching using `difflib.SequenceMatcher`
- **Search Query Formatter** - Intelligent query generation for different search types

**Error Handling & Observability:**
- **Custom Error Handling Module** - Retry logic, error classification, input validation
- **Structured Logging** - Python logging with file and console handlers
- **Performance Tracking** - Execution time tracking for agents and API calls

**Testing:**
- **pytest** - Unit and integration testing framework
- **pytest-cov** - Code coverage analysis
- **pytest-mock** - Mocking external dependencies
- **63 tests** with 81% code coverage

### Development Process

1. **Architecture Design**: Sequential workflow with three specialized agents
2. **Tool Development**: Custom watchlist tool with fuzzy matching and alias support
3. **API Integration**: Google Custom Search and Gemini APIs with error handling
4. **State Management**: Type-safe state management with LangGraph TypedDict
5. **Error Handling**: Comprehensive error handling with retry logic and graceful degradation
6. **Logging**: Structured logging and performance tracking
7. **Testing**: Comprehensive test suite covering all components (63 tests, 81% coverage)
8. **Documentation**: Complete architecture and key concepts documentation

### Key Design Decisions

- **Sequential Workflow**: Ensures each agent has complete context from previous steps
- **Fuzzy Matching**: Handles name variations and aliases, critical for real-world KYC scenarios
- **Graceful Degradation**: System continues to function even when APIs fail
- **Type Safety**: TypedDict for state management to catch errors early
- **Comprehensive Logging**: Detailed logging for debugging and compliance auditing

### Code Quality

- **81% code coverage** with 63 comprehensive tests
- **Type hints** throughout the codebase
- **Error handling** at every layer
- **Modular design** for easy extension and maintenance

## If I Had More Time, This Is What I'd Do

### 1. Enhanced Risk Assessment
- **Rule-based scoring system**: Combine AI assessment with explicit rules for consistency
- **Numerical risk scores**: Add 0-100 scores in addition to categorical levels
- **Historical pattern analysis**: Learn from past investigations to improve accuracy
- **Multi-factor assessment**: Consider transaction patterns, geographic risk, etc.

### 2. Real Watchlist Integration
- **Connect to real sanctions databases**: Integrate with actual OFAC, UN, EU, and UK sanctions APIs
- **PEP (Politically Exposed Person) screening**: Add PEP database checks
- **Real-time watchlist updates**: Subscribe to watchlist update feeds
- **Entity resolution**: Better handling of corporate entities and complex ownership structures

### 3. Advanced Search & ML
- **Multi-language support and date filtering** for international customers
- **Source credibility scoring and sentiment analysis** of adverse media
- **ML models** for false positive reduction, risk prediction, and anomaly detection

### 4. User Interface & API
- **Web interface** for compliance officers
- **REST API** for integration with existing systems
- **Batch processing** and report customization

### 5. Compliance, Performance & Integrations
- **Compliance**: Audit trail, regulatory reporting, workflow management
- **Performance**: Parallel processing, caching, cloud deployment to Google Cloud Run
- **Integrations**: Document/identity verification, credit bureau, blockchain analysis

These enhancements would transform KYC Bot from a proof-of-concept into a production-ready enterprise solution capable of handling thousands of customers daily while maintaining high accuracy and compliance standards.

