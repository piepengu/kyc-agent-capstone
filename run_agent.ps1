# PowerShell script to run the KYC Bot agent
# This script ensures the environment variable is set before running

param(
    [Parameter(Mandatory=$false)]
    [string]$Name = "Test Customer"
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   KYC Bot - Automated KYC Compliance" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Load environment variables from .env file
Write-Host "[*] Loading environment variables from .env file..." -ForegroundColor Yellow
$envPath = Join-Path $PSScriptRoot ".env"

if (Test-Path $envPath) {
    # Read .env file line by line and set environment variables
    Get-Content $envPath | ForEach-Object {
        $line = $_.Trim()
        # Skip empty lines and comments
        if ($line -and -not $line.StartsWith('#')) {
            if ($line -match '^\s*([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                # Remove quotes if present
                if ($value.StartsWith('"') -and $value.EndsWith('"')) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                if ($value.StartsWith("'") -and $value.EndsWith("'")) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
                Write-Host "   [+] Loaded: $key" -ForegroundColor Gray
            }
        }
    }
    Write-Host "[+] Environment variables loaded`n" -ForegroundColor Green
} else {
    Write-Host "[ERROR] .env file not found at $envPath" -ForegroundColor Red
    Write-Host "Please create a .env file with GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID" -ForegroundColor Yellow
    exit 1
}

# Step 2: Verify API key is set
if (-not $env:GOOGLE_API_KEY) {
    Write-Host "[ERROR] GOOGLE_API_KEY not found in environment variables" -ForegroundColor Red
    Write-Host "Please check your .env file contains: GOOGLE_API_KEY=your_key_here" -ForegroundColor Yellow
    exit 1
}

# Step 3: Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
    if (Test-Path ".\venv\Scripts\Activate.ps1") {
        & .\venv\Scripts\Activate.ps1
        Write-Host "[+] Virtual environment activated`n" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Virtual environment not found" -ForegroundColor Red
        Write-Host "Please create a virtual environment first: python -m venv venv" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "[+] Virtual environment already activated`n" -ForegroundColor Green
}

# Step 4: Run the agent
Write-Host "[*] Starting KYC investigation for: $Name" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor White

try {
    python main.py --name "$Name"
    Write-Host "`n[+] Investigation complete!`n" -ForegroundColor Green
} catch {
    Write-Host "`n[ERROR] Failed to run agent: $_" -ForegroundColor Red
    exit 1
}

