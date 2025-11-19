# Project Video Creation Guide

Complete guide for creating a compelling 2-minute demo video for the KYC Bot project.

## Video Requirements

- **Length:** ~2 minutes (120 seconds)
- **Format:** MP4, MOV, or similar
- **Purpose:** Demonstrate the agent in action and showcase key features
- **Audience:** Competition judges and potential users

## Video Structure (2 Minutes)

### **Opening (0:00 - 0:15)** - 15 seconds
**Hook & Problem Statement**

- Quick intro: "Meet KYC Bot - an AI-powered multi-agent system that automates KYC compliance"
- Show the problem: "Manual KYC checks take hours. KYC Bot does it in minutes."
- Visual: Project card image or title screen

**Script Ideas:**
- "What if you could automate 90% of KYC compliance work? That's what KYC Bot does."
- "KYC compliance is slow, manual, and error-prone. We built an AI agent to fix that."

### **Demo - Part 1: Running an Investigation (0:15 - 0:50)** - 35 seconds
**Show the Agent in Action**

**Option A: Browser Demo (Recommended)**
- Open the HTML test interface
- Enter a customer name (e.g., "Grigor Dimitrov")
- Click "Run Investigation"
- Show the investigation running (loading state)
- Display the results when complete

**Option B: Command Line Demo**
- Show terminal/command prompt
- Run: `python main.py --name "Grigor Dimitrov"`
- Show the workflow executing
- Display the final report

**What to Highlight:**
- The three-agent workflow (Search → Watchlist → Analysis)
- Real-time search results
- Watchlist matching with similarity scores
- AI-generated risk assessment report

**Script Ideas:**
- "Let's investigate a customer. KYC Bot uses three specialized agents..."
- "First, the SearchAgent finds adverse media using Google Custom Search..."
- "Then, the WatchlistAgent checks sanctions lists with fuzzy matching..."
- "Finally, the AnalysisAgent uses Gemini AI to generate a comprehensive risk report..."

### **Demo - Part 2: Key Features (0:50 - 1:30)** - 40 seconds
**Showcase Technical Features**

**Feature 1: Multi-Agent Architecture (10 seconds)**
- Show code or diagram of the LangGraph workflow
- Highlight: "Three specialized agents working in sequence"
- Visual: Architecture diagram or code snippet

**Feature 2: Real Search Results (10 seconds)**
- Show actual Google Custom Search results
- Highlight: "Real-time adverse media search"
- Visual: Search results or API response

**Feature 3: Watchlist Matching (10 seconds)**
- Show watchlist match with similarity score
- Highlight: "Fuzzy matching catches name variations"
- Visual: Match result showing similarity percentage

**Feature 4: AI-Powered Analysis (10 seconds)**
- Show the generated report
- Highlight: "Gemini AI analyzes all findings and generates a structured report"
- Visual: Report output or risk level

**Script Ideas:**
- "KYC Bot uses LangGraph to orchestrate three specialized agents..."
- "Real-time Google Custom Search finds adverse media..."
- "Fuzzy matching catches name variations and aliases..."
- "Gemini AI synthesizes everything into a comprehensive risk assessment..."

### **Demo - Part 3: Deployed Service (1:30 - 1:50)** - 20 seconds
**Show Production Deployment**

- Open the deployed Cloud Run service URL
- Show the API endpoints working
- Quick demo of the REST API
- Highlight: "Deployed and ready for production use"

**Script Ideas:**
- "KYC Bot is deployed on Google Cloud Run and accessible via REST API..."
- "You can integrate it into any system..."

### **Closing (1:50 - 2:00)** - 10 seconds
**Call to Action & Summary**

- Show project card/thumbnail
- Quick summary: "Automated KYC compliance in minutes, not hours"
- GitHub link or project URL
- Thank you message

**Script Ideas:**
- "KYC Bot: Automated KYC compliance in minutes, not hours. Check it out on GitHub."
- "From hours of manual work to minutes of automated analysis. That's KYC Bot."

## Recording Tools & Software

### **Screen Recording Software**

**Free Options:**
1. **OBS Studio** (Recommended)
   - Free, open-source
   - High-quality recording
   - Can record screen + webcam
   - Download: https://obsproject.com/

2. **Windows Game Bar** (Built-in Windows)
   - Press `Win + G` to open
   - Click record button
   - Simple and built-in

