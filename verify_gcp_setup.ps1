# Verify GCP Setup for KYC Bot
Write-Host "=== GCP Setup Verification ===" -ForegroundColor Cyan
Write-Host ""

# Check current project
Write-Host "1. Current Project:" -ForegroundColor Yellow
$project = gcloud config get-value project 2>&1
Write-Host "   Project: $project" -ForegroundColor Green
Write-Host ""

# Check enabled APIs
Write-Host "2. Enabled APIs:" -ForegroundColor Yellow
$apis = gcloud services list --enabled 2>&1 | Select-String -Pattern "run|build|artifact"
if ($apis) {
    $apis | ForEach-Object { Write-Host "   $_" -ForegroundColor Green }
} else {
    Write-Host "   No matching APIs found" -ForegroundColor Red
}
Write-Host ""

# Check billing
Write-Host "3. Billing Status:" -ForegroundColor Yellow
$billing = gcloud billing projects describe $project 2>&1
if ($billing -match "billingAccountName") {
    Write-Host "   Billing is enabled" -ForegroundColor Green
} else {
    Write-Host "   WARNING: Billing may not be enabled" -ForegroundColor Yellow
    Write-Host "   Check at: https://console.cloud.google.com/billing" -ForegroundColor Yellow
}
Write-Host ""

# Check authentication
Write-Host "4. Authentication:" -ForegroundColor Yellow
$auth = gcloud auth list 2>&1 | Select-String -Pattern "ACTIVE"
if ($auth) {
    Write-Host "   $auth" -ForegroundColor Green
} else {
    Write-Host "   No active accounts found" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Verify billing is enabled (if not already)" -ForegroundColor White
Write-Host "2. Test deployment (see DEPLOYMENT.md)" -ForegroundColor White
Write-Host ""

