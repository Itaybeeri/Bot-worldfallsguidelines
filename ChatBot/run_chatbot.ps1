# PowerShell script to run the ChatBot Streamlit app

# Optional: create and activate a separate venv for ChatBot
if (-not (Test-Path .venv)) {
    python -m venv .venv
}
. .venv\Scripts\Activate.ps1

Write-Host "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Launching Streamlit app..."
streamlit run app.py
