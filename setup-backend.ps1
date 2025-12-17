# Setup script for Windows
Write-Host "Setting up NBFC Loan Sales Chatbot - Backend" -ForegroundColor Green

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed or not in PATH. Please install Python 3.10 or higher." -ForegroundColor Red
    exit 1
}

# Navigate to backend directory
Set-Location backend

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-Not (Test-Path ".env")) {
    Write-Host "`nCreating .env file..." -ForegroundColor Yellow
    Copy-Item "../.env.example" ".env"
    Write-Host "Please edit backend/.env and add your OpenAI API key!" -ForegroundColor Red
}

Write-Host "`n✅ Backend setup complete!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit backend/.env and add your OPENAI_API_KEY"
Write-Host "2. Run: cd backend"
Write-Host "3. Run: .\venv\Scripts\Activate.ps1"
Write-Host "4. Run: python main.py"
