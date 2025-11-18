# **KYC Bot: A Multi-Agent System for Automated KYC Compliance**

Track: Concierge Agents  
Project for: Kaggle Agents Intensive Capstone Project (Nov 2025\)

## **The Pitch (Category 1: 30 Points)**

### **The Problem (Why?)**

In the financial industry, "Know Your Customer" (KYC) compliance is a mandatory, high-stakes, and incredibly manual process. When onboarding a new client, a compliance officer must perform a multi-hour investigation:

* **Manual Searches:** Sift through dozens of search results for "adverse media"—any news linking the client to fraud, sanctions, or other financial crimes.  
* **Repetitive Checks:** Cross-reference client names against numerous, disconnected international watchlists.  
* **Data Silos:** Collate this disparate information into a coherent report to make a risk-based decision.

This process is a costly bottleneck. It's slow for the bank, frustrating for the new customer, and prone to human error—an analyst might miss a crucial article on page 5 of a search.

### **The Solution (What?)**

The **KYC Bot** is an autonomous "Concierge Agent" built on a multi-agent framework. It's designed to act as a junior analyst, automating 90% of the manual investigation.

Given a new customer's name, the agent autonomously executes a three-step investigative workflow:

1. **SearchAgent:** Dynamically generates and executes multiple "adverse media" search queries using the Google Search tool.  
2. **WatchlistAgent:** Checks the name against a simulated international sanctions database using a custom-built tool.  
3. **AnalysisAgent:** Reads the complete findings from the other agents, uses a Gemini model to analyze the context, and generates a final, structured risk report.

### **The Value (Impact)**

This agent transforms the KYC process from a manual, multi-hour task into a 5-minute automated review.

* **For the Compliance Officer:** It eliminates manual data gathering, freeing them to focus on high-level analysis. Instead of spending 2 hours *searching*, they spend 10 minutes *reviewing* a pre-compiled report.  
* **For the Business:** It dramatically reduces onboarding friction, cuts operational costs, and ensures a consistent, auditable compliance process every single time.

*(This is a placeholder for Day 8\)*

## **Architecture**

### **System Overview**

The KYC Bot is built as a **sequential multi-agent system** using **LangGraph** for orchestration. The architecture follows a pipeline pattern where three specialized agents work in sequence, each contributing to the final risk assessment.

### **Core Components**

1. **LangGraph StateGraph**: Orchestrates the sequential workflow
2. **AgentState TypedDict**: Manages shared state between agents
3. **Three Specialized Agents**: SearchAgent, WatchlistAgent, AnalysisAgent
4. **Custom Tools**: Watchlist checking and query formatting
5. **Logging & Observability**: Comprehensive tracking and metrics

### **Workflow Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Input                               │
│                    (Customer Name)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │   main.py      │
                    │  Entry Point   │
                    └────────┬───────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │   LangGraph StateGraph       │
              │   (Sequential Workflow)      │
              └──────────────┬───────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │         AgentState (TypedDict)             │
        │  • customer_name: str                      │
        │  • search_results: List[Dict]              │
        │  • watchlist_results: Dict                 │
        │  • final_report: str                       │
        │  • error: str                              │
        └────────────────────────────────────────────┘
                             │
                             ▼
        ┌────────────────────────────────────────────┐
        │         Node 1: SearchAgent                │
        │  • Generates search queries                │
        │  • Calls Google Custom Search API          │
        │  • Collects adverse media results          │
        │  • Updates: search_results                 │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │      Node 2: WatchlistAgent                │
        │  • Uses custom check_watchlist tool        │
        │  • Checks 4 watchlists (OFAC, UN, EU, UK) │
        │  • Updates: watchlist_results              │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
        ┌────────────────────────────────────────────┐
        │        Node 3: AnalysisAgent               │
        │  • Uses Gemini 2.0 Flash                   │
        │  • Analyzes all findings                   │
        │  • Generates risk assessment report        │
        │  • Updates: final_report                   │
        └──────────────┬─────────────────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Final Report  │
              │  (Output)      │
              └────────────────┘
