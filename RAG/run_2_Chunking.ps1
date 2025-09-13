# PowerShell script to run the chunking stage

if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Running chunking..."
python -m rag_2_Chunking.chunker

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}
