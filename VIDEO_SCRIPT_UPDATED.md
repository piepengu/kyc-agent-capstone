# KYC Bot - Video Script (Updated for Demo.html)
## 2-Minute Video Production Plan

---

## Phase 1: Preparation (Gather Assets)

### Screen Recordings Needed:

1. **The "Pain" Shot** (Optional - 5 seconds):
   - Open Google, search "Vladimir Petrov fraud"
   - Scroll through results
   - Show manual effort

2. **The "Magic" Shot - Main Demo** (30-40 seconds):
   - **Record demo.html in action:**
     - Open demo.html in browser (full screen, F11)
     - Show the beautiful dark-themed interface
     - **Recommended: Use "Demo Mode" for main demo** (faster, more reliable)
     - Enter "Grigor Dimitrov" (shows LOW risk - matches real API)
     - Click "🎬 Demo Mode" button
     - **Capture these moments:**
       - Agent logs streaming in real-time (terminal panel)
       - SearchAgent logs appearing
       - WatchlistAgent logs with match results
       - AnalysisAgent generating report
       - Final report appearing in right panel with risk level badge
   - **Optional: Show one "Real Investigation"** (30-60 sec):
     - Enter "Shakira" (shows MEDIUM risk - matches real API)
     - Click "🔍 Run Real Investigation"
     - Show it's actually calling the live API
     - Wait for real results (can speed up in editing)

3. **The "Code" Shots** (30 seconds):
   - Open VS Code with these files ready:
     - `graph.py` - Show the workflow graph definition
     - `tools.py` - Show the fuzzy matching logic
     - `agents.py` - Show the Gemini API call

4. **The Architecture Diagram**:
   - Screenshot from README.md (Workflow Architecture section)
   - Or use the ASCII diagram from the README

---

## Phase 2: The Script (2-Minute Limit)

**Read at a steady, conversational pace (~300 words)**

### [0:00 - 0:20] The Hook & Problem

> "In the financial world, onboarding a new client isn't simple. It involves 'Know Your Customer' or KYC compliance—a manual nightmare of Googling for adverse media, checking scattered sanctions lists, and writing reports. It's slow, expensive, and prone to human error.
>
> I'm [Your Name], and for the Kaggle Agents Capstone, I built the KYC Bot: An autonomous concierge agent that turns a 2-hour investigation into a 2-minute automated review."

### [0:20 - 0:55] The Demo (Show, Don't Just Tell)

> "Let's look at it in action. I simply enter a customer name and click 'Run Investigation'.
>
> **Visual: Show demo.html interface, enter "Grigor Dimitrov", click "Demo Mode" button**
>
> Under the hood, a Sequential Multi-Agent System springs to life.
>
> **Visual: Highlight terminal logs streaming in real-time**
>
> First, the SearchAgent uses the Google Custom Search API to find adverse media regarding fraud or financial crime.
>
> **Visual: Show SearchAgent logs appearing: "Querying Google Custom Search API..."**
>
> Next, the WatchlistAgent takes over. It doesn't just look for exact matches; it uses a custom tool with fuzzy matching logic to check international sanctions lists like OFAC and the UN, handling aliases automatically.
>
> **Visual: Show WatchlistAgent logs: "Performing fuzzy matching check..." then "Scan Complete. 0 Matches found"**
>
> Finally, the AnalysisAgent reads all this data and uses Gemini 2.0 Flash to synthesize a professional risk assessment.
>
> **Visual: Show AnalysisAgent logs: "Sending context to Gemini 2.0 Flash..." then report panel appearing with LOW risk badge**

### [0:55 - 1:35] The Architecture (Technical Deep Dive)

