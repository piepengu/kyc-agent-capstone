# Deploy KYC Bot to Google Cloud Run
# Make sure you're in the project directory and have .env file with API keys

Write-Host "=== KYC Bot Cloud Run Deployment ===" -ForegroundColor Cyan
Write-Host ""

# Find gcloud executable
$gcloudPath = $null
$possiblePaths = @(
    "C:\Program Files (x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "C:\Program Files\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
    "$env:ProgramFiles(x86)\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $gcloudPath = $path
        break
    }
}

# Try to find gcloud in PATH
if (-not $gcloudPath) {
    $gcloudInPath = Get-Command gcloud -ErrorAction SilentlyContinue
    if ($gcloudInPath) {
        $gcloudPath = $gcloudInPath.Source
    }
}

if (-not $gcloudPath) {
    Write-Host "ERROR: gcloud not found!" -ForegroundColor Red
    Write-Host "Please make sure Google Cloud SDK is installed." -ForegroundColor Yellow
    Write-Host "Or run this from Command Prompt where gcloud is available." -ForegroundColor Yellow
    exit 1
}

Write-Host "Using gcloud: $gcloudPath" -ForegroundColor Gray
Write-Host ""

# Set variables
$PROJECT_ID = "finsight-ai-jd"
$REGION = "us-central1"
$SERVICE_NAME = "kyc-bot"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Project ID: $PROJECT_ID" -ForegroundColor White
Write-Host "  Region: $REGION" -ForegroundColor White
Write-Host "  Service Name: $SERVICE_NAME" -ForegroundColor White
Write-Host "  Image: $IMAGE_NAME" -ForegroundColor White
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "ERROR: .env file not found!" -ForegroundColor Red
    Write-Host "Please create .env file with GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID" -ForegroundColor Yellow
    exit 1
}

# Read environment variables from .env
$envVars = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

if (-not $envVars.ContainsKey("GOOGLE_API_KEY")) {
    Write-Host "ERROR: GOOGLE_API_KEY not found in .env file!" -ForegroundColor Red
    exit 1
}

if (-not $envVars.ContainsKey("GOOGLE_SEARCH_ENGINE_ID")) {
    Write-Host "ERROR: GOOGLE_SEARCH_ENGINE_ID not found in .env file!" -ForegroundColor Red
    exit 1
}

Write-Host "Found API keys in .env file" -ForegroundColor Green
Write-Host ""

# Step 1: Build and push image
Write-Host "Step 1: Building and pushing Docker image..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes..." -ForegroundColor Gray
Write-Host ""

& $gcloudPath builds submit --tag $IMAGE_NAME`:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host ""

# Step 2: Deploy to Cloud Run
Write-Host "Step 2: Deploying to Cloud Run..." -ForegroundColor Yellow
Write-Host ""

$envVarsString = "GOOGLE_API_KEY=$($envVars['GOOGLE_API_KEY']),GOOGLE_SEARCH_ENGINE_ID=$($envVars['GOOGLE_SEARCH_ENGINE_ID'])"

& $gcloudPath run deploy $SERVICE_NAME `
    --image $IMAGE_NAME`:latest `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --set-env-vars $envVarsString `
    --memory 1Gi `
    --cpu 1 `
    --timeout 300 `
    --max-instances 10

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Deployment failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Deployment Complete! ===" -ForegroundColor Green
Write-Host ""

# Get service URL
Write-Host "Getting service URL..." -ForegroundColor Yellow
$serviceUrl = & $gcloudPath run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'

Write-Host ""
Write-Host "Service URL: $serviceUrl" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test the service:" -ForegroundColor Yellow
Write-Host "  Health: $serviceUrl/health" -ForegroundColor White
Write-Host "  API: $serviceUrl/api/v1/investigate" -ForegroundColor White
Write-Host ""

