import os
import streamlit as st


def missing_ingestion_settings():
    """Return human-readable missing settings that block ingestion."""
    missing = []
    provider = st.session_state.get("llm_provider") or st.session_state.get("selected_provider")

    if provider in ("OpenRouter", "OpenRouter (Free Models)") or ("openrouter_api_key" in st.session_state and provider is None):
        api_key = st.session_state.get("openrouter_api_key") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            missing.append("a valid OpenRouter API Key")
        chat_model = st.session_state.get("openrouter_model") or st.session_state.get("selected_model")
        chat_models = st.session_state.get("openrouter_models")
        if not chat_model or (chat_models is not None and chat_model not in chat_models):
            missing.append("a valid OpenRouter model")
    elif provider in ("Google Gemini", "Gemini") or ("gemini_api_key" in st.session_state and provider is None):
        api_key = st.session_state.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            missing.append("a valid Gemini API Key")
        chat_model = st.session_state.get("gemini_model") or st.session_state.get("selected_model")
        chat_models = st.session_state.get("gemini_models")
        if not chat_model or (chat_models is not None and chat_model not in chat_models):
            missing.append("a valid Gemini chat model")
    else:
        # Fallback for generic or test-mocked providers
        chat_model = st.session_state.get("selected_model")
        chat_models = st.session_state.get("gemini_models")
        if not chat_model or (chat_models is not None and chat_model not in chat_models):
            missing.append("a valid chat model")

    backend = st.session_state.get("embedding_backend", "Gemini")
    if backend == "Gemini":
        if "gemini_api_key" in st.session_state and not (st.session_state.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")):
            missing.append("a valid Gemini API Key for embeddings")
        embedding_model = st.session_state.get("gemini_embedding_model") or st.session_state.get("embedding_model")
        embedding_models = st.session_state.get("gemini_embedding_models")
        if not embedding_model or (embedding_models is not None and embedding_model not in embedding_models):
            missing.append("a valid Gemini embedding model")
    elif backend == "OpenRouter":
        api_key = st.session_state.get("openrouter_api_key") or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            missing.append("a valid OpenRouter API Key for embeddings")
        embedding_model = st.session_state.get("openrouter_embedding_model") or st.session_state.get("embedding_model")
        embedding_models = st.session_state.get("openrouter_embedding_models")
        if not embedding_model or (embedding_models is not None and embedding_model not in embedding_models):
            missing.append("a valid OpenRouter embedding model")
    else:
        missing.append("a supported embedding backend")

    return missing


def ingestion_is_configured():
    """Return whether the app has the model settings required for ingestion."""
    return len(missing_ingestion_settings()) == 0


def render_ingestion_settings_warning():
    """Explain why ingestion is unavailable and where to fix it."""
    missing = missing_ingestion_settings()
    if not missing:
        return

    st.warning(
        "Before importing data, go to **Settings** and configure " + " and ".join(missing) + ".",
        icon="⚠️",
    )
