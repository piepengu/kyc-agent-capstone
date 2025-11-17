# PowerShell script to run the KYC Bot agent
# This script ensures the environment variable is set before running

# Set the API key
$env:GOOGLE_API_KEY="AIzaSyAR0cUEIWvD1f6UIHC0zCPz9YoUg-VQaKI"

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        .\venv\Scripts\Activate.ps1
    }
}

# Get customer name from command line argument or use default
$customerName = $args[0]
if (-not $customerName) {
    $customerName = "Test Customer"
}

# Run the agent
Write-Host "Running KYC Bot for: $customerName" -ForegroundColor Green
python main.py --name "$customerName"