```

### **Sequential Workflow**

The workflow is **strictly sequential** - each agent must complete before the next begins:

1. **SearchAgent** → Searches for adverse media
2. **WatchlistAgent** → Checks watchlists (uses search results context)
3. **AnalysisAgent** → Generates report (uses both search and watchlist results)

**Code Reference**: See `graph.py`, lines 206-228 for workflow definition.

### **State Management**

State is managed using a **TypedDict** (`AgentState`) that flows through all nodes:

```python
class AgentState(TypedDict):
    customer_name: str              # Input: Customer to investigate
    search_results: List[Dict]      # Output from SearchAgent
    watchlist_results: Dict         # Output from WatchlistAgent
    final_report: str               # Output from AnalysisAgent
    error: str                      # Error tracking
```

**State Flow**:
- **Initial State**: Only `customer_name` is set (see `main.py`, lines 43-49)
- **After SearchAgent**: `search_results` populated
- **After WatchlistAgent**: `watchlist_results` populated
- **After AnalysisAgent**: `final_report` populated

**Code Reference**: See `graph.py`, lines 69-76 for state definition.

### **Agent Communication**

Agents communicate **only through shared state** - they do not directly call each other:

1. **SearchAgent** reads `customer_name`, writes `search_results`
2. **WatchlistAgent** reads `customer_name`, writes `watchlist_results`
3. **AnalysisAgent** reads `customer_name`, `search_results`, `watchlist_results`, writes `final_report`

This design ensures:
- **Loose coupling**: Agents are independent
- **Testability**: Each agent can be tested in isolation
- **Maintainability**: Easy to modify individual agents
- **Observability**: State transitions are logged

**Code Reference**: See `graph.py`, lines 99-203 for node implementations.

### **Agent Details**

#### **1. SearchAgent** (`agents.py`, lines 16-160)

**Purpose**: Search for adverse media about the customer

**Tools Used**:
- **Built-in**: Google Custom Search API (via `googleapiclient`)
- **Custom**: `format_search_query()` helper

**Process**:
1. Generates 3 search queries (fraud, sanctions, financial crime)
2. Executes each query via Google Custom Search API
3. Collects results (title, snippet, link)
4. Falls back to simulated results if API fails

**Output**: List of search result dictionaries

#### **2. WatchlistAgent** (`agents.py`, lines 180-233)

**Purpose**: Check customer against sanctions watchlists with fuzzy matching

**Tools Used**:
- **Custom**: `check_watchlist()` tool with fuzzy matching and alias support

**Process**:
1. Calls `check_watchlist()` with customer name
2. Checks against 4 watchlists: OFAC, UN, EU, UK
3. Uses fuzzy matching to handle name variations and aliases
4. Returns match status, similarity scores, and detailed match information

**Output**: Dictionary with:
- `matched`: bool - Whether any matches found
- `watchlists_checked`: List[str] - Watchlists checked
- `matches`: List[Dict] - Detailed match information including:
  - Watchlist name
  - Matched name
  - Similarity score (0.0-1.0)
  - Reason for listing
  - Date added
  - Country

#### **3. AnalysisAgent** (`agents.py`, lines 210-333)

**Purpose**: Generate comprehensive risk assessment report

**Tools Used**:
- **Built-in**: Gemini 2.0 Flash (`models/gemini-2.0-flash-exp`)

**Process**:
1. Formats search results and watchlist results
2. Constructs prompt with all findings
3. Calls Gemini API to generate report
4. Returns structured risk assessment

**Output**: Formatted risk assessment report (markdown)

### **Error Handling**

The system includes comprehensive error handling with multiple layers:

1. **Input Validation**: Customer names are validated before processing
   - Minimum length: 2 characters
   - Maximum length: 200 characters
   - Invalid character filtering
   - **Code Reference**: `error_handling.py`, `validate_customer_name()` function

2. **Retry Logic**: API calls use exponential backoff retry
   - Google Custom Search: 2 retries with 1s initial delay
   - Gemini API: 2 retries with 1s initial delay
   - Automatic retry for transient errors (rate limits, network issues)
   - **Code Reference**: `error_handling.py`, `retry_with_backoff()` decorator

3. **Error Classification**: Errors are classified as retryable or non-retryable
   - Retryable: Network errors, rate limits, server errors (5xx)
   - Non-retryable: Authentication errors, invalid requests (4xx)
   - **Code Reference**: `error_handling.py`, `classify_error()` function

4. **Graceful Degradation**: System continues even when components fail
   - Search failures: Falls back to simulated results
   - Report generation failures: Generates basic fallback report
   - Workflow continues to completion even with partial failures
   - **Code Reference**: `graph.py`, all node functions with try-except blocks

5. **User-Friendly Messages**: Clear, actionable error messages
   - Explains what went wrong
   - Suggests what to check
   - Provides context for troubleshooting

**Code Reference**: 
- Error handling utilities: `error_handling.py`
- Node error handling: `graph.py`, lines 113-150, 167-204, 200-248
- Agent error handling: `agents.py`, lines 140-154, 352-387

### **Logging & Observability**

The system includes comprehensive logging:
- **Structured logging** with timestamps
- **Performance tracking** for each agent
- **API call monitoring** (Google Search, Gemini)
- **File logging** to `logs/` directory

**Code Reference**: See `logger.py` for implementation details.

### **Technology Stack**

- **LangGraph**: Workflow orchestration
- **Google Generative AI**: Gemini 2.0 Flash for analysis
- **Google Custom Search API**: Adverse media searches
- **Python TypedDict**: Type-safe state management
- **Python Logging**: Structured logging and observability

### **Design Patterns**

1. **Sequential Pipeline**: Agents execute in strict order
2. **State-Based Communication**: Agents communicate via shared state
3. **Lazy Initialization**: Agents initialized on first use
4. **Graceful Degradation**: Fallbacks when APIs fail
5. **Separation of Concerns**: Each agent has a single responsibility

## **How to Run**

### **Day 1 Setup (Initial Setup)**

1. **Prerequisites:**
   - Python 3.9 or higher (required for LangGraph)
   - Check your Python version: `python --version`
   
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys:**
   - Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Get your Google Custom Search Engine ID from [Google Custom Search](https://programmablesearchengine.google.com/)
   - Create a `.env` file in the project root:
     ```bash
     GOOGLE_API_KEY=your_api_key_here
     GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
     ```
   - **Important:** Make sure Custom Search API is enabled in [Google Cloud Console](https://console.cloud.google.com/apis/library) and your API key allows Custom Search API (see [FIX_API_KEY_RESTRICTIONS.md](FIX_API_KEY_RESTRICTIONS.md) for details)

4. **Test the setup:**
   ```bash
   # Activate virtual environment first
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   venv\Scripts\activate.bat     # Windows CMD
   
   # Run the agent
   python main.py --name "Test Customer"
   ```
   
   **📖 For detailed testing instructions, see [TESTING.md](TESTING.md)**

### **Project Structure**

```
.
├── main.py              # Main entry point and agent orchestration
├── graph.py             # LangGraph workflow definition
├── agents.py            # Agent definitions (SearchAgent, WatchlistAgent, AnalysisAgent)
├── tools.py             # Custom tools (watchlist checking, query formatting)
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (API keys) - not in git
├── .env.example         # Example environment variables file
├── .gitignore          # Git ignore file
└── Readme.md           # This file
```

### **Current Status: Day 2**

✅ Project structure created  
✅ Basic agent skeletons implemented  
✅ State management framework set up  
✅ LangGraph workflow implemented  
✅ AnalysisAgent with Gemini 2.0 Flash  
✅ WatchlistAgent with custom tool  
✅ SearchAgent with Google Custom Search API (real search results)  
✅ End-to-end workflow functional  
✅ Google Custom Search API integrated and working  
⏳ Enhanced error handling (in progress)

### **Day 2 Achievements**

- **LangGraph Integration**: Sequential multi-agent workflow using StateGraph
- **Gemini 2.0 Flash**: AnalysisAgent generates comprehensive risk reports
- **Custom Tools**: WatchlistAgent uses custom check_watchlist tool
- **State Management**: AgentState TypedDict manages data flow between agents
- **Google Custom Search API**: SearchAgent now uses real Google Custom Search API for adverse media searches
- **Working Pipeline**: Full end-to-end execution from customer name to risk report with real search results

## **Key Concepts Used**

This section explicitly maps our code to the course's key concepts for the judges. Each concept includes specific file paths and line numbers for verification.

### **1. Multi-Agent System (Sequential)** ✅

**Concept**: Sequential workflow where agents execute one after another in a defined order.

**Implementation**:
- **File**: `graph.py`
- **Lines**: 206-228 (`create_workflow()` function)
- **Code**: 
  ```python
  workflow = StateGraph(AgentState)
  workflow.add_node("search_agent", search_node)
  workflow.add_node("watchlist_agent", watchlist_node)
  workflow.add_node("analysis_agent", analysis_node)
  workflow.set_entry_point("search_agent")
  workflow.add_edge("search_agent", "watchlist_agent")
  workflow.add_edge("watchlist_agent", "analysis_agent")
  workflow.add_edge("analysis_agent", END)
  ```

**How it works**: 
- LangGraph `StateGraph` orchestrates the sequential flow
- Each agent is a node in the graph
- Edges define the execution order: SearchAgent → WatchlistAgent → AnalysisAgent
- State flows through each node sequentially

**Node Implementations**:
- `search_node()`: `graph.py`, lines 99-129
- `watchlist_node()`: `graph.py`, lines 132-162
- `analysis_node()`: `graph.py`, lines 165-203

### **2. Tools (Built-in)** ✅

**Concept**: Using external APIs and services as tools for agents.

**Implementation - Google Custom Search API**:
- **File**: `agents.py`
- **Lines**: 70-78 (initialization), 112-117 (usage)
- **Code**:
  ```python
  from googleapiclient.discovery import build
  self.search_service = build("customsearch", "v1", developerKey=self.api_key)
  result = self.search_service.cse().list(q=query, cx=self.search_engine_id, num=3).execute()
  ```

**How it works**:
- SearchAgent uses Google Custom Search API via `googleapiclient` library
- Executes multiple search queries for adverse media
- Returns structured results (title, snippet, link)
- Falls back to simulated results if API fails

**Implementation - Gemini API**:
- **File**: `agents.py`
- **Lines**: 241-243 (initialization), 310-312 (usage)
- **Code**:
  ```python
  import google.generativeai as genai
  genai.configure(api_key=api_key)
  self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
  response = self.model.generate_content(prompt)
  ```

**How it works**:
- AnalysisAgent uses Gemini 2.0 Flash for report generation
- Sends formatted prompt with all findings
- Receives structured risk assessment report

### **3. Tools (Custom)** ✅

**Concept**: Creating custom tools that agents can use for specialized tasks.

**Implementation - check_watchlist Tool**:
- **File**: `tools.py`
- **Lines**: 196-261 (`check_watchlist()` function)
- **Features**:
  - **Fuzzy Matching**: Uses `difflib.SequenceMatcher` for name similarity scoring
  - **Alias Support**: Checks known aliases for each watchlist entry
  - **Name Normalization**: Normalizes names (lowercase, removes punctuation) for better matching
  - **Similarity Threshold**: Configurable threshold (default 0.85) for match detection
  - **Realistic Sample Data**: Includes sample entries for OFAC, UN, EU, and UK sanctions lists

**Code**:
```python
def check_watchlist(customer_name: str, similarity_threshold: float = 0.85) -> Dict:
    """Custom tool to check a customer name against watchlists with fuzzy matching."""
    # Checks against OFAC, UN, EU, UK watchlists
    # Returns match status, similarity scores, and detailed match information
