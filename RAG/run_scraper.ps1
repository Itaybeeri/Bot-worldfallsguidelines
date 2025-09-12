# Run scraper script using virtual environment if available
if (Test-Path .venv\Scripts\Activate.ps1) {
    Write-Host "Activating .venv..."
    . .\.venv\Scripts\Activate.ps1
}

# Run the scraper as a module (preferred) so package imports work
Write-Host "Running scraper..."
python -m scraper.scraper

# Deactivate venv if activated
if (Get-Command deactivate -ErrorAction SilentlyContinue) {
    deactivate
}