> "Here is how I built it. I used LangGraph to orchestrate a state-based workflow.
>
> **Visual: Show Architecture Diagram from README**
>
> The AgentState flows sequentially through three nodes. The agents are decoupled—they don't talk to each other; they only communicate by updating the shared state.
>
> **Visual: Show graph.py code, highlight StateGraph and AgentState**
>
> I implemented Custom Tools for the watchlist logic to ensure we catch name variations, and I utilized Built-in Tools to leverage Gemini's reasoning capabilities.
>
> **Visual: Show tools.py (fuzzy matching), then agents.py (Gemini call)**
>
> The system also features comprehensive logging and error handling, ensuring that if one search fails, the investigation continues without crashing."

### [1:35 - 2:00] Impact & Conclusion

> "The result is this: A structured, auditable risk report generated in seconds.
>
> **Visual: Scroll through the final report in demo.html, highlight risk level badge**
>
> The KYC Bot demonstrates how Concierge Agents can automate high-stakes, complex workflows, freeing up compliance officers to focus on decisions, not data gathering.
>
> **Visual: Show deployed service URL or GitHub link**
>
> Thanks for watching."

---

## Phase 3: Visual Storyboard (Editing Guide)

| Time | Audio Segment | Visual on Screen |
|------|---------------|------------------|
| 0:00 | Intro / Problem | Option A: Stock footage of busy office<br>Option B: Manual Google search<br>Option C: Jump straight to demo |
| 0:15 | "I built the KYC Bot" | Title Card: **KYC Bot - Automated Compliance Agent**<br>Subtitle: Multi-Agent System for KYC |
| 0:20 | "Let's look at it in action" | **Screen Recording: demo.html**<br>Show the interface, enter "Grigor Dimitrov"<br>Text overlay: "Step 1: Enter Customer Name" |
| 0:25 | Click "Demo Mode" | **Screen Recording: Click "🎬 Demo Mode" button**<br>Show button click, logs start appearing immediately<br>Text overlay: "Multi-Agent System Starting" |
| 0:30 | "SearchAgent... Google API" | **Screen Recording: Terminal logs (left panel)**<br>Highlight: "SearchAgent: Querying Google Custom Search API..."<br>Zoom in on log messages, show timestamps<br>Text overlay: "SearchAgent Active" |
| 0:38 | "WatchlistAgent... Fuzzy Matching" | **Screen Recording: Terminal logs**<br>Highlight: "WatchlistAgent: Performing fuzzy matching check..."<br>Show: "✅ Scan Complete. 0 Matches found across 4 databases"<br>Text overlay: "WatchlistAgent Checking" |
| 0:48 | "AnalysisAgent... Gemini 2.0" | **Screen Recording: Terminal logs**<br>Highlight: "AnalysisAgent: Sending context to Gemini 2.0 Flash..."<br>Then show report panel (right side) appearing with animation<br>Text overlay: "Gemini 2.0 Generating Report" |
| 0:55 | "LangGraph... Architecture" | **Diagram: Architecture from README**<br>Zoom in on the 3 nodes (SearchAgent → WatchlistAgent → AnalysisAgent)<br>Highlight sequential flow |
| 1:05 | "Shared State" | **Code: graph.py**<br>Highlight: `AgentState` TypedDict definition<br>Show state fields (customer_name, search_results, etc.) |
| 1:15 | "Custom Tools" | **Code: tools.py**<br>Highlight: `check_watchlist` function<br>Show fuzzy matching logic with `SequenceMatcher` |
| 1:25 | "Gemini 2.0 Reasoning" | **Code: agents.py**<br>Highlight: `model.generate_content(prompt)`<br>Show Gemini 2.0 Flash model initialization |
| 1:35 | "The Result" | **Screen Recording: demo.html report panel (right side)**<br>Slowly scroll through the final report<br>Highlight: Risk Level badge (LOW - green badge)<br>Show: Executive Summary, Watchlist hits (all clean), Adverse media (tennis-related), Recommendations (APPROVE)<br>Text overlay: "Complete Risk Assessment in Seconds" |
| 1:50 | Conclusion | **Title Card: KYC Bot**<br>Show: GitHub: github.com/piepengu/kyc-agent-capstone<br>Deployed: https://kyc-bot-67jaheyovq-uc.a.run.app<br>Text: "Built with LangGraph & Gemini 2.0 Flash" |

