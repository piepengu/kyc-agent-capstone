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

*This section will detail our technical design. The system is built using **LangGraph** to manage a sequential, multi-agent workflow. The state is managed in a TypedDict...*

*(This is a placeholder for Day 9\)*

## **How to Run**

### **Day 1 Setup (Initial Setup)**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key:**
   - Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a `.env` file in the project root:
     ```bash
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Or export it as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```

3. **Test the setup:**
   ```bash
   python main.py --name "Test Customer"
   ```

### **Project Structure**

```
.
├── main.py              # Main entry point and agent orchestration
├── agents.py            # Agent definitions (SearchAgent, WatchlistAgent, AnalysisAgent)
├── tools.py             # Custom tools (watchlist checking, query formatting)
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables file
├── .gitignore          # Git ignore file
└── Readme.md           # This file
```

### **Current Status: Day 1**

✅ Project structure created  
✅ Basic agent skeletons implemented  
✅ State management framework set up  
⏳ Agent implementations (in progress)  
⏳ Tool integrations (in progress)  
⏳ LangGraph workflow (pending)

*(Full implementation will be completed in subsequent days)*

## **Key Concepts Used**

*This section will explicitly map our code to the course's key concepts for the judges.*

1. **Multi-agent system (Sequential):** See main.py, line 42\. Our LangGraph StateGraph defines the sequential flow between the SearchAgent, WatchlistAgent, and AnalysisAgent.  
2. **Tools (Built-in):** See agents.py, line 15\. The SearchAgent is equipped with the GoogleSearch tool.  
3. **Tools (Custom):** See tools.py, line 8\. We built a custom check\_watchlist tool for our WatchlistAgent.  
4. **Sessions & Memory:** See main.py, line 25\. The AgentState TypedDict is used to manage and pass state between all nodes in the graph.  
5. **(Bonus) Use Gemini:** See agents.py, line 30\. The AnalysisAgent uses the gemini-2.5-flash model to generate its final report.  
6. **(Bonus) Deployment:** See the "Deployment Strategy" section below.

*(This is a placeholder for Day 7\)*

## **Deployment Strategy**

*This agent is designed for a serverless deployment on **Google Cloud Run**, referencing the concepts from the **Day 5 MLOps Codelab**. The "Agent Starter Pack" provides a template for this, allowing the agent to be triggered via a secure API...*

*(This is a placeholder for Day 11\)*

## **Project Video**

*\[Link to 2-minute YouTube demo video\]*