# World Falls Guidelines ChatBot

A Streamlit chatbot that uses Retrieval-Augmented Generation (RAG) with ChromaDB and OpenAI LLM for the World Falls Guidelines project.

## IMPORTANT: OpenAI API Key Required

To use the chatbot, you must provide an OpenAI API key. **Do NOT commit your API key to version control.**

**How to add your API key:**

1. Create a file named `openai_key.txt` in the `ChatBot` folder (next to `config.py`).
2. Paste your OpenAI API key (e.g., `sk-...`) as the only line in that file.
3. This file is already in `.gitignore` and will not be committed to GitHub.

If you run the chatbot without an API key, you will be prompted in the UI to add `openai_key.txt` with your key.

You can get an API key here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

## Features

- User prompt input and chat history
- RAG retrieval from your vector DB (ChromaDB)
- OpenAI LLM call with context and adjustable parameters
- Source/citation display

## Quick Start

### Option 1: Run with Script (Recommended)

```powershell
./run_chatbot.ps1
```

This script will automatically install dependencies and launch the chatbot.

### Option 2: Manual Setup

1. Install requirements: `pip install -r requirements.txt`
2. Add your OpenAI API key to `openai_key.txt` (see above)
3. Run: `streamlit run app.py`

## Notes

- Make sure your vector DB is built and available in `../RAG/data/vectordb/` before
- This is a POC for demonstration only