```

**Supporting Functions**:
- `normalize_name()` (lines 118-136): Normalizes names for comparison
- `calculate_similarity()` (lines 139-165): Computes similarity score between names
- `check_name_match()` (lines 168-193): Checks if customer name matches entry (including aliases)

**Usage**:
- **File**: `agents.py`
- **Lines**: 21 (import), 215 (call in WatchlistAgent)
- **Code**:
  ```python
  from tools import check_watchlist
  results = check_watchlist(customer_name)
  ```

**How it works**:
- Custom tool with realistic sample watchlist data
- Checks against 4 international sanctions lists (OFAC, UN, EU, UK)
- Uses fuzzy matching to handle name variations (e.g., "Vlad Petrov" matches "Vladimir Petrov")
- Checks aliases for each watchlist entry
- Returns structured results with match status, similarity scores, and detailed information
- Can be extended to connect to real watchlist databases

**Example Results**:
- Exact match: "Vladimir Petrov" → 4 matches (100% similarity)
- Alias match: "Vlad Petrov" → 4 matches (100% similarity via alias)
- No match: "John Smith" → 0 matches

**Implementation - format_search_query Helper**:
- **File**: `tools.py`
- **Lines**: 264-285
- **Usage**: `agents.py`, line 107

### **4. Sessions & Memory** ✅

**Concept**: Managing and persisting state across agent interactions.

**Implementation - AgentState TypedDict**:
- **File**: `graph.py`
- **Lines**: 69-76 (state definition)
- **Code**:
  ```python
  class AgentState(TypedDict):
      customer_name: str
      search_results: List[Dict[str, str]]
      watchlist_results: Dict
      final_report: str
      error: str
  ```

**State Initialization**:
- **File**: `main.py`
- **Lines**: 43-49
- **Code**:
  ```python
  initial_state: AgentState = {
      "customer_name": args.name,
      "search_results": [],
      "watchlist_results": {},
      "final_report": "",
      "error": ""
  }
  ```

**State Flow**:
1. **Initial**: Only `customer_name` set (`main.py`, lines 43-49)
2. **After SearchAgent**: `search_results` populated (`graph.py`, lines 119-123)
3. **After WatchlistAgent**: `watchlist_results` populated (`graph.py`, lines 152-156)
4. **After AnalysisAgent**: `final_report` populated (`graph.py`, lines 192-196)

**How it works**:
- TypedDict ensures type safety
- State is immutable between nodes (new state returned)
- Each node reads from and writes to state
- State persists throughout the entire workflow

### **5. Logging & Observability** ✅ (Bonus/Required Concept)

**Concept**: Tracking agent execution, API calls, and performance metrics.

**Implementation**:
- **File**: `logger.py`
- **Key Components**:
  - Structured logging: Lines 18-51
  - Performance tracking: Lines 32-183
  - Agent execution tracking: Lines 189-205
  - API call tracking: Lines 208-227

**Usage in Agents**:
- **SearchAgent**: `agents.py`, lines 95, 97, 105, 112, 128, 134, 145, 156, 158
- **WatchlistAgent**: `agents.py`, lines 188, 190, 198, 201, 204
- **AnalysisAgent**: `agents.py`, lines 263, 265, 266, 310

**How it works**:
- Each agent execution is tracked with timestamps
- API calls are monitored for performance
- Metrics are logged to both console and file
- Performance summary generated at end

### **6. Use Gemini** ✅ (Bonus)

**Concept**: Using Google's Gemini model for AI-powered analysis.

**Implementation**:
- **File**: `agents.py`
- **Lines**: 241-243 (model initialization), 310-312 (content generation)
- **Model**: `models/gemini-2.0-flash-exp`
- **Code**:
  ```python
  genai.configure(api_key=api_key)
  self.model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
  response = self.model.generate_content(prompt)
  ```

**How it works**:
- AnalysisAgent uses Gemini 2.0 Flash to analyze all findings
- Generates comprehensive risk assessment reports
- Provides structured output with risk levels and recommendations

### **Summary Table**

| Concept | File | Lines | Status |
|---------|------|-------|--------|
| Multi-Agent System (Sequential) | `graph.py` | 206-228 | ✅ |
| Tools (Built-in) - Google Search | `agents.py` | 70-78, 112-117 | ✅ |
| Tools (Built-in) - Gemini | `agents.py` | 241-243, 310-312 | ✅ |
| Tools (Custom) - check_watchlist | `tools.py` | 196-261 | ✅ |
| Sessions & Memory - AgentState | `graph.py` | 69-76 | ✅ |
| Sessions & Memory - State Init | `main.py` | 43-49 | ✅ |
| Logging & Observability | `logger.py` | Throughout | ✅ |
| Use Gemini (Bonus) | `agents.py` | 241-243, 310-312 | ✅ |

## **Deployment Strategy**

*This agent is designed for a serverless deployment on **Google Cloud Run**, referencing the concepts from the **Day 5 MLOps Codelab**. The "Agent Starter Pack" provides a template for this, allowing the agent to be triggered via a secure API...*

*(This is a placeholder for Day 11\)*

## **Project Video**

*\[Link to 2-minute YouTube demo video\]*