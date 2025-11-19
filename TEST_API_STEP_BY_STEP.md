# Step-by-Step API Testing Guide

## Method 1: Using PowerShell (Windows)

### Step 1: Open PowerShell
- Press `Windows Key + X`
- Select "Windows PowerShell" or "Terminal"

### Step 2: Test Health Endpoint
Copy and paste this command:

```powershell
Invoke-WebRequest -Uri "https://kyc-bot-67jaheyovq-uc.a.run.app/health" -Method GET | Select-Object -ExpandProperty Content
```

**Expected Result:**
```json
{"service":"KYC Bot","status":"healthy","version":"1.0.0"}
```

### Step 3: Test Investigation Endpoint
Copy and paste this command:

```powershell
$body = @{customer_name="Grigor Dimitrov"} | ConvertTo-Json
$response = Invoke-WebRequest -Uri "https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate" -Method POST -ContentType "application/json" -Body $body
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**What this does:**
- Creates a JSON body with the customer name
- Sends a POST request to the investigate endpoint
- Displays the formatted JSON response

**Expected Result:**
You should see a JSON response with:
- `customer_name`: "Grigor Dimitrov"
- `risk_level`: "LOW" (or "MEDIUM"/"HIGH")
- `search_results`: Array of search results
- `watchlist_results`: Watchlist check results
- `final_report`: Full risk assessment report

### Step 4: Test with Different Names
Change the customer name in the command:

```powershell
$body = @{customer_name="Shakira"} | ConvertTo-Json
$response = Invoke-WebRequest -Uri "https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate" -Method POST -ContentType "application/json" -Body $body
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## Method 2: Using Browser (Easiest)

### Step 1: Open Your HTML Test Page
1. Navigate to your project folder: `C:\Users\piron\OneDrive\Documents\AI Agents`
2. Double-click `test_kyc_bot.html` to open it in your browser

### Step 2: Test Health Endpoint
1. Click the **"Test Health Endpoint"** button
2. You should see: `{"service":"KYC Bot","status":"healthy","version":"1.0.0"}`

### Step 3: Test Investigation
1. Enter a customer name (e.g., "Grigor Dimitrov") in the text box
2. Click **"Run Investigation"** button
   - OR click **"Test: Grigor Dimitrov"** for a quick test
3. Wait 30-60 seconds for the investigation to complete
4. Review the results:
   - Customer name
   - **Risk Level** (should be LOW, MEDIUM, or HIGH - not UNKNOWN)
   - Search results count
   - Watchlist matches
   - Full report

---

## Method 3: Using Browser Developer Console

### Step 1: Open Browser Developer Tools
1. Open your browser (Chrome, Edge, Firefox)
2. Press `F12` to open Developer Tools
3. Click the **"Console"** tab

### Step 2: Test Health Endpoint
Copy and paste this JavaScript:

```javascript
fetch('https://kyc-bot-67jaheyovq-uc.a.run.app/health')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

**Expected Result:**
```json
{service: "KYC Bot", status: "healthy", version: "1.0.0"}
```

### Step 3: Test Investigation Endpoint
Copy and paste this JavaScript:

```javascript
fetch('https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ customer_name: 'Grigor Dimitrov' })
})
  .then(response => response.json())
  .then(data => {
    console.log('Risk Level:', data.risk_level);
    console.log('Full Response:', data);
  })
  .catch(error => console.error('Error:', error));
```

**Expected Result:**
You'll see in the console:
- `Risk Level: LOW` (or MEDIUM/HIGH)
- Full response object with all details

---

## Method 4: Using cURL (If Installed)

### Step 1: Test Health
```bash
curl https://kyc-bot-67jaheyovq-uc.a.run.app/health
```

### Step 2: Test Investigation
```bash
curl -X POST https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d "{\"customer_name\": \"Grigor Dimitrov\"}"
```

---

## Quick Test Checklist

- [ ] Health endpoint returns `{"status":"healthy"}`
- [ ] Investigation endpoint accepts POST requests
- [ ] Risk level is extracted correctly (LOW/MEDIUM/HIGH, not UNKNOWN)
- [ ] Search results are returned
- [ ] Watchlist results are returned
- [ ] Full report is generated

## Troubleshooting

### If you get "Failed to fetch" or CORS error:
- Make sure you're using the correct URL: `https://kyc-bot-67jaheyovq-uc.a.run.app`
- The service has CORS enabled, so this shouldn't happen

### If risk_level shows "UNKNOWN":
- Check the `final_report` field in the response
- Look for "Risk Level:" in the report text
- The improved extraction should handle most formats now

### If the request times out:
- Investigations take 30-60 seconds
- Make sure you wait for the full response
- Check your internet connection

---

## Recommended: Use the HTML Test Page

The easiest way is to use `test_kyc_bot.html`:
1. Double-click the file to open in browser
2. Click the test buttons
3. See formatted results instantly

No command line needed! 🎉

