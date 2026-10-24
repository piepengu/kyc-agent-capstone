# KYC Bot

**Live demo:** [https://piepengu.github.io/kyc-agent-capstone/](https://piepengu.github.io/kyc-agent-capstone/)

Multi-agent **Know Your Customer** workflow that turns a customer name into an auditable risk report: adverse-media search → sanctions screening → Gemini analysis.

Built for the [Kaggle Agents Intensive](https://www.kaggle.com/) Capstone (Concierge Agents track, Nov 2025).

## Why it exists

Manual KYC investigation is slow and error-prone. KYC Bot acts as a junior analyst: it gathers evidence, screens watchlists, and drafts a structured LOW / MEDIUM / HIGH risk report for a human reviewer.

## Architecture

```
Customer name
      │
      ▼
┌─────────────────┐
│  SearchAgent    │  Google Custom Search — adverse media queries
└────────┬────────┘
         ▼
┌─────────────────┐
│ WatchlistAgent  │  Fuzzy match vs OFAC / UN / EU / UK lists
└────────┬────────┘
         ▼
┌─────────────────┐
│ AnalysisAgent   │  Gemini 2.0 Flash — risk report
└────────┬────────┘
         ▼
   Structured report
```

Orchestration is a **LangGraph** sequential `StateGraph` with a typed `AgentState` (`customer_name`, `search_results`, `watchlist_results`, `final_report`, `error`). Agents communicate only through shared state — see `graph.py`, `agents.py`, `tools.py`.

## Tech stack

| Layer | Tools |
|-------|--------|
| Orchestration | Python 3.11+, LangGraph, LangChain |
| LLM | Google Gemini (`langchain-google-genai`) |
| Search | Google Custom Search API |
| API (optional) | Flask + Gunicorn (Cloud Run) |
| Reliability | pytest (63 tests, ~81% coverage), structured logging, retries / validation |

## Quickstart

```bash
git clone https://github.com/piepengu/kyc-agent-capstone.git
cd kyc-agent-capstone
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in API keys
```

**.env keys** (never commit real values):

- `GOOGLE_API_KEY` — Gemini / Google AI
- `GOOGLE_SEARCH_ENGINE_ID` — Custom Search engine ID

```bash
python main.py --name "Jane Doe"
pytest -q
```

Optional API server: `python api.py` → `POST /api/v1/investigate`.

Browser demo: [https://piepengu.github.io/kyc-agent-capstone/](https://piepengu.github.io/kyc-agent-capstone/). Use **Demo Mode** for the walkthrough. **Run Real Investigation** calls the deployed API at `https://kyc-bot-67jaheyovq-uc.a.run.app` — see `DEPLOYMENT.md`.

## Engineering notes

- **Typed state** via `AgentState` TypedDict for predictable agent handoffs
- **Fuzzy sanctions matching** with aliases (see `tools.py` + tests)
- **Error handling** for bad names, API failures, and partial results
- Capstone write-up: [`PROJECT_DESCRIPTION.md`](./PROJECT_DESCRIPTION.md)

## License

MIT — see [LICENSE](./LICENSE).
