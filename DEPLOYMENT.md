# KYC Bot - Deployment Guide

This guide covers deploying the KYC Bot to Google Cloud Run and other cloud platforms.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Docker Deployment](#local-docker-deployment)
3. [Google Cloud Run Deployment](#google-cloud-run-deployment)
4. [Environment Variables](#environment-variables)
5. [API Endpoint Design](#api-endpoint-design)
6. [Monitoring & Logging](#monitoring--logging)
7. [Scaling & Performance](#scaling--performance)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Accounts & Tools
- **Google Cloud Platform (GCP) Account** with billing enabled
- **Google Cloud SDK (gcloud)** installed and configured
- **Docker** installed (for local testing)
- **Google API Key** with access to:
  - Gemini API
  - Google Custom Search API

### Required APIs Enabled
Enable the following APIs in Google Cloud Console:
- Cloud Run API
- Container Registry API (or Artifact Registry API)
- Cloud Build API (optional, for automated builds)

## Local Docker Deployment

### 1. Build Docker Image

```bash
# Build the image
docker build -t kyc-bot:latest .

# Test locally
docker run --env-file .env kyc-bot:latest python main.py --name "Test Customer"
```

### 2. Run with Environment Variables

```bash
# Create .env file with your API keys
echo "GOOGLE_API_KEY=your_key_here" > .env
echo "GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id" >> .env

# Run container
docker run --env-file .env kyc-bot:latest
```

## Google Cloud Run Deployment

### Step 1: Set Up GCP Project

```bash
# Set your project ID
export PROJECT_ID=your-gcp-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 2: Build and Push Container

```bash
# Set variables
export PROJECT_ID=your-gcp-project-id
export REGION=us-central1
export SERVICE_NAME=kyc-bot

# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Or use Artifact Registry (recommended)
gcloud artifacts repositories create kyc-bot-repo \
    --repository-format=docker \
    --location=$REGION

gcloud builds submit --tag $REGION-docker.pkg.dev/$PROJECT_ID/kyc-bot-repo/$SERVICE_NAME:latest
```

### Step 3: Deploy to Cloud Run

```bash
# Deploy with environment variables
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/kyc-bot-repo/$SERVICE_NAME:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars GOOGLE_API_KEY=your_key_here,GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10
```

### Step 4: Secure Environment Variables (Recommended)

For production, use Secret Manager:

```bash
# Create secrets
echo -n "your_api_key" | gcloud secrets create google-api-key --data-file=-
echo -n "your_search_engine_id" | gcloud secrets create google-search-engine-id --data-file=-

# Grant Cloud Run access
gcloud secrets add-iam-policy-binding google-api-key \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Deploy with secrets
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/kyc-bot-repo/$SERVICE_NAME:latest \
    --update-secrets GOOGLE_API_KEY=google-api-key:latest,GOOGLE_SEARCH_ENGINE_ID=google-search-engine-id:latest \
    --region $REGION
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google API key for Gemini and Custom Search | `AIzaSy...` |
| `GOOGLE_SEARCH_ENGINE_ID` | Custom Search Engine ID | `322c8536721cd40d8` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |
| `LOG_DIR` | Directory for log files | `logs/` |
| `MAX_RETRIES` | Maximum API retry attempts | `3` |
| `SIMILARITY_THRESHOLD` | Watchlist matching threshold | `0.85` |

### Setting in Cloud Run

```bash
gcloud run services update $SERVICE_NAME \
    --set-env-vars LOG_LEVEL=INFO,MAX_RETRIES=3 \
    --region $REGION
```

## API Endpoint Design

### Option 1: REST API with Flask/FastAPI

Create `api.py` for a web API:

```python
from flask import Flask, request, jsonify
from main import main as run_kyc_investigation
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/investigate', methods=['POST'])
def investigate():
    data = request.json
    customer_name = data.get('customer_name')
    
    if not customer_name:
        return jsonify({"error": "customer_name is required"}), 400
    
    # Run investigation
    result = run_kyc_investigation(customer_name)
    
    return jsonify(result), 200
```

### Option 2: Cloud Run with HTTP Trigger

Deploy as a Cloud Function or Cloud Run service that accepts HTTP requests.

### Recommended API Endpoints

```
POST /api/v1/investigate
  Body: { "customer_name": "John Doe" }
  Response: {
    "customer_name": "John Doe",
    "search_results": [...],
    "watchlist_results": {...},
    "final_report": "...",
    "risk_level": "LOW|MEDIUM|HIGH",
    "execution_time": 8.5
  }

GET /api/v1/health
  Response: { "status": "healthy" }

GET /api/v1/metrics
  Response: { "total_investigations": 100, ... }
```

## Monitoring & Logging

### Cloud Logging

Cloud Run automatically sends logs to Cloud Logging. View logs:

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME" --limit 50
```

### Custom Metrics

Add custom metrics for:
- Investigation count
- Average execution time
- Error rates
- API call success rates

### Log Aggregation

Logs are automatically aggregated in Cloud Logging. Filter by:
- Severity level
- Agent name
- Customer name (if logged)
- Error type

## Scaling & Performance

### Cloud Run Configuration

```bash
# Configure autoscaling
gcloud run services update $SERVICE_NAME \
    --min-instances 0 \
    --max-instances 10 \
    --concurrency 10 \
    --cpu 1 \
    --memory 1Gi \
    --region $REGION
```

### Performance Optimization

1. **Caching**: Cache watchlist data and search results
2. **Parallel Processing**: Process multiple customers in parallel
3. **Connection Pooling**: Reuse API connections
4. **Async Operations**: Use async/await for I/O operations

### Cost Optimization

- Use minimum instances = 0 (scale to zero)
- Set appropriate memory limits
- Monitor API quota usage
- Use Cloud Run's pay-per-use pricing

## Troubleshooting

### Common Issues

#### 1. API Key Not Found
```
Error: GOOGLE_API_KEY environment variable not set
```
**Solution**: Ensure environment variables are set in Cloud Run:
```bash
gcloud run services update $SERVICE_NAME --set-env-vars GOOGLE_API_KEY=your_key
```

#### 2. Container Build Fails
```
Error: Failed to build container
```
**Solution**: Check Dockerfile syntax and dependencies:
```bash
docker build -t kyc-bot:test .
```

#### 3. Timeout Errors
```
Error: Request timeout
```
**Solution**: Increase Cloud Run timeout:
```bash
gcloud run services update $SERVICE_NAME --timeout 300
```

#### 4. Memory Issues
```
Error: Container killed due to memory limit
```
**Solution**: Increase memory allocation:
```bash
gcloud run services update $SERVICE_NAME --memory 2Gi
```

### Debugging

#### View Logs
```bash
# Real-time logs
gcloud run services logs tail $SERVICE_NAME --region $REGION

# Filter by severity
gcloud logging read "severity>=ERROR" --limit 50
```

#### Test Locally
```bash
# Test with Docker
docker run --env-file .env kyc-bot:latest python main.py --name "Test"

# Test API locally
python api.py  # If API endpoint is implemented
```

## Alternative Deployment Options

### 1. AWS Lambda / API Gateway
- Serverless deployment
- Pay per request
- Good for low-volume usage

### 2. Azure Container Instances
- Simple container deployment
- No orchestration needed
- Good for testing

### 3. Kubernetes (GKE)
- Full orchestration
- Better for high-volume production
- More complex setup

### 4. Heroku
- Simple deployment
- Good for prototypes
- Limited scalability

## Security Best Practices

1. **Never commit API keys** - Use Secret Manager or environment variables
2. **Use HTTPS** - Cloud Run provides HTTPS by default
3. **Authentication** - Consider adding authentication for production
4. **Rate Limiting** - Implement rate limiting to prevent abuse
5. **Input Validation** - Validate all inputs before processing
6. **Logging** - Don't log sensitive customer data

## Cost Estimation

### Cloud Run Pricing (Approximate)
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests
- **Free Tier**: 2 million requests/month, 360,000 GiB-seconds/month

### Example Monthly Cost (1000 investigations/day)
- Requests: ~30,000/month = $0.01
- Compute: ~$5-10/month (depending on execution time)
- **Total**: ~$5-10/month

## Next Steps

1. ✅ Set up GCP project and enable APIs
2. ✅ Build and test Docker image locally
3. ✅ Deploy to Cloud Run
4. ✅ Configure environment variables
5. ✅ Set up monitoring and alerts
6. ✅ Test production deployment
7. ⏳ Implement API endpoints (optional)
8. ⏳ Set up CI/CD pipeline (optional)

## References

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Google Secret Manager](https://cloud.google.com/secret-manager/docs)
- [Cloud Logging](https://cloud.google.com/logging/docs)

