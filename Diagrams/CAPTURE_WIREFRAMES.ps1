# Automated Wireframe Capture Script
# Captures screenshots from running application for presentation

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "    🎨 AUTOMATED WIREFRAME CAPTURE FOR EY TECHATHON      " -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if servers are running
Write-Host "🔍 Checking if servers are running..." -ForegroundColor Yellow

try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:5173" -Method Head -TimeoutSec 2 -ErrorAction SilentlyContinue
    $frontendRunning = $true
    Write-Host "   ✅ Frontend: Running (Port 5173)" -ForegroundColor Green
} catch {
    $frontendRunning = $false
    Write-Host "   ❌ Frontend: Not running" -ForegroundColor Red
}

try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/docs" -Method Head -TimeoutSec 2 -ErrorAction SilentlyContinue
    $backendRunning = $true
    Write-Host "   ✅ Backend: Running (Port 8000)" -ForegroundColor Green
} catch {
    $backendRunning = $false
    Write-Host "   ❌ Backend: Not running" -ForegroundColor Red
}

Write-Host ""

# Step 2: Start servers if not running
if (-not $frontendRunning -or -not $backendRunning) {
    Write-Host "⚠️  Servers not running! Starting them now..." -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $backendRunning) {
        Write-Host "   🚀 Starting Backend Server..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", `
            "cd D:\EY-Techathon\backend; & D:/EY-Techathon/.venv/Scripts/Activate.ps1; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
        Write-Host "   ✅ Backend terminal opened" -ForegroundColor Green
    }
    
    if (-not $frontendRunning) {
        Write-Host "   🚀 Starting Frontend Server..." -ForegroundColor Cyan
        Start-Process powershell -ArgumentList "-NoExit", "-Command", `
            "cd D:\EY-Techathon\frontend; npm run dev"
        Write-Host "   ✅ Frontend terminal opened" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "⏳ Waiting 15 seconds for servers to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 15
    Write-Host "   ✅ Servers should be ready now!" -ForegroundColor Green
    Write-Host ""
}

# Step 3: Check if Node.js is installed
Write-Host "🔍 Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "   ✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "   ❌ Node.js not found!" -ForegroundColor Red
    Write-Host "   📥 Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host "   Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}
Write-Host ""

# Step 4: Setup Puppeteer
Set-Location "D:\EY-Techathon\Diagrams"

if (-not (Test-Path "package.json")) {
    Write-Host "📦 Initializing Node.js project..." -ForegroundColor Yellow
    npm init -y | Out-Null
    Write-Host "   ✅ package.json created" -ForegroundColor Green
}

if (-not (Test-Path "node_modules\puppeteer")) {
    Write-Host "📦 Installing Puppeteer (this may take 2-3 minutes)..." -ForegroundColor Yellow
    Write-Host "   ⏳ Downloading Chromium browser..." -ForegroundColor Cyan
    npm install puppeteer --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Puppeteer installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Puppeteer installation failed!" -ForegroundColor Red
        Write-Host "   Try running: npm install puppeteer" -ForegroundColor Yellow
        exit
    }
} else {
    Write-Host "✅ Puppeteer already installed" -ForegroundColor Green
}
Write-Host ""

# Step 5: Run capture script
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "    📸 STARTING SCREENSHOT CAPTURE                         " -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 A Chrome window will open automatically" -ForegroundColor Yellow
Write-Host "   Don't close it - it's capturing screenshots!" -ForegroundColor Yellow
Write-Host ""

node capture_wireframes.js

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "    ✅ ALL WIREFRAMES CAPTURED SUCCESSFULLY!              " -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""
    
    # List captured files
    Write-Host "📁 Captured Files:" -ForegroundColor Cyan
    Get-ChildItem -Path "wireframe_*.png" -ErrorAction SilentlyContinue | ForEach-Object {
        $sizeKB = [math]::Round($_.Length / 1KB, 1)
        Write-Host "   ✅ $($_.Name) - $sizeKB KB" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "📊 Next Steps:" -ForegroundColor Yellow
    Write-Host "   1. Open your PowerPoint presentation" -ForegroundColor White
    Write-Host "   2. Insert → Pictures → Select wireframe_*.png files" -ForegroundColor White
    Write-Host "   3. Resize to fit slides (maintain aspect ratio)" -ForegroundColor White
    Write-Host "   4. Add annotations/callouts as needed" -ForegroundColor White
    Write-Host ""
    Write-Host "🎉 Your presentation assets are ready!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Capture failed! Check the error messages above." -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   • Make sure both servers are running" -ForegroundColor White
    Write-Host "   • Check http://localhost:5173 in your browser" -ForegroundColor White
    Write-Host "   • Try running capture_wireframes.js directly: node capture_wireframes.js" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to close..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
