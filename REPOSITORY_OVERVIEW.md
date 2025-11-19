# Repository Overview

## 🎯 KYC Bot - Multi-Agent System for Automated KYC Compliance

This repository contains a production-ready multi-agent system for automated KYC (Know Your Customer) compliance checks.

## 📁 Repository Structure

### Core Application
- `main.py` - Entry point and workflow orchestration
- `agents.py` - Agent implementations (SearchAgent, WatchlistAgent, AnalysisAgent)
- `graph.py` - LangGraph workflow definition
- `tools.py` - Custom tools (watchlist checking, query formatting)
- `logger.py` - Structured logging and performance tracking
- `error_handling.py` - Error handling utilities
- `api.py` - Flask REST API server

### Tests
- `tests/` - Comprehensive test suite (63 tests, 81% coverage)
  - `test_agents.py` - Agent tests
  - `test_tools.py` - Tool tests
  - `test_error_handling.py` - Error handling tests
  - `test_integration.py` - Integration tests

### Configuration
- `requirements.txt` - Python dependencies
- `pytest.ini` - Test configuration
- `Dockerfile` - Docker image definition
- `cloudbuild.yaml` - Google Cloud Build configuration
- `.dockerignore` - Docker ignore patterns
- `.gitignore` - Git ignore patterns

### Documentation
- `Readme.md` - Main project documentation
- `PROJECT_DESCRIPTION.md` - Competition project description
- `DEPLOYMENT.md` - Deployment guide
- `DEPLOYED_SERVICE_INFO.md` - Deployed service information
- `DOCKER_SETUP.md` - Docker setup instructions
- `GCP_SETUP.md` - Google Cloud Platform setup
- `GOOGLE_SEARCH_SETUP.md` - Google Search API setup
- `LOGGING_GUIDE.md` - Logging system documentation
- `RISK_ASSESSMENT_GUIDE.md` - Risk assessment documentation
- `TEST_AGENT.md` - Testing guide
- `TEST_DEPLOYMENT.md` - Deployment testing guide
- `QUICK_DEPLOY.md` - Quick deployment reference
- `QUICK_START_GCP.md` - Quick GCP setup
- `USE_EXISTING_GCP_PROJECT.md` - Using existing GCP project
- `VIDEO_GUIDE.md` - Video creation guide
- `VIDEO_SCRIPT.md` - Video script
- `QUICK_VIDEO_RECORD.md` - Quick video recording guide
- `NEXT_STEPS.md` - Development roadmap
- `PROGRESS.md` - Development progress

### Scripts
- `deploy_to_cloud_run.ps1` - Automated deployment script
- `run_agent.ps1` - Local agent runner script
- `test_api.py` - API testing script

### Assets
- `kyc_bot_card.png` - Project card/thumbnail image
- `test_kyc_bot.html` - Browser-based test interface

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/piepengu/kyc-agent-capstone.git
   cd kyc-agent-capstone
   ```

2. **Set up environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   Create a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
   ```

4. **Run the agent:**
   ```bash
   python main.py --name "John Doe"
   ```
   Or use the PowerShell script:
   ```powershell
   .\run_agent.ps1 -Name "John Doe"
   ```

## 🌐 Deployed Service

**Service URL:** https://kyc-bot-67jaheyovq-uc.a.run.app

**Endpoints:**
- Health: `GET /health`
- Investigate: `POST /api/v1/investigate`
- Metrics: `GET /api/v1/metrics`

See `DEPLOYED_SERVICE_INFO.md` for details.

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

## 📊 Project Status

- ✅ Multi-agent system implemented
- ✅ Google Custom Search integration
- ✅ Watchlist checking with fuzzy matching
- ✅ Comprehensive logging and observability
- ✅ Error handling and validation
- ✅ Unit tests (63 tests, 81% coverage)
- ✅ Docker containerization
- ✅ Google Cloud Run deployment
- ✅ REST API with CORS support
- ✅ Complete documentation

## 🏗️ Architecture

The system uses a sequential multi-agent architecture:
1. **SearchAgent** - Searches for adverse media using Google Custom Search
2. **WatchlistAgent** - Checks against international sanctions lists
3. **AnalysisAgent** - Analyzes findings and generates risk assessment report

See `Readme.md` for detailed architecture documentation.

## 📝 Key Technologies

- **LangGraph** - Agent orchestration
- **Google Gemini 2.0 Flash** - AI analysis
- **Google Custom Search API** - Web search
- **Flask** - REST API
- **Docker** - Containerization
- **Google Cloud Run** - Deployment platform

## 📄 License

This project is part of the Kaggle Agents Intensive Capstone Project.

## 👤 Author

Dylan Zlatinski (piepengu)

## 🔗 Links

- **GitHub:** https://github.com/piepengu/kyc-agent-capstone
- **Deployed Service:** https://kyc-bot-67jaheyovq-uc.a.run.app
- **Competition:** https://www.kaggle.com/competitions/agents-intensive-capstone-project

