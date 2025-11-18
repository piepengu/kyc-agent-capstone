# How to Test the KYC Bot Agent

## Quick Test (Recommended)

Use the PowerShell script for the easiest testing experience:

```powershell
.\run_agent.ps1 -Name "Your Customer Name"
```

**Example:**
```powershell
.\run_agent.ps1 -Name "John Smith"
```

The script automatically:
- ✅ Loads environment variables from `.env`
- ✅ Activates the virtual environment
- ✅ Runs the agent with proper configuration

## Manual Testing

### Step 1: Open PowerShell

Navigate to the project directory:
```powershell
cd "C:\Users\piron\OneDrive\Documents\AI Agents"
```

### Step 2: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` appear at the beginning of your prompt.

### Step 3: Run the Agent

```powershell
python main.py --name "Your Customer Name"
```

**Examples:**
```powershell
# Test with a common name
python main.py --name "John Smith"

# Test with a less common name
python main.py --name "Grigor Dimitrov"

# Test with a suspicious name
python main.py --name "Pablo Escubar"
```

## What to Expect

### Successful Run Output

You should see:

1. **Initialization Messages:**
   ```
   [*] Starting KYC investigation for: Customer Name
   ============================================================
   [+] SearchAgent initialized with Google Custom Search
   [+] WatchlistAgent initialized with custom watchlist tool
   [+] AnalysisAgent initialized with Gemini 2.0 Flash
   ```

2. **SearchAgent Execution:**
   ```
   [*] SearchAgent: Searching for adverse media on 'Customer Name'...
      [*] Query: "Customer Name" fraud OR sanctions OR financial crime
      [+] Found 3 real search results
      ...
   ```

3. **WatchlistAgent Execution:**
   ```
   [*] WatchlistAgent: Checking 'Customer Name' against watchlists...
      [+] No matches found in 4 watchlists
   ```

4. **AnalysisAgent Execution:**
   ```
   [*] AnalysisAgent: Generating risk report for 'Customer Name'...
      [+] Report generated successfully (XXXX characters)
   ```

5. **Final Report:**
   ```
   ============================================================
   [+] KYC investigation complete!
   ============================================================
   
   [REPORT] FINAL RISK ASSESSMENT REPORT:
   ------------------------------------------------------------
   ## KYC Risk Assessment Report - Customer Name
   ...
   ```

6. **Performance Metrics:**
   ```
   [PERFORMANCE METRICS]
     Total Time: X.XXs
     SearchAgent: X.XXs avg
     WatchlistAgent: X.XXs avg
     AnalysisAgent: X.XXs avg
     Google Custom Search: X.XXs avg
     Gemini API: X.XXs avg
     Log file: logs/kyc_bot_YYYYMMDD.log
   ```

## Test Cases

### Test Case 1: Common Name (Low Risk)
```powershell
.\run_agent.ps1 -Name "John Smith"
```
**Expected**: LOW to MEDIUM risk, real search results, no watchlist matches

### Test Case 2: Professional Person (Low Risk)
```powershell
.\run_agent.ps1 -Name "Grigor Dimitrov"
```
**Expected**: LOW risk (tennis player), real search results about sports

### Test Case 3: Suspicious Name (Medium Risk)
```powershell
.\run_agent.ps1 -Name "Pablo Escubar"
```
**Expected**: MEDIUM risk, mentions of money laundering, Enhanced Due Diligence recommended

### Test Case 4: Generic Test
```powershell
.\run_agent.ps1 -Name "Test Customer"
```
**Expected**: Generic results, system functionality verification

## Checking Logs

After running, check the log file for detailed information:

```powershell
# View today's log file
Get-Content logs\kyc_bot_$(Get-Date -Format "yyyyMMdd").log | Select-Object -Last 50
```

Or open the log file directly:
```powershell
notepad logs\kyc_bot_20251118.log
```

## Troubleshooting

### Issue: "GOOGLE_API_KEY environment variable not set"

**Solution**: Use the PowerShell script which loads `.env` automatically:
```powershell
.\run_agent.ps1 -Name "Test Customer"
```

Or manually set environment variables:
```powershell
$env:GOOGLE_API_KEY="your_key_here"
python main.py --name "Test Customer"
```

### Issue: "ModuleNotFoundError"

**Solution**: Make sure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: API errors (403, rate limits)

**Solution**: 
- Some queries may fail with 403 errors (this is normal)
- System will fall back to simulated results
- Check API key restrictions in Google Cloud Console
- See [FIX_API_KEY_RESTRICTIONS.md](FIX_API_KEY_RESTRICTIONS.md) for details

## Performance Expectations

- **Total Execution Time**: 7-15 seconds
- **SearchAgent**: 1-3 seconds (3 queries)
- **WatchlistAgent**: < 0.1 seconds
- **AnalysisAgent**: 4-8 seconds (Gemini API call)
- **Search Results**: 3-9 results per investigation
- **Report Length**: 2500-4500 characters

## What Gets Logged

All executions are logged to:
- **Console**: Real-time feedback (INFO level)
- **Log File**: Detailed logs (DEBUG level) in `logs/kyc_bot_YYYYMMDD.log`

Logs include:
- Agent execution times
- API call details
- Search queries and results
- Error messages
- Performance metrics

## Next Steps After Testing

1. Review the generated risk report
2. Check the log file for detailed execution traces
3. Review performance metrics
4. Test with different customer names
5. Verify all agents are working correctly

For more detailed testing instructions, see [TESTING.md](TESTING.md).

