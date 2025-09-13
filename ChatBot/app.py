


import streamlit as st
import openai
from rag_retriever import get_relevant_chunks
import importlib.util
import pathlib
import random

st.set_page_config(page_title="World Falls Prevention Guidelines", layout="wide")

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
        "OpenAI API Key (from openai_key.txt)",
        type="password",
        value=config_api_key,
        disabled=True,
        help="This key is loaded from openai_key.txt and cannot be edited here."
    )
    st.session_state.api_key = config_api_key
else:
    st.sidebar.warning(
        "No OpenAI API key found. Please add your key to a file named 'openai_key.txt' in the ChatBot folder. "
        "This file should contain your OpenAI API key as the only line. "
        "[Get one here](https://platform.openai.com/account/api-keys)"
    )
    st.session_state.api_key = ""




st.sidebar.title("LLM Parameters")
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

temperature = st.sidebar.slider(
    "Temperature",
    0.0, 1.0, float(st.session_state.temperature),
    help="Controls randomness: higher values (e.g., 1.0) make answers more creative, lower values (e.g., 0.0) make them more focused and deterministic."
)
st.session_state.temperature = temperature

if "top_p" not in st.session_state:
    st.session_state.top_p = 1.0

top_p = st.sidebar.slider(
    "Top-p",
    0.0, 1.0, float(st.session_state.top_p),
    help="Controls diversity via nucleus sampling: 1.0 uses all words, lower values limit to most likely words. Usually leave at 1.0."
)
st.session_state.top_p = top_p

if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 512

max_tokens = st.sidebar.number_input(
    "Max tokens",
    64, 4096, int(st.session_state.max_tokens),
    help="Maximum length of the model's answer. Higher values allow longer answers but may use more credits."
)
st.session_state.max_tokens = max_tokens

if "model" not in st.session_state:
    st.session_state.model = "gpt-4"
model_list = ["gpt-3.5-turbo", "gpt-4"]
default_index = model_list.index(st.session_state.model) if st.session_state.model in model_list else 1

model = st.sidebar.selectbox(
    "Model",
    model_list,
    index=default_index,
    help="Choose which OpenAI model to use. GPT-4 is more advanced but may be slower or cost more."
)
st.session_state.model = model



st.sidebar.title("RAG Parameters")
if "top_k" not in st.session_state:
    st.session_state.top_k = 3

top_k = st.sidebar.slider(
    "Top-K Chunks",
    1, 10, int(st.session_state.top_k),
    help="How many document chunks to retrieve from the database for each question. Higher values may improve answer quality but can add noise."
)
st.session_state.top_k = top_k

# --- Session State ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Main UI ---

st.title("World Falls Guidelines")

# Show a random sample question as a hint
sample_qa = getattr(config, "SAMPLE_QA", [])
sample_question = None
if sample_qa:
    sample_question = random.choice(sample_qa)["question"]
    st.info(f"💡 Example question you can ask: '{sample_question}'")






# Use a separate session state variable for the input box
if "user_input_value" not in st.session_state:
    st.session_state.user_input_value = ""
user_input = st.text_input("Ask a question:", value=st.session_state.user_input_value, key="user_input_box")



send_clicked = st.button("Send")
if send_clicked and user_input:
    # RAG retrieval
    chunks = get_relevant_chunks(user_input, top_k=top_k)
    # Build context with source info for each chunk, source as bold label above paragraph
    context_chunks = []
    for c in chunks:
        src = c["metadata"].get("source_path", "Unknown source")
        txt = c["metadata"].get("text", "")
        context_chunks.append(f"**Source: {src}**\n\n{txt}")
    rag_context = "\n\n".join(context_chunks)
    sources = [c["metadata"].get("source_path", "") for c in chunks]


    # Build conversation history context (use config.MAX_HISTORY)
    max_history = getattr(config, "MAX_HISTORY", 5)
    history_context = ""
    if st.session_state.history:
        for entry in st.session_state.history[-max_history:]:
            history_context += f"User: {entry['user']}\nBot: {entry['answer']}\n"

    # Combine RAG context and conversation history
    full_context = history_context + ("\n" if history_context and rag_context else "") + rag_context

    # Use system prompt and messages from config
    system_prompt = getattr(config, "SYSTEM_PROMPT", "")
    get_messages = getattr(config, "get_messages", None)
    if get_messages:
        messages = get_messages(full_context, user_input)
    else:
        # fallback
        messages = [
            {"role": "system", "content": system_prompt.format(context=full_context)},
            {"role": "user", "content": f"Question: {user_input}\nAnswer:"}
        ]

    if not st.session_state.api_key:
        answer = "[OpenAI API key required to generate LLM answer. RAG retrieval completed. Please set your API key in config.py.]"
    else:
        # LLM call (OpenAI v1+ API)
        try:
            client = openai.OpenAI(api_key=st.session_state.api_key)
            completion_args = dict(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p=top_p,
            )
            if model == "gpt-5":
                completion_args["max_completion_tokens"] = max_tokens
            else:
                completion_args["max_tokens"] = max_tokens
            response = client.chat.completions.create(**completion_args)
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error: {e}"


    # Update history, now also store the context for display
    st.session_state.history.append({
        "user": user_input,
        "answer": answer,
        "sources": sources,
        "context": rag_context
    })

    # Clear the input box for the next question and rerun so answer is shown
    st.session_state.user_input_value = ""
    st.rerun()

# --- Display Chat History ---


# Show latest answer first (reverse order)
for entry in reversed(st.session_state.history):
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Bot:** {entry['answer']}")
    if "context" in entry and entry["context"]:
        with st.expander("Show context sent to LLM", expanded=False):
            st.write(entry["context"])
    st.markdown("---")


# Move Clear History button to sidebar
if st.sidebar.button("Clear Chat History"):
    st.session_state.history = []
    st.rerun()
