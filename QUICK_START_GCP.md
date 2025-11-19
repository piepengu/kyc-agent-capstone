# Quick Start: GCP Setup (5 Minutes)

Fastest way to get your GCP project ready for deployment.

## Prerequisites Checklist

- [ ] Google account (Gmail works)
- [ ] Credit card for billing (won't be charged for free tier)
- [ ] 5-10 minutes

## Step 1: Create Project (2 minutes)

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: `kyc-bot`
4. Click "Create"
5. Select your new project

## Step 2: Enable APIs (1 minute)

Run these commands in PowerShell (after installing gcloud):

```powershell
# Install gcloud first (if not installed)
# Download from: https://cloud.google.com/sdk/docs/install

# Initialize (first time only)
gcloud init

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

Or enable via Console:
- Go to: https://console.cloud.google.com/apis/library
- Search and enable: "Cloud Run API", "Cloud Build API", "Artifact Registry API"

## Step 3: Set Up Billing (1 minute)

1. Go to: https://console.cloud.google.com/billing
2. Create billing account (if needed)
3. Link to your project
4. **Note:** $300 free credit for new accounts!

## Step 4: Verify (1 minute)

```powershell
# Check project
gcloud config get-value project

# Check APIs
gcloud services list --enabled | Select-String "run|build|artifact"

# Test authentication
gcloud auth list
```

## Step 5: Deploy! (See DEPLOYMENT.md)

```powershell
# Set variables
$PROJECT_ID = "your-project-id"
$REGION = "us-central1"

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/kyc-bot:latest
gcloud run deploy kyc-bot --image gcr.io/$PROJECT_ID/kyc-bot:latest --region $REGION
```

## That's It!

Your GCP project is ready. See `DEPLOYMENT.md` for full deployment instructions.

## Need Help?

- Full guide: See `GCP_SETUP.md`
- Troubleshooting: See `GCP_SETUP.md` → Troubleshooting section
- GCP Console: https://console.cloud.google.com/

