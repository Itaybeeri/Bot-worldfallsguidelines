# PowerShell script to run the vector DB ingest stage

if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Running vector DB ingest..."
python -m rag_4_VectorDB_ingest.ingest

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}
