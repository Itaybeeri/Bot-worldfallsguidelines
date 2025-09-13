# World Falls Guidelines

A Streamlit chatbot that uses Retrieval-Augmented Generation (RAG) with ChromaDB and OpenAI LLM for the World Falls Guidelines project.

## IMPORTANT: OpenAI API Key Required

To use the chatbot, you must provide an OpenAI API key. You can do this in one of two ways:

1. **Recommended:** Set your API key in `config.py` as `OPENAI_API_KEY = "sk-..."` before running the app.
2. Or, enter your API key in the sidebar when the app is running.

If you run the chatbot without an API key, you will be prompted to add it in the sidebar or in `config.py`.

You can get an API key here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

## Features

- User prompt input and chat history
- RAG retrieval from your vector DB (ChromaDB)
- OpenAI LLM call with context and adjustable parameters
- Source/citation display

## Usage

1. Install requirements: `pip install -r requirements.txt`
2. Run: `streamlit run app.py`
3. Enter your OpenAI API key in the sidebar or set it in `config.py`

## Notes

- Make sure your vector DB is built and available in `../RAG/data/vectordb/`
- This is a POC for demonstration only
