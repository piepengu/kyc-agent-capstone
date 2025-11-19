# Deploy KYC Bot to Cloud Run - Right Now! 🚀

## Quick Commands (Copy & Paste)

### Option 1: Automated Script (Easiest)

In PowerShell, from your project directory:

```powershell
cd "C:\Users\piron\OneDrive\Documents\AI Agents"
.\deploy_to_cloud_run.ps1
```

This script will:
- ✅ Read API keys from `.env`
- ✅ Build and push Docker image
- ✅ Deploy to Cloud Run
- ✅ Show you the service URL

### Option 2: Manual Commands (Step by Step)

In Command Prompt (where you ran gcloud init):

```cmd
REM Navigate to project
cd "C:\Users\piron\OneDrive\Documents\AI Agents"

REM Step 1: Build and push (takes 5-10 minutes)
gcloud builds submit --tag gcr.io/finsight-ai-jd/kyc-bot:latest

REM Step 2: Deploy (replace YOUR_KEY and YOUR_ID with values from .env)
gcloud run deploy kyc-bot ^
    --image gcr.io/finsight-ai-jd/kyc-bot:latest ^
    --platform managed ^
    --region us-central1 ^
    --allow-unauthenticated ^
    --set-env-vars GOOGLE_API_KEY=YOUR_KEY,GOOGLE_SEARCH_ENGINE_ID=YOUR_ID ^
    --memory 1Gi ^
    --cpu 1 ^
    --timeout 300

REM Step 3: Get service URL
gcloud run services describe kyc-bot --platform managed --region us-central1 --format "value(status.url)"
```

## Before You Deploy

1. **Verify billing** (if not already done):
   ```cmd
   gcloud billing projects describe finsight-ai-jd
   ```

2. **Check .env file** (already verified ✅)

## After Deployment

Test your service:
```powershell
# Get the URL from deployment output, then:
$url = "https://your-service-url.run.app"
Invoke-WebRequest -Uri "$url/health" -Method GET
```

## Need Help?

- See `QUICK_DEPLOY.md` for detailed instructions
- See `DEPLOYMENT.md` for comprehensive guide
- Check logs: `gcloud run services logs read kyc-bot --region us-central1`

