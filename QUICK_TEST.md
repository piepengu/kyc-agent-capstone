# Quick Test Guide - KYC Bot

## How to Test the Agent

### 🚀 Easy Method: Use the PowerShell Script (Recommended)

Simply run:
```powershell
.\run_agent.ps1 -Name "Grigor Dimitrov"
```

Or with any customer name:
```powershell
.\run_agent.ps1 -Name "Your Customer Name"
```

The script automatically:
- ✅ Loads environment variables from `.env` file
- ✅ Activates the virtual environment
- ✅ Runs the agent with proper configuration

### Manual Method: Step by Step

#### Step 1: Open PowerShell

Open PowerShell in the project directory:
```powershell
cd "C:\Users\piron\OneDrive\Documents\AI Agents"
```

#### Step 2: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear at the beginning of your prompt.

#### Step 3: Run the Agent

Test with any customer name:
```powershell
python main.py --name "Jane Doe"
```

Or test with a different name:
```powershell
python main.py --name "John Smith"
```

### Step 4: What to Look For

✅ **Success indicators:**
- `[+] SearchAgent initialized with Google Custom Search`
- `[+] Found X real search results` (at least some queries should succeed)
- `[+] WatchlistAgent initialized`
- `[+] AnalysisAgent initialized with Gemini 2.0 Flash`
- `[+] KYC investigation complete!`
- A detailed risk report at the end

⚠️ **Expected behavior:**
- Some queries may show `[!] Search API error` - this is normal (rate limiting or API restrictions)
- The system will fall back to simulated results for failed queries
- You should still get real results from at least 1-2 queries

### Example Output

```
[*] Starting KYC investigation for: Jane Doe
============================================================

[+] SearchAgent initialized with Google Custom Search (CX: 322c853672...)
[+] WatchlistAgent initialized with custom watchlist tool
[+] AnalysisAgent initialized with Gemini 2.0 Flash
[*] SearchAgent: Searching for adverse media on 'Jane Doe'...
   [*] Query: "Jane Doe" fraud OR sanctions OR financial crime
   [+] Found 3 real search results
   [*] Query: "Jane Doe" fraud OR scam OR embezzlement
   [+] Found 3 real search results
   [*] Query: "Jane Doe" sanctions OR OFAC OR blacklist
   [+] Found 3 real search results
   [+] Found 7 search results
[*] WatchlistAgent: Checking 'Jane Doe' against watchlists...
   [+] No matches found in 4 watchlists
[*] AnalysisAgent: Generating risk report for 'Jane Doe'...
   [+] Report generated successfully (4090 characters)

============================================================
[+] KYC investigation complete!
============================================================

[REPORT] FINAL RISK ASSESSMENT REPORT:
------------------------------------------------------------
## KYC Risk Assessment Report: Jane Doe
...
```

## Troubleshooting

### If you get "GOOGLE_API_KEY environment variable not set"
- Make sure your `.env` file exists in the project root
- Check that it contains: `GOOGLE_API_KEY=your_key_here`
- Make sure you're in the project directory when running

### If you get "ModuleNotFoundError"
- Make sure the virtual environment is activated
- Run: `pip install -r requirements.txt`

### If all queries fail with 403 errors
- Check that Custom Search API is enabled in Google Cloud Console
- Verify API key restrictions allow Custom Search API
- See [FIX_API_KEY_RESTRICTIONS.md](FIX_API_KEY_RESTRICTIONS.md) for details

## Quick One-Liner Test

**Easiest way (recommended):**
```powershell
.\run_agent.ps1 -Name "Test Customer"
```

**Or manually:**
```powershell
.\venv\Scripts\Activate.ps1; python main.py --name "Test Customer"
```

## Test Different Scenarios

Try different customer names to see how the agent handles various cases:
```powershell
# Common name
python main.py --name "John Smith"

# Less common name
python main.py --name "Vladimir Petrov"

# Company name
python main.py --name "Acme Corporation"
```

