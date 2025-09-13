


import streamlit as st
import openai
from rag_retriever import get_relevant_chunks
import importlib.util
import pathlib
import random

st.set_page_config(page_title="World Falls Guidelines", layout="wide")

# --- Sidebar: API Key and Parameters ---




# Load API key from config.py
config_path = pathlib.Path(__file__).parent / "config.py"
spec = importlib.util.spec_from_file_location("config", str(config_path))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

st.sidebar.title("OpenAI API Settings")
config_api_key = getattr(config, "OPENAI_API_KEY", "")

if config_api_key:
    st.sidebar.text_input(
        "OpenAI API Key (from config.py)",
        type="password",
        value=config_api_key,
        disabled=True,
        help="This key is set in config.py and cannot be edited here."
    )
    st.session_state.api_key = config_api_key
else:
    st.sidebar.warning(
        "No OpenAI API key found. Please set OPENAI_API_KEY in config.py. "
        "[Get one here](https://platform.openai.com/account/api-keys)"
    )
    st.session_state.api_key = ""




st.sidebar.title("LLM Parameters")
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, float(st.session_state.temperature))
st.session_state.temperature = temperature

if "top_p" not in st.session_state:
    st.session_state.top_p = 1.0
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, float(st.session_state.top_p))
st.session_state.top_p = top_p

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 512
max_tokens = st.sidebar.number_input("Max tokens", 64, 4096, int(st.session_state.max_tokens))
st.session_state.max_tokens = max_tokens

if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
model = st.sidebar.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"], index=0 if st.session_state.model=="gpt-3.5-turbo" else 1)
st.session_state.model = model



st.sidebar.title("RAG Parameters")
if "top_k" not in st.session_state:
    st.session_state.top_k = 3
top_k = st.sidebar.slider("Top-K Chunks", 1, 10, int(st.session_state.top_k))
st.session_state.top_k = top_k

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Main UI ---

st.title("World Falls Guidelines")

st.session_state.history = []  # Ensure history is initialized
# Show a random sample question as a hint
sample_qa = getattr(config, "SAMPLE_QA", [])
sample_question = None
if sample_qa:
    sample_question = random.choice(sample_qa)["question"]
    st.info(f"💡 Example question you can ask: '{sample_question}'")

user_input = st.text_input("Ask a question:", key="user_input")



if st.button("Send") and user_input:
    # RAG retrieval
    chunks = get_relevant_chunks(user_input, top_k=top_k)
    context = "\n\n".join([c["metadata"].get("text", "") for c in chunks])
    sources = [c["metadata"].get("source_path", "") for c in chunks]

    # Use system prompt and messages from config
    system_prompt = getattr(config, "SYSTEM_PROMPT", "")
    get_messages = getattr(config, "get_messages", None)
    if get_messages:
        messages = get_messages(context, user_input)
    else:
        # fallback
        messages = [
            {"role": "system", "content": system_prompt.format(context=context)},
            {"role": "user", "content": f"Question: {user_input}\nAnswer:"}
        ]

    if not st.session_state.api_key:
        answer = "[OpenAI API key required to generate LLM answer. RAG retrieval completed. Please set your API key in config.py.]"
    else:
        # LLM call (OpenAI v1+ API)
        try:
            client = openai.OpenAI(api_key=st.session_state.api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error: {e}"

    # Update history, now also store the context for display
    st.session_state.history.append({
        "user": user_input,
        "answer": answer,
        "sources": sources,
        "context": context
    })

# --- Display Chat History ---

for entry in st.session_state.history:
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Bot:** {entry['answer']}")
    if entry["sources"]:
        st.markdown("**Sources:**")
        for src in entry["sources"]:
            st.code(src)
    if "context" in entry and entry["context"]:
        with st.expander("Show context sent to LLM", expanded=False):
            st.write(entry["context"])
    st.markdown("---")

if st.button("Clear History"):
    st.session_state.history = []
    st.rerun()
