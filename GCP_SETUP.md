# Google Cloud Platform (GCP) Setup Guide

Complete step-by-step guide to set up a GCP project for deploying KYC Bot to Cloud Run.

## Prerequisites

- Google account (Gmail account works)
- Credit card (for billing, but free tier available)
- Basic understanding of cloud services

## Step 1: Create Google Cloud Account

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/

2. **Sign in with your Google account:**
   - Use your Gmail account or Google Workspace account

3. **Accept Terms of Service:**
   - Read and accept Google Cloud Platform Terms of Service

4. **Set up billing** (required, but free tier available):
   - Click "Select a project" → "New Project"
   - You'll be prompted to set up billing
   - Add a payment method (credit card)
   - **Note:** Google provides $300 free credit for new accounts (valid for 90 days)
   - You won't be charged unless you exceed free tier limits

## Step 2: Select or Create a Project

### Option A: Use Existing Project (Recommended)

If you already have a Google Cloud project, you can use it:

1. **Click the project dropdown** (top left, shows "Select a project")

2. **Select your existing project** from the list

3. **Verify the project is active:**
   - The project name should appear in the top bar
   - Note your Project ID (you'll need it later)

4. **Skip to Step 3** (Enable Required APIs)

**Note:** Make sure billing is enabled for your existing project. If not, see Step 3 in the billing section below.

### Option B: Create a New Project

If you want to create a new project specifically for KYC Bot:

1. **Click the project dropdown** (top left, shows "Select a project")

2. **Click "New Project"**

3. **Fill in project details:**
   - **Project name:** `kyc-bot` (or any name you prefer)
   - **Project ID:** Auto-generated (e.g., `kyc-bot-123456`)
   - **Organization:** Leave as default (if applicable)
   - **Location:** Leave as default

4. **Click "Create"**

5. **Wait for project creation** (takes a few seconds)

6. **Select your new project** from the dropdown

## Step 3: Verify Billing (For Existing Projects)

If using an existing project, verify billing is enabled:

1. **Go to Billing:**
   - Click hamburger menu (☰) → "Billing"
   - Or visit: https://console.cloud.google.com/billing

2. **Check if billing is linked:**
   - If you see "No billing accounts", create one
   - If billing exists but not linked, link it to your project

3. **Link billing to project:**
   ```powershell
   gcloud billing projects link YOUR_PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
   ```

## Step 4: Enable Required APIs

1. **Go to APIs & Services → Library:**
   - Click the hamburger menu (☰) → "APIs & Services" → "Library"
   - Or visit: https://console.cloud.google.com/apis/library

2. **Enable Cloud Run API:**
   - Search for "Cloud Run API"
   - Click on "Cloud Run API"
   - Click "Enable"
   - Wait for it to enable (takes 10-30 seconds)

3. **Enable Cloud Build API:**
   - Search for "Cloud Build API"
   - Click on "Cloud Build API"
   - Click "Enable"

4. **Enable Artifact Registry API:**
   - Search for "Artifact Registry API"
   - Click on "Artifact Registry API"
   - Click "Enable"

5. **Enable Container Registry API** (alternative to Artifact Registry):
   - Search for "Container Registry API"
   - Click on "Container Registry API"
   - Click "Enable"

6. **Verify APIs are enabled:**
   - Go to "APIs & Services" → "Enabled APIs"
   - You should see all the APIs listed above

## Step 5: Install Google Cloud SDK (gcloud CLI)

### Option A: Using Installer (Recommended for Windows)

1. **Download Google Cloud SDK:**
   - Visit: https://cloud.google.com/sdk/docs/install
   - Click "Download Google Cloud SDK"
   - Download the Windows installer

2. **Run the installer:**
   - Run `GoogleCloudSDKInstaller.exe`
   - Follow the installation wizard
   - Choose installation location (default is fine)
   - Click "Install"

3. **Initialize gcloud:**
   - Open a new PowerShell window
   - Run: `gcloud init`

### Option B: Using PowerShell (Alternative)

```powershell
# Download and install gcloud
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

## Step 6: Initialize gcloud CLI

1. **Open PowerShell** (new window)

2. **Run initialization:**
   ```powershell
   gcloud init
   ```

3. **Follow the prompts:**
   - **"Would you like to log in? (Y/n)"** → Type `Y` and press Enter
   - Browser will open → Sign in with your Google account
   - **"Pick cloud project to use:"** → Select your project (e.g., `kyc-bot-123456`)
   - **"Do you want to configure a default Compute Region and Zone? (Y/n)"** → Type `Y`
   - **"Which compute region would you like to use?"** → Select `us-central1` (or your preferred region)
   - **"Which compute zone would you like to use?"** → Select any zone (e.g., `us-central1-a`)

4. **Verify setup:**
   ```powershell
   gcloud config list
   ```

   **Expected output:**
   ```
   [core]
   account = your-email@gmail.com
   project = kyc-bot-123456
   ```

## Step 7: Set Up Authentication

1. **Set your project:**
   ```powershell
   gcloud config set project YOUR_PROJECT_ID
   ```
   Replace `YOUR_PROJECT_ID` with your actual project ID (e.g., `kyc-bot-123456`)

2. **Verify authentication:**
   ```powershell
   gcloud auth list
   ```

3. **Set application default credentials:**
   ```powershell
   gcloud auth application-default login
   ```
   - Browser will open → Sign in and authorize

## Step 8: Create Artifact Registry Repository (Optional but Recommended)

1. **Create repository:**
   ```powershell
   gcloud artifacts repositories create kyc-bot-repo `
       --repository-format=docker `
       --location=us-central1 `
       --description="Docker repository for KYC Bot"
   ```

2. **Configure Docker authentication:**
   ```powershell
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

## Step 9: Verify Setup

Run these commands to verify everything is set up:

```powershell
# Check project
gcloud config get-value project

# Check APIs are enabled
gcloud services list --enabled

# Check authentication
gcloud auth list

# Test Cloud Run access
gcloud run services list --region=us-central1
```

## Step 10: Set Environment Variables

Create a PowerShell script or set these in your session:

```powershell
# Set your project ID
$env:PROJECT_ID = "your-project-id-here"
$env:REGION = "us-central1"
$env:SERVICE_NAME = "kyc-bot"

# Verify
echo "Project ID: $env:PROJECT_ID"
echo "Region: $env:REGION"
```

## Step 11: Test Deployment

Now you're ready to deploy! Test with a simple build:

```powershell
# Set variables
$PROJECT_ID = "your-project-id"
$REGION = "us-central1"

# Build and push (this will take a few minutes)
gcloud builds submit --tag gcr.io/$PROJECT_ID/kyc-bot:test

# Or use Artifact Registry
gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/kyc-bot-repo/kyc-bot:test
```

## Quick Reference Commands

```powershell
# Set project
gcloud config set project YOUR_PROJECT_ID

# List projects
gcloud projects list

# Enable API
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check billing
gcloud billing accounts list

# Link billing to project
gcloud billing projects link YOUR_PROJECT_ID --billing-account=BILLING_ACCOUNT_ID

# View quotas
gcloud compute project-info describe --project=YOUR_PROJECT_ID
```

## Cost Management

### Free Tier Limits:
- **Cloud Run:** 2 million requests/month, 360,000 GiB-seconds/month
- **Cloud Build:** 120 build-minutes/day
- **Artifact Registry:** 0.5 GB storage

### Estimated Monthly Cost (1000 investigations/day):
- **Cloud Run:** ~$5-10/month
- **Cloud Build:** Free (within limits)
- **Storage:** Free (within limits)
- **Total:** ~$5-10/month

### Set Budget Alerts:
1. Go to "Billing" → "Budgets & alerts"
2. Click "Create Budget"
3. Set budget amount (e.g., $20/month)
4. Set alert threshold (e.g., 50%, 90%, 100%)

## Troubleshooting

### Issue: "Billing account not found"

**Solution:**
1. Go to "Billing" in Cloud Console
2. Create a billing account
3. Link it to your project:
   ```powershell
   gcloud billing projects link YOUR_PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
   ```

### Issue: "API not enabled"

**Solution:**
```powershell
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Issue: "Permission denied"

**Solution:**
1. Check you're using the correct project:
   ```powershell
   gcloud config get-value project
   ```
2. Verify authentication:
   ```powershell
   gcloud auth list
   ```

### Issue: "Quota exceeded"

**Solution:**
1. Check quotas: https://console.cloud.google.com/iam-admin/quotas
2. Request quota increase if needed
3. Or wait for quota reset (daily/monthly)

## Next Steps

After setup is complete:

1. ✅ Test Docker build locally
2. ✅ Build and push to Container Registry
3. ✅ Deploy to Cloud Run
4. ✅ Test the deployed service
5. ✅ Set up monitoring and alerts

See `DEPLOYMENT.md` for detailed deployment instructions.

## Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)
- [GCP Free Tier](https://cloud.google.com/free)
- [Billing Documentation](https://cloud.google.com/billing/docs)

