import json
from datetime import datetime

import streamlit as st

from utils.openrouter import OPENROUTER_FREE_MODELS


def settings():
    st.header("Settings")
    st.caption("Configure NexusRAG settings and AI provider integrations")

    st.subheader("Chat")
    chat_settings = st.container(border=True)
    with chat_settings:
        provider = st.selectbox(
            "LLM Provider",
            ["Google Gemini", "OpenRouter (Free Models)"],
            key="llm_provider",
            help="Select which AI provider to use for chat and reasoning.",
        )
        if not provider:
            provider = st.session_state.get("llm_provider", "Google Gemini")
        if provider == "Google Gemini":
            st.text_input(
                "Gemini API Key",
                key="gemini_api_key",
                type="password",
                help="Google Gemini API key for high-speed cloud reasoning.",
            )
            st.selectbox(
                "Chat Model",
                st.session_state.get(
                    "gemini_models",
                    ["gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.5-flash", "gemini-flash-latest"],
                ),
                key="gemini_model",
                help="Select which Gemini model to use for chat.",
            )
            st.caption("Powered by Google Gemini GenAI.")
        else:
            st.text_input(
                "OpenRouter API Key",
                key="openrouter_api_key",
                type="password",
                help="OpenRouter API key for free community models.",
            )
            st.selectbox(
                "Chat Model (Free Models Only)",
                st.session_state.get(
                    "openrouter_models",
                    OPENROUTER_FREE_MODELS,
                ),
                key="openrouter_model",
                help="Select which OpenRouter free model to use for chat.",
            )
            st.caption("Powered by OpenRouter (Exclusively Free Tier Models).")

        if st.session_state.get("advanced") is True:
            st.select_slider(
                "Top K",
                options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                help="The number of most similar documents to retrieve in response to a query.",
                value=st.session_state["top_k"],
                key="top_k",
            )
            st.selectbox(
                "Chat Mode",
                (
                    "compact",
                    "refine",
                    "tree_summarize",
                    "simple_summarize",
                    "accumulate",
                    "compact_accumulate",
                ),
                help="Sets the Query Engine response mode. Default: `compact`.",
                key="chat_mode",
                disabled=True,
            )
            st.write("")

    st.subheader(
        "Embeddings",
        help="Embeddings are numerical representations of data, useful for tasks like document clustering and similarity detection when processing files.",
    )
    embedding_settings = st.container(border=True)
    with embedding_settings:
        embedding_backend = st.selectbox(
            "Backend",
            ["Gemini", "OpenRouter"],
            key="embedding_backend",
        )
        if embedding_backend == "Gemini":
            st.selectbox(
                "Embedding Model",
                st.session_state.get(
                    "gemini_embedding_models",
                    ["models/gemini-embedding-2", "models/gemini-embedding-001"],
                ),
                key="gemini_embedding_model",
            )
            st.caption("Google Gemini 3072-dimension cloud embeddings with automatic backoff and rate-limit recovery.")
        else:
            from utils.openrouter import OPENROUTER_EMBEDDING_MODELS
            st.selectbox(
                "Embedding Model",
                st.session_state.get("openrouter_embedding_models", OPENROUTER_EMBEDDING_MODELS),
                key="openrouter_embedding_model",
            )
            st.caption("OpenRouter API cloud embeddings (BGE Large/Base, OpenAI, Gemini). Uses your configured OpenRouter API Key.")

        if st.session_state.get("advanced") is True:
            st.session_state["chunk_size"] = str(st.session_state["chunk_size"])
            st.session_state["chunk_overlap"] = str(st.session_state["chunk_overlap"])
            st.text_input(
                "Chunk Size",
                max_chars=4,
                placeholder="1024",
                help="Reducing `chunk_size` improves embedding precision by focusing on smaller text portions.",
                key="chunk_size",
                value=st.session_state["chunk_size"],
            )
            st.text_input(
                "Chunk Overlap",
                max_chars=4,
                placeholder="200",
                help="The amount of overlap between two consecutive chunks.",
                key="chunk_overlap",
                value=st.session_state["chunk_overlap"],
            )

    st.subheader("Export Data")
    export_data_settings = st.container(border=True)
    with export_data_settings:
        st.write("Chat History")
        st.download_button(
            label="Download",
            data=json.dumps(st.session_state["messages"]),
            file_name=f"nexusrag-chat-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json",
            mime="application/json",
        )

    st.toggle("Advanced Settings", key="advanced", value=st.session_state.get("advanced", False))

    if st.session_state.get("advanced") is True:
        with st.expander("Diagnostics"):
            st.json(sanitized_diagnostics(st.session_state))


def sanitized_diagnostics(state):
    """Expose status only, without document content, prompts, URLs, or paths."""
    return {
        "documents_loaded": bool(state.get("documents")),
        "llm_ready": state.get("llm") is not None,
        "index_ready": state.get("query_engine") is not None,
    }
