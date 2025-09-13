# PowerShell script to run the embeddings stage

if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    . .\.venv\Scripts\Activate.ps1
}

Write-Host "Running embeddings..."
python -m rag_3_Embeddings.embed

if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}
