# PowerShell script to run the data preprocessing stage

if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Running data preprocessing..."
python -m rag_1_Data_preprocessing.prepare

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}
