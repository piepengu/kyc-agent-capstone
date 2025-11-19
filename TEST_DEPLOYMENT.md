# Testing Deployment Setup

This guide covers testing the KYC Bot deployment in different environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Test Local Docker Build](#test-local-docker-build)
3. [Test API Server Locally](#test-api-server-locally)
4. [Test Docker Container](#test-docker-container)
5. [Test Cloud Run Deployment](#test-cloud-run-deployment)
6. [Test API Endpoints](#test-api-endpoints)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

Before testing, ensure you have:

- ✅ Docker installed and running
- ✅ `.env` file with API keys configured
- ✅ Virtual environment activated (for local testing)
- ✅ All dependencies installed (`pip install -r requirements.txt`)

## Test Local Docker Build

### Step 1: Build Docker Image

```bash
# Build the image
docker build -t kyc-bot:test .

# Verify image was created
docker images | grep kyc-bot
```

**Expected Output:**
```
kyc-bot    test    <image-id>    <time>    <size>
```

### Step 2: Test Docker Image Structure

```bash
# Check image layers
docker history kyc-bot:test

# Inspect image
docker inspect kyc-bot:test
```

## Test API Server Locally

### Step 1: Start API Server

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
# or
source venv/bin/activate     # macOS/Linux

# Start Flask development server
python api.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:8080
```

### Step 2: Test Health Endpoint

Open a new terminal and run:

```bash
# Test health endpoint
curl http://localhost:8080/health

# Or use PowerShell (Windows)
Invoke-WebRequest -Uri http://localhost:8080/health -Method GET
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "KYC Bot",
  "version": "1.0.0"
}
```

### Step 3: Test Investigation Endpoint

```bash
# Test investigation endpoint
curl -X POST http://localhost:8080/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "John Doe"}'

# Or use PowerShell (Windows)
$body = @{customer_name="John Doe"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:8080/api/v1/investigate `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

**Expected Response:**
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

## Test Docker Container

### Step 1: Run Container with Environment Variables

```bash
# Create .env file if not exists
# Ensure it contains:
# GOOGLE_API_KEY=your_key
# GOOGLE_SEARCH_ENGINE_ID=your_id

# Run container with API server
docker run -d \
  --name kyc-bot-test \
  --env-file .env \
  -p 8080:8080 \
  kyc-bot:test

# Check container is running
docker ps | grep kyc-bot-test
```

### Step 2: Test Container Endpoints

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test investigation endpoint
curl -X POST http://localhost:8080/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Test Customer"}'
```

### Step 3: View Container Logs

```bash
# View logs
docker logs kyc-bot-test

# Follow logs in real-time
docker logs -f kyc-bot-test
```

### Step 4: Test CLI Mode in Container

```bash
# Run container in CLI mode (override CMD)
docker run --rm \
  --env-file .env \
  kyc-bot:test \
  python main.py --name "Test Customer"
```

### Step 5: Clean Up

```bash
# Stop and remove container
docker stop kyc-bot-test
docker rm kyc-bot-test
```

## Test Cloud Run Deployment

### Step 1: Set Up GCP Project

```bash
# Set project ID
export PROJECT_ID=your-gcp-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 2: Build and Push to Container Registry

```bash
# Build and push
gcloud builds submit --tag gcr.io/$PROJECT_ID/kyc-bot:test

# Verify image
gcloud container images list --repository=gcr.io/$PROJECT_ID
```

### Step 3: Deploy to Cloud Run

```bash
# Deploy with environment variables
gcloud run deploy kyc-bot-test \
  --image gcr.io/$PROJECT_ID/kyc-bot:test \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your_key,GOOGLE_SEARCH_ENGINE_ID=your_id \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300
```

**Expected Output:**
```
Service [kyc-bot-test] revision [kyc-bot-test-00001-abc] has been deployed
Service URL: https://kyc-bot-test-xxxxx-uc.a.run.app
```

### Step 4: Test Cloud Run Service

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe kyc-bot-test \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test investigation endpoint
curl -X POST $SERVICE_URL/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Test Customer"}'
```

### Step 5: View Cloud Run Logs

```bash
# View logs
gcloud run services logs read kyc-bot-test \
  --platform managed \
  --region us-central1 \
  --limit 50

# Stream logs
gcloud run services logs tail kyc-bot-test \
  --platform managed \
  --region us-central1
```

### Step 6: Clean Up Test Deployment

```bash
# Delete test service
gcloud run services delete kyc-bot-test \
  --platform managed \
  --region us-central1
```

## Test API Endpoints

### Using cURL

```bash
# Health check
curl http://localhost:8080/health

# Investigation
curl -X POST http://localhost:8080/api/v1/investigate \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "John Doe"}'

# Metrics
curl http://localhost:8080/api/v1/metrics
```

### Using PowerShell (Windows)

```powershell
# Health check
Invoke-WebRequest -Uri http://localhost:8080/health -Method GET

# Investigation
$body = @{
    customer_name = "John Doe"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:8080/api/v1/investigate `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

# Metrics
Invoke-WebRequest -Uri http://localhost:8080/api/v1/metrics -Method GET
```

### Using Python Requests

Create `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8080"

# Test health
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Test investigation
response = requests.post(
    f"{BASE_URL}/api/v1/investigate",
    json={"customer_name": "John Doe"}
)
print("Investigation:", json.dumps(response.json(), indent=2))

# Test metrics
response = requests.get(f"{BASE_URL}/api/v1/metrics")
print("Metrics:", response.json())
```

Run:
```bash
python test_api.py
```

### Using Postman

1. Import collection:
   - `GET /health`
   - `POST /api/v1/investigate`
   - `GET /api/v1/metrics`

2. Set base URL: `http://localhost:8080`

3. For investigation endpoint, set body:
   ```json
   {
     "customer_name": "John Doe"
   }
   ```

## Troubleshooting

### Issue: Docker build fails

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Ensure requirements.txt includes Flask
grep Flask requirements.txt

# Rebuild image
docker build --no-cache -t kyc-bot:test .
```

### Issue: API server won't start

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8080
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # macOS/Linux

# Kill process or change port in api.py
```

### Issue: Environment variables not loaded in Docker

**Error:** `GOOGLE_API_KEY environment variable not set`

**Solution:**
```bash
# Ensure .env file exists and has correct format
cat .env

# Use --env-file flag
docker run --env-file .env kyc-bot:test
```

### Issue: Cloud Run deployment fails

**Error:** `Permission denied` or `API not enabled`

**Solution:**
```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check permissions
gcloud projects get-iam-policy $PROJECT_ID
```

### Issue: API returns 500 error

**Check logs:**
```bash
# Docker
docker logs kyc-bot-test

# Cloud Run
gcloud run services logs read kyc-bot-test --limit 50
```

**Common causes:**
- Missing environment variables
- API key invalid
- Network connectivity issues
- Timeout (increase timeout in Cloud Run)

## Quick Test Checklist

- [ ] Docker image builds successfully
- [ ] API server starts locally
- [ ] Health endpoint returns 200
- [ ] Investigation endpoint works
- [ ] Docker container runs with API server
- [ ] Docker container runs in CLI mode
- [ ] Cloud Run deployment succeeds
- [ ] Cloud Run service responds to requests
- [ ] Logs are accessible
- [ ] Environment variables are loaded correctly

## Next Steps

After successful testing:

1. ✅ Deploy to production Cloud Run
2. ✅ Set up monitoring and alerts
3. ✅ Configure custom domain (optional)
4. ✅ Set up CI/CD pipeline (optional)
5. ✅ Add authentication (for production)

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- See `DEPLOYMENT.md` for detailed deployment instructions

