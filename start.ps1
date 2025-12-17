# Quick Start Script - Runs both backend and frontend
Write-Host "Starting NBFC Loan Sales Chatbot..." -ForegroundColor Green

# Start backend in a new PowerShell window
Write-Host "`nStarting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; python main.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 5

# Start frontend in a new PowerShell window
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "`n✅ Both servers are starting!" -ForegroundColor Green
Write-Host "`nBackend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
Write-Host "`nAPI Docs: http://localhost:8000/docs" -ForegroundColor Cyan
