# PowerShell script to run the full RAG pipeline in order

if (-not (Test-Path .venv)) {
    python -m venv .venv
}

Write-Host "Installing requirements..."
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "Running all pipeline stages..."
./run_0_scraper.ps1
./run_1_data_preprocessing.ps1
./run_2_Chunking.ps1
./run_3_Embeddings.ps1
./run_4_VectorDB_ingest.ps1

Write-Host "Pipeline complete."
