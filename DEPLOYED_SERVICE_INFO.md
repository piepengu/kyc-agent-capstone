# Deployed Service Information

## Service URL

**Production Service:** https://kyc-bot-67jaheyovq-uc.a.run.app

## Available Endpoints

### 1. Health Check
```
GET https://kyc-bot-67jaheyovq-uc.a.run.app/health
```

**Response:**
```json
{
  "service": "KYC Bot",
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Run Investigation
```
POST https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate
Content-Type: application/json

{
  "customer_name": "John Doe"
}
```

**Response:**
```json
{
  "customer_name": "John Doe",
  "search_results": [...],
  "watchlist_results": {...},
  "final_report": "...",
  "risk_level": "LOW|MEDIUM|HIGH",
  "error": ""
}
```

### 3. Service Metrics
```
GET https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/metrics
```

**Response:**
```json
{
  "service": "KYC Bot",
  "version": "1.0.0",
  "status": "operational"
}
```

## Test the Service

### Using Browser
1. Health Check: https://kyc-bot-67jaheyovq-uc.a.run.app/health
2. Use the HTML test interface: `test_kyc_bot.html` (configured to use this URL)

### Using PowerShell
```powershell
# Health check
Invoke-WebRequest -Uri "https://kyc-bot-67jaheyovq-uc.a.run.app/health" -Method GET

# Run investigation
$body = @{customer_name="John Doe"} | ConvertTo-Json
Invoke-WebRequest -Uri "https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Using Python
```python
import requests

# Health check
response = requests.get("https://kyc-bot-67jaheyovq-uc.a.run.app/health")
print(response.json())

# Run investigation
response = requests.post(
    "https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate",
    json={"customer_name": "John Doe"}
)
print(response.json())
```

### Using cURL
```bash
# Health check
curl https://kyc-bot-67jaheyovq-uc.a.run.app/health

# Run investigation
curl -X POST https://kyc-bot-67jaheyovq-uc.a.run.app/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "John Doe"}'
```

## Deployment Details

- **Platform:** Google Cloud Run
- **Region:** us-central1
- **Project:** finsight-ai-jd
- **Service Name:** kyc-bot
- **Status:** Active and running
- **CORS:** Enabled (can be accessed from browsers)

## For Video Recording

When recording your video, you can:

1. **Show the Health Endpoint:**
   - Open: https://kyc-bot-67jaheyovq-uc.a.run.app/health
   - Shows JSON response: `{"status": "healthy", ...}`

2. **Show the Test Interface:**
   - Use the HTML test page (`test_kyc_bot.html`)
   - It's already configured to use this URL
   - Shows a nice UI for testing

3. **Show API in Action:**
   - Use browser console or Postman
   - Make a POST request to the investigate endpoint
   - Show the full response

## Quick Test

Open this URL in your browser to see it working:
**https://kyc-bot-67jaheyovq-uc.a.run.app/health**

