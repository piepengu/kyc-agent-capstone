# PowerShell script to run the KYC Bot agent
# This script ensures the environment variable is set before running

# Load API key from .env file
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GOOGLE_API_KEY=(.+)") {
        $env:GOOGLE_API_KEY = $matches[1].Trim()
    } else {
        Write-Host "ERROR: GOOGLE_API_KEY not found in .env file" -ForegroundColor Red
        Write-Host "Please create a .env file with: GOOGLE_API_KEY=your_key_here" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "ERROR: .env file not found" -ForegroundColor Red
    Write-Host "Please create a .env file with: GOOGLE_API_KEY=your_key_here" -ForegroundColor Yellow
    exit 1
}

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