3. **ShareX** (Windows)
   - Free, open-source
   - Screen recording + editing
   - Download: https://getsharex.com/

4. **Loom** (Free tier available)
   - Easy to use
   - Built-in editing
   - Can share directly
   - Download: https://www.loom.com/

**Paid Options:**
- **Camtasia** - Professional editing
- **ScreenFlow** (Mac) - Professional editing
- **Adobe Premiere** - Full video editing suite

### **Video Editing Software**

**Free Options:**
1. **DaVinci Resolve** (Recommended)
   - Professional-grade editing
   - Free version available
   - Download: https://www.blackmagicdesign.com/products/davinciresolve

2. **OpenShot**
   - Simple, free editor
   - Good for beginners
   - Download: https://www.openshot.org/

3. **Windows Video Editor** (Built-in)
   - Simple editing
   - Built into Windows 10/11

**Online Editors:**
- **Canva** - Simple online editor
- **Kapwing** - Browser-based editor
- **Clipchamp** - Microsoft's online editor

## Recording Tips

### **Before Recording**

1. **Prepare Your Environment:**
   - Close unnecessary applications
   - Clean up your desktop
   - Set browser to full-screen or clean window
   - Have test data ready (customer names to test)

2. **Test Everything:**
   - Make sure the service is running
   - Test the investigation with a known customer
   - Verify all endpoints work
   - Check audio levels if narrating

3. **Prepare Script:**
   - Write a rough script (see below)
   - Practice the flow
   - Time yourself (aim for 2 minutes)

### **During Recording**

1. **Screen Recording:**
   - Record at 1080p (1920x1080) minimum
   - 30 FPS is fine (60 FPS if possible)
   - Record in a quiet environment
   - Use a good microphone if narrating

2. **Pacing:**
   - Don't rush - speak clearly
   - Pause between sections
   - Show key moments clearly
   - Let animations/loading complete

3. **Visuals:**
   - Use zoom/pan to highlight important parts
   - Show code snippets clearly
   - Display results prominently
   - Use cursor to guide attention

### **After Recording**

1. **Editing:**
   - Trim unnecessary parts
   - Add transitions between sections
   - Add text overlays for key points
   - Add background music (optional, keep it subtle)
   - Add captions/subtitles (recommended)

2. **Export:**
   - Export as MP4 (H.264 codec)
   - 1080p resolution
   - Keep file size reasonable (< 100MB if possible)

## Sample Script (2 Minutes)

### **Full Script Example:**

```
[0:00-0:15] Opening
"KYC compliance is a critical but time-consuming process. 
Compliance officers spend hours manually searching for adverse media 
and checking watchlists. What if we could automate 90% of this work? 
That's what KYC Bot does - an AI-powered multi-agent system that 
transforms hours of manual work into minutes of automated analysis."

[0:15-0:30] Demo Start
"Let me show you how it works. I'll investigate a customer named 
Grigor Dimitrov. KYC Bot uses three specialized AI agents working 
in sequence. First, the SearchAgent searches for adverse media..."

[0:30-0:45] Show Results
"As you can see, it found several search results. Next, the 
WatchlistAgent checks against international sanctions lists using 
fuzzy matching to catch name variations..."

[0:45-1:00] Show Report
"Finally, the AnalysisAgent uses Gemini AI to analyze all findings 
and generate a comprehensive risk assessment report. Here's the 
complete report with risk level, key findings, and recommendations."

[1:00-1:15] Technical Features
"KYC Bot is built with LangGraph for agent orchestration, integrates 
real Google Custom Search results, uses fuzzy matching for watchlist 
screening, and leverages Gemini AI for intelligent analysis."

[1:15-1:30] Deployment
"The system is deployed on Google Cloud Run and accessible via REST API. 
You can integrate it into any system or use our web interface."

[1:30-1:45] Show API
"Here's the deployed service. You can call the API with any customer 
name and get a complete risk assessment in minutes."

[1:45-2:00] Closing
"KYC Bot: Automated KYC compliance in minutes, not hours. 
Check out the code on GitHub and try it yourself. Thank you!"
```

## Visual Ideas

### **Screen Layout Options**

**Option 1: Split Screen**
- Left: Code/Architecture diagram
- Right: Running demo
- Good for showing technical details

