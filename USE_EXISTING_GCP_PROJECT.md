# Using an Existing Google Cloud Project

Quick guide for using your existing GCP project instead of creating a new one.

## Quick Steps

### 1. Select Your Existing Project

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" (top left)
3. Choose your existing project from the list

### 2. Verify Billing is Enabled

```powershell
# Check if billing is linked
gcloud billing projects describe YOUR_PROJECT_ID

# If not linked, link it
gcloud billing projects link YOUR_PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

Or via Console:
- Go to: https://console.cloud.google.com/billing
- Make sure your project is linked to a billing account

### 3. Enable Required APIs

```powershell
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 4. Verify APIs are Enabled

```powershell
# List enabled APIs
gcloud services list --enabled | Select-String "run|build|artifact"
```

### 5. Get Your Project ID

```powershell
# Get project ID
gcloud config get-value project

# Or list all projects
gcloud projects list
```

### 6. You're Ready!

Use your existing project ID in deployment commands:

```powershell
# Set variables (use your actual project ID)
$PROJECT_ID = "your-existing-project-id"
$REGION = "us-central1"

# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/kyc-bot:latest
gcloud run deploy kyc-bot --image gcr.io/$PROJECT_ID/kyc-bot:latest --region $REGION
```

## Benefits of Using Existing Project

✅ No need to create new project  
✅ Reuse existing billing account  
✅ Centralized resource management  
✅ Easier to manage multiple services  

## Important Notes

⚠️ **Billing:** Make sure billing is enabled for your project  
⚠️ **Quotas:** Check if you have available quotas for Cloud Run  
⚠️ **Permissions:** Ensure you have necessary permissions (Editor or Owner role)  
⚠️ **APIs:** Enable required APIs if not already enabled  

## Check Permissions

```powershell
# Check your permissions
gcloud projects get-iam-policy YOUR_PROJECT_ID --flatten="bindings[].members" --filter="bindings.members:user:YOUR_EMAIL"
```

You need one of these roles:
- **Owner** (full access)
- **Editor** (can deploy services)
- **Cloud Run Admin** + **Cloud Build Editor** (specific permissions)

## Troubleshooting

### "Permission denied" error

**Solution:** Ask project owner to grant you Editor role:
```powershell
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="user:YOUR_EMAIL" \
    --role="roles/editor"
```

### "Billing account not found"

**Solution:** Link billing account:
```powershell
gcloud billing projects link YOUR_PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

### "API not enabled"

**Solution:** Enable the API:
```powershell
gcloud services enable API_NAME
```

## Next Steps

After setting up your existing project:

1. ✅ Verify billing is enabled
2. ✅ Enable required APIs
3. ✅ Check permissions
4. ✅ Proceed with deployment (see `DEPLOYMENT.md`)

