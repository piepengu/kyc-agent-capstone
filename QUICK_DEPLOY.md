# Quick Deploy to Cloud Run

Step-by-step guide to deploy KYC Bot to Google Cloud Run.

## Prerequisites Checklist

- [x] GCP project set: `finsight-ai-jd`
- [x] APIs enabled: Cloud Run, Cloud Build, Artifact Registry
- [ ] Billing enabled (verify)
- [ ] `.env` file with API keys
- [ ] In project directory

## Step 1: Verify Billing

```cmd
gcloud billing projects describe finsight-ai-jd
```

If billing is not enabled, enable it:
- Go to: https://console.cloud.google.com/billing?project=finsight-ai-jd
- Link a billing account

## Step 2: Verify .env File

Make sure you have `.env` file in the project directory with:
```
GOOGLE_API_KEY=your_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
```

## Step 3: Build and Push Image

```cmd
cd "C:\Users\piron\OneDrive\Documents\AI Agents"

gcloud builds submit --tag gcr.io/finsight-ai-jd/kyc-bot:latest
```

**Note:** This will take 5-10 minutes the first time.

## Step 4: Deploy to Cloud Run

```cmd
gcloud run deploy kyc-bot ^
    --image gcr.io/finsight-ai-jd/kyc-bot:latest ^
    --platform managed ^
    --region us-central1 ^
    --allow-unauthenticated ^
    --set-env-vars GOOGLE_API_KEY=your_key,GOOGLE_SEARCH_ENGINE_ID=your_id ^
    --memory 1Gi ^
    --cpu 1 ^
    --timeout 300
```

**Important:** Replace `your_key` and `your_id` with actual values from your `.env` file.

## Step 5: Get Service URL

After deployment, get your service URL:

```cmd
gcloud run services describe kyc-bot --platform managed --region us-central1 --format "value(status.url)"
```

## Step 6: Test the Deployment

Test the health endpoint:
```cmd
curl https://your-service-url.run.app/health
```

Or use PowerShell:
```powershell
Invoke-WebRequest -Uri "https://your-service-url.run.app/health" -Method GET
```

## Using the PowerShell Script (Easier)

If you prefer, use the automated script:

```powershell
cd "C:\Users\piron\OneDrive\Documents\AI Agents"
.\deploy_to_cloud_run.ps1
```

This script will:
1. Read API keys from `.env` file
2. Build and push the image
3. Deploy to Cloud Run
4. Show you the service URL

## Troubleshooting

### "Billing account not found"
- Enable billing: https://console.cloud.google.com/billing?project=finsight-ai-jd

### "Permission denied"
- Make sure you have Editor or Owner role on the project

### "API not enabled"
- Run: `gcloud services enable run.googleapis.com cloudbuild.googleapis.com`

### Build fails
- Check Dockerfile is correct
- Verify all files are in the directory
- Check `.dockerignore` isn't excluding needed files

## Next Steps

After successful deployment:
1. Test the API endpoints
2. Set up monitoring (optional)
3. Configure custom domain (optional)
4. Set up CI/CD (optional)

See `DEPLOYMENT.md` for more details.

