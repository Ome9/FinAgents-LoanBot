# Setup script for Frontend
Write-Host "Setting up NBFC Loan Sales Chatbot - Frontend" -ForegroundColor Green

# Check Node.js version
Write-Host "`nChecking Node.js version..." -ForegroundColor Yellow
node --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Node.js is not installed or not in PATH. Please install Node.js 18 or higher." -ForegroundColor Red
    exit 1
}

# Navigate to frontend directory
Set-Location frontend

# Install dependencies
Write-Host "`nInstalling npm dependencies..." -ForegroundColor Yellow
npm install

Write-Host "`n✅ Frontend setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Make sure backend is running on port 8000"
Write-Host "2. Run: cd frontend"
Write-Host "3. Run: npm run dev"
Write-Host "4. Open browser at http://localhost:5173"
