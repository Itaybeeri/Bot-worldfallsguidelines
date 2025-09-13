# World Falls Guidelines ChatBot

A professional Streamlit chatbot for the World Falls Prevention Guidelines project, using Retrieval-Augmented Generation (RAG) with ChromaDB and OpenAI LLM. This chatbot answers questions strictly from the guidelines, with clear citations and a robust, user-friendly interface.

---

## 🚀 Quick Start

1. **Install dependencies**
   ```sh
   pip install -r ChatBot/requirements.txt
   ```
2. **Add your OpenAI API key**
   - Create a file named `openai_key.txt` in the `ChatBot` folder (next to `config.py`).
   - Paste your OpenAI API key (starts with `sk-...`) as the only line in that file.
   - This file is already in `.gitignore` and will NOT be committed.
3. **Run the chatbot**
   ```sh
   cd ChatBot
   streamlit run app.py
   ```
4. **Ask questions!**
   - Enter your question in the input box.
   - The chatbot will answer using only the World Falls Guidelines (with sources shown).
   - All previous Q&A are visible, with the latest at the top.
   - Use the sidebar to adjust model/parameters or clear chat history.

---

## Features

- Strict RAG: Answers only from the guidelines (with fallback disclaimer if not found)
- Conversational memory: Last X Q&A used as context
- Professional, persistent UI/UX (input clears after send, history always visible)
- Secure API key handling (never committed)
- Model selection (OpenAI GPT-3.5/4 only)
- Adjustable LLM and retrieval parameters in sidebar
- Source/citation display for every answer

---

## Notes

- Make sure your vector DB is built and available in `../RAG/data/vectordb/` (see `RAG/README.md` for pipeline setup)
- This is a demonstration project for the World Falls Guidelines
- For any issues, check your API key and vector DB paths

---

## Project Structure

- `ChatBot/app.py` — Streamlit chatbot UI and logic
- `ChatBot/config.py` — All configuration, prompts, and sample Q&A
- `ChatBot/requirements.txt` — Python dependencies
- `ChatBot/rag_retriever.py` — RAG retrieval logic (ChromaDB)
- `ChatBot/openai_key.txt` — Your API key (never committed)
- `RAG/` — Vector DB pipeline and data processing scripts

---

## Security

- **Never commit your OpenAI API key!** The chatbot loads it from `openai_key.txt`, which is gitignored.

---

## License

This project is for demonstration and educational use only.