---

## Phase 4: Recording Tips

### For demo.html Recording:

1. **Full Screen Mode**: 
   - Make browser full screen (F11)
   - Zoom browser to 125% for better visibility

2. **Key Moments to Capture**:
   - ✅ Interface loading (shows professional UI)
   - ✅ Entering customer name
   - ✅ Clicking "Run Real Investigation"
   - ✅ Logs streaming in real-time (this is the magic!)
   - ✅ Report appearing with risk level badge
   - ✅ Scroll through full report

3. **For Quick Demo**:
   - Use "Demo Mode" for fast, consistent results
   - Use "Run Real Investigation" for one real API call to show it's live

### For Code Shots:

1. **VS Code Setup**:
   - Use large font size (18-20pt)
   - Use dark theme for better contrast
   - Zoom in on specific code sections

2. **Highlighting**:
   - Use red box or highlighter effect in editor
   - Draw attention to specific lines you're discussing

### Audio Recording:

1. **Record voiceover first** (easier to match video to audio)
2. **Use quiet room** or phone voice recorder
3. **Speak clearly** at steady pace (~150 words/minute)

---

## Phase 5: Editing Workflow

### Recommended Tools:

- **Simple**: Loom (screen + cam), then trim
- **Better**: OBS Studio (screen recording) + CapCut (free) or DaVinci Resolve

### Editing Steps:

1. **Record all screen captures** (demo.html, code files, architecture)
2. **Record voiceover** separately
3. **Sync audio to video** in editor
4. **Add text overlays** for key moments:
   - "SearchAgent Active"
   - "WatchlistAgent Checking..."
   - "Gemini 2.0 Generating Report"
   - "Risk Level: LOW"
5. **Add transitions** between sections
6. **Export at 1080p** for best quality

---

## Quick Reference: What to Show

### Must Show (Rubric Points):

✅ **Concierge Agent**: KYC Bot automating compliance workflow  
✅ **Multi-Agent System**: Three agents (SearchAgent, WatchlistAgent, AnalysisAgent)  
✅ **Tools**: 
   - Built-in: Google Custom Search API, Gemini 2.0 Flash
   - Custom: `check_watchlist` with fuzzy matching  
✅ **LangGraph**: StateGraph orchestration  
✅ **Gemini**: AnalysisAgent using Gemini 2.0 Flash  
✅ **Sessions & Memory**: AgentState TypedDict  

### Visual Highlights:

- **demo.html interface** (shows professional UI)
- **Real-time agent logs** (shows multi-agent system working)
- **Risk assessment report** (shows output)
- **Code snippets** (shows implementation)
- **Architecture diagram** (shows design)

### Recommended Demo Names (Match Real API):

- **"Grigor Dimitrov"** → LOW risk (tennis player, clean)
- **"Shakira"** → MEDIUM risk (tax fraud mentions)
- **"Vladimir Petrov"** → HIGH risk (demo mode only, simulated)

### Recording Strategy:

1. **Main Demo**: Use "Demo Mode" with "Grigor Dimitrov" (fast, reliable, shows LOW risk)
2. **Optional**: Show one "Real Investigation" with "Shakira" (proves it's live, shows MEDIUM risk)
3. **Code Shots**: Pre-record, zoom in, highlight key lines
4. **Architecture**: Screenshot from README or recreate clean version

---

## Alternative: Quick 90-Second Version

If you need it shorter, cut the architecture deep-dive:

- [0:00-0:20] Problem & Solution
- [0:20-0:50] Demo (demo.html)
- [0:50-1:10] Quick code highlights (graph.py, tools.py)
- [1:10-1:30] Final report + conclusion

---

**Good luck with your video! The demo.html interface will make it look very professional! 🎬**

