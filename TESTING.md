# Testing the KYC Bot Agent

## Prerequisites

1. **Python 3.9+** (You have Python 3.13.5 installed ✅)
2. **Virtual Environment** (Already created in `venv/` ✅)
3. **Dependencies Installed** (Already installed ✅)
4. **API Key** (Configured in `.env` file ✅)

## Quick Start Testing

### Step 1: Activate the Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Git Bash (if using):**
```bash
source venv/Scripts/activate
```

### Step 2: Verify Environment Setup

Check that the API key is loaded:
```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'Loaded' if os.getenv('GOOGLE_API_KEY') else 'NOT Loaded')"
```

### Step 3: Run the Agent

**Basic test with a sample customer name:**
```powershell
python main.py --name "John Doe"
```

**Test with a different name:**
```powershell
python main.py --name "Jane Smith"
```

**Test with a more specific name:**
```powershell
python main.py --name "Robert Johnson"
```

## Expected Output

When you run the agent, you should see:

1. **Initialization messages:**
   - `[*] Starting KYC investigation for: [Customer Name]`
   - `[+] SearchAgent initialized`
   - `[+] WatchlistAgent initialized with custom watchlist tool`
   - `[+] AnalysisAgent initialized with Gemini 2.0 Flash`

2. **Search Agent execution:**
   - `[*] SearchAgent: Searching for adverse media on '[Customer Name]'...`
   - `[*] Query: "[Customer Name]" fraud OR sanctions OR financial crime`
   - `[+] Found X search results`

3. **Watchlist Agent execution:**
   - `[*] WatchlistAgent: Checking '[Customer Name]' against watchlists...`
   - `[+] No matches found in 4 watchlists` (or warning if match found)

4. **Analysis Agent execution:**
   - `[*] AnalysisAgent: Generating risk report for '[Customer Name]'...`
   - `[+] Report generated successfully (XXXX characters)`

5. **Final Report:**
   - Complete risk assessment report with:
     - Executive Summary
     - Risk Level (LOW/MEDIUM/HIGH)
     - Key Findings
     - Watchlist Check Summary
     - Recommendations
     - Overall Assessment

6. **Summary Statistics:**
   - Number of search results found
   - Number of watchlists checked
   - Number of watchlist matches

## Example Test Cases

### Test Case 1: Standard Customer
```powershell
python main.py --name "John Doe"
```
**Expected:** Low to Medium risk, no watchlist matches

### Test Case 2: Common Name
```powershell
python main.py --name "Michael Johnson"
```
**Expected:** Similar results, may have more search results due to common name

### Test Case 3: Unique Name
```powershell
python main.py --name "Xavier Montague"
```
**Expected:** Fewer search results, clearer risk assessment

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable not set"

**Solution 1:** Make sure `.env` file exists in the project root:
```powershell
Get-Content .env
```

**Solution 2:** Manually set the environment variable:
```powershell
$env:GOOGLE_API_KEY="AIzaSyAR0cUEIWvD1f6UIHC0zCPz9YoUg-VQaKI"
python main.py --name "John Doe"
```

**Solution 3:** Check file encoding (should be UTF-8):
```powershell
[System.IO.File]::ReadAllText("$PWD\.env", [System.Text.Encoding]::UTF8)
```

### Issue: "ModuleNotFoundError: No module named 'langgraph'"

**Solution:** Reinstall dependencies:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: "Python version too old"

**Solution:** Make sure you're using Python 3.9+:
```powershell
python --version
# Should show Python 3.9 or higher
```

If not, activate the virtual environment which has Python 3.13.5:
```powershell
.\venv\Scripts\Activate.ps1
python --version
```

### Issue: Gemini API errors

**Solution:** Check your API key is valid and has access to Gemini models:
```powershell
python -c "import google.generativeai as genai; genai.configure(api_key='AIzaSyAR0cUEIWvD1f6UIHC0zCPz9YoUg-VQaKI'); print([m.name for m in genai.list_models()][:5])"
```

## Advanced Testing

### Test with Verbose Output

You can modify `main.py` to add more detailed logging, or check the console output for each agent's progress.

### Test Different Scenarios

1. **Test with empty name:**
   ```powershell
   python main.py --name ""
   ```
   (Should show error or handle gracefully)

2. **Test with special characters:**
   ```powershell
   python main.py --name "O'Brien"
   ```
   (Should handle special characters correctly)

3. **Test with very long name:**
   ```powershell
   python main.py --name "Dr. John Michael Robert Smith-Jones III"
   ```
   (Should handle long names correctly)

## Performance Testing

The agent should complete a full investigation in approximately:
- **Search Agent:** 1-2 seconds (simulated)
- **Watchlist Agent:** < 1 second
- **Analysis Agent:** 3-10 seconds (depends on Gemini API response time)
- **Total:** ~5-15 seconds per investigation

## Next Steps

Once testing is successful, you can:
1. Integrate real Google Search API (requires Search Engine ID)
2. Enhance watchlist data with realistic examples
3. Add more sophisticated error handling
4. Implement logging to files
5. Add unit tests

## Support

If you encounter any issues:
1. Check the error message carefully
2. Verify all prerequisites are met
3. Ensure the virtual environment is activated
4. Check that the `.env` file is in the correct location
5. Verify your API key is valid