**Option 2: Full Screen Demo**
- Show the actual application running
- Zoom in on important parts
- Good for showing user experience

**Option 3: Picture-in-Picture**
- Main: Application demo
- Small corner: Webcam (optional)
- Good for personal touch

### **Visual Elements to Include**

1. **Title Card** (5 seconds)
   - Project name: "KYC Bot"
   - Tagline: "Automated KYC Compliance"
   - Your name/GitHub

2. **Architecture Diagram**
   - Show the three-agent workflow
   - Highlight LangGraph orchestration
   - Can use ASCII art or create a simple diagram

3. **Code Snippets**
   - Show key code (agents.py, graph.py)
   - Highlight important parts
   - Keep it brief and readable

4. **Live Demo**
   - Show the investigation running
   - Display results clearly
   - Highlight key outputs

5. **Closing Card**
   - GitHub link
   - Service URL
   - Thank you message

## Step-by-Step Recording Plan

### **Step 1: Prepare (15 minutes)**
1. Open your test interface or terminal
2. Have test customer names ready
3. Make sure service is running
4. Clean up your screen
5. Write a rough script

### **Step 2: Record (30 minutes)**
1. Record the full demo (may take 2-3 takes)
2. Record each section separately if needed
3. Get multiple takes of key moments
4. Record at least 3-5 minutes of footage (you'll edit down)

### **Step 3: Edit (1-2 hours)**
1. Import footage into editor
2. Trim to 2 minutes
3. Add transitions
4. Add text overlays for key points
5. Add background music (optional)
6. Add captions (recommended)
7. Export final video

### **Step 4: Review & Upload**
1. Watch the final video
2. Check audio levels
3. Verify all text is readable
4. Upload to YouTube/Vimeo
5. Add to your project submission

## Quick Recording Checklist

- [ ] Screen recording software installed
- [ ] Test environment ready
- [ ] Service deployed and working
- [ ] Test customer names prepared
- [ ] Script written (rough outline)
- [ ] Desktop cleaned up
- [ ] Audio tested (if narrating)
- [ ] Recording settings configured (1080p, 30fps)
- [ ] Multiple takes recorded
- [ ] Video edited and trimmed
- [ ] Text overlays added
- [ ] Final video exported
- [ ] Video uploaded/shared

## Alternative: No-Narration Video

If you prefer not to narrate:

1. **Use Text Overlays:**
   - Add text explaining each step
   - Use clear, readable fonts
   - Keep text brief

2. **Use Background Music:**
   - Choose subtle, professional music
   - Keep volume low
   - No lyrics (instrumental)

3. **Show Key Moments:**
   - Highlight important parts with zoom
   - Use arrows/annotations
   - Show results clearly

## Example Video Structure (No Narration)

```
[0:00-0:10] Title card with project name
[0:10-0:20] Text: "Automated KYC Compliance in Minutes"
[0:20-0:40] Show investigation running (with text overlays)
[0:40-1:00] Show search results (highlight key findings)
[1:00-1:20] Show watchlist matching (show similarity scores)
[1:20-1:40] Show final report (highlight risk level)
[1:40-1:50] Show deployed service URL
[1:50-2:00] Closing card with GitHub link
```

## Resources

- **OBS Studio:** https://obsproject.com/
- **DaVinci Resolve:** https://www.blackmagicdesign.com/products/davinciresolve
- **Free Music:** https://www.bensound.com/ (royalty-free)
- **Free Images:** https://unsplash.com/
- **Video Hosting:** YouTube (unlisted), Vimeo, or Google Drive

## Tips for Success

1. **Keep it Simple:** Don't try to show everything - focus on key features
2. **Show, Don't Tell:** Let the demo speak for itself
3. **Be Clear:** Speak clearly or use clear text overlays
4. **Practice:** Record multiple takes and pick the best
5. **Edit Well:** Trim unnecessary parts, add smooth transitions
6. **Test First:** Make sure everything works before recording
7. **Time It:** Aim for exactly 2 minutes (can be 1:50-2:10)

## Next Steps

1. Choose your recording tool (OBS Studio recommended)
2. Write a rough script
3. Practice the demo flow
4. Record multiple takes
5. Edit down to 2 minutes
6. Add polish (transitions, text, music)
7. Export and upload

Good luck with your video! 🎥

