$backendProcess = Start-Process -FilePath "cmd.exe" -ArgumentList "/c cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000" -PassThru -NoNewWindow
$frontendProcess = Start-Process -FilePath "cmd.exe" -ArgumentList "/c cd frontend && npm run dev" -PassThru -NoNewWindow

Write-Host "Backend PID: $($backendProcess.Id)"
Write-Host "Frontend PID: $($frontendProcess.Id)"
Write-Host "Press Ctrl+C to stop (might need to kill processes manually if this script exits)"

# Wait for user input to exit
Read-Host "Press Enter to exit and kill processes..."

Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
