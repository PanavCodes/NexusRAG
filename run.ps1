Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Launching NexusRAG (Gemini and OpenRouter Free)   " -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

Set-Location -Path "$PSScriptRoot"

# Load .env file if it exists
if (Test-Path ".env") {
    Get-Content ".env" | Where-Object { $_ -match '^[^#=]+=.+' } | ForEach-Object {
        $parts = $_.Split('=', 2)
        $k = $parts[0].Trim()
        $v = $parts[1].Trim().Trim('"\'')
        [System.Environment]::SetEnvironmentVariable($k, $v, "Process")
    }
}

if (-not $env:GEMINI_API_KEY -and -not $env:OPENROUTER_API_KEY) {
    Write-Host "[INFO] No API keys detected in .env or environment." -ForegroundColor Yellow
    Write-Host "Configure keys in .env or enter them inside the UI Settings tab." -ForegroundColor Yellow
}

Write-Host "Starting NexusRAG Streamlit Server..." -ForegroundColor Cyan
Start-Process "http://localhost:8501"
& ".\.venv\Scripts\streamlit.exe" run main.py
