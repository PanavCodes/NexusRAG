
def default_chat_model(models):
    preferred_models = ('gemma4:latest', 'llama3:latest')
    for model in preferred_models:
        if model in models:
            return model
    if models:
        return models[0]
    return DEFAULT_GEMINI_CHAT_MODEL
import streamlit as st
from utils.gemini import (
    GEMINI_CHAT_MODELS,
    GEMINI_EMBEDDING_MODELS,
    DEFAULT_GEMINI_CHAT_MODEL,
    DEFAULT_GEMINI_EMBEDDING_MODEL,
    get_gemini_api_key,
)
from utils.openrouter import (
    OPENROUTER_FREE_MODELS,
    DEFAULT_OPENROUTER_MODEL,
    OPENROUTER_EMBEDDING_MODELS,
    DEFAULT_OPENROUTER_EMBEDDING_MODEL,
    get_openrouter_api_key,
)
from utils.browser_settings import (
    restore_settings_from_browser_storage,
)


def ensure_valid_model_selections(state):
    """Keep selected model values consistent with available model lists."""
    provider = state.get("llm_provider", "Google Gemini")
    if provider == "OpenRouter (Free Models)":
        o_models = state.get("openrouter_models", OPENROUTER_FREE_MODELS)
        if state.get("openrouter_model") not in o_models and o_models:
            state["openrouter_model"] = o_models[0]
        state["selected_model"] = state.get("openrouter_model", DEFAULT_OPENROUTER_MODEL)
    else:
        g_models = state.get("gemini_models", GEMINI_CHAT_MODELS)
        if state.get("gemini_model") not in g_models:
            state["gemini_model"] = DEFAULT_GEMINI_CHAT_MODEL
        state["selected_model"] = state.get("gemini_model", DEFAULT_GEMINI_CHAT_MODEL)

    if state.get("embedding_backend") == "Gemini":
        ge_models = state.get("gemini_embedding_models", GEMINI_EMBEDDING_MODELS)
        if state.get("gemini_embedding_model") not in ge_models:
            state["gemini_embedding_model"] = DEFAULT_GEMINI_EMBEDDING_MODEL
    elif state.get("embedding_backend") == "OpenRouter":
        oe_models = state.get("openrouter_embedding_models", OPENROUTER_EMBEDDING_MODELS)
        if state.get("openrouter_embedding_model") not in oe_models:
            state["openrouter_embedding_model"] = DEFAULT_OPENROUTER_EMBEDDING_MODEL


def set_initial_state():
    restore_settings_from_browser_storage()

    ###########
    # General #
    ###########

    if "sidebar_state" not in st.session_state:
        st.session_state["sidebar_state"] = "expanded"

    if "llm_provider" not in st.session_state:
        st.session_state["llm_provider"] = "Google Gemini"

    if "gemini_api_key" not in st.session_state:
        st.session_state["gemini_api_key"] = get_gemini_api_key()

    if "gemini_models" not in st.session_state:
        st.session_state["gemini_models"] = list(GEMINI_CHAT_MODELS)

    if "gemini_model" not in st.session_state:
        st.session_state["gemini_model"] = DEFAULT_GEMINI_CHAT_MODEL

    if "openrouter_api_key" not in st.session_state:
        st.session_state["openrouter_api_key"] = get_openrouter_api_key()

    if "openrouter_models" not in st.session_state:
        st.session_state["openrouter_models"] = list(OPENROUTER_FREE_MODELS)

    if "openrouter_model" not in st.session_state:
        st.session_state["openrouter_model"] = DEFAULT_OPENROUTER_MODEL

    if "selected_model" not in st.session_state:
        st.session_state["selected_model"] = st.session_state["gemini_model"]

    if "embedding_backend" not in st.session_state:
        st.session_state["embedding_backend"] = "OpenRouter"

    if "gemini_embedding_models" not in st.session_state:
        st.session_state["gemini_embedding_models"] = list(GEMINI_EMBEDDING_MODELS)

    if "gemini_embedding_model" not in st.session_state:
        st.session_state["gemini_embedding_model"] = DEFAULT_GEMINI_EMBEDDING_MODEL

    if "openrouter_embedding_models" not in st.session_state:
        st.session_state["openrouter_embedding_models"] = list(OPENROUTER_EMBEDDING_MODELS)

    if "openrouter_embedding_model" not in st.session_state:
        st.session_state["openrouter_embedding_model"] = DEFAULT_OPENROUTER_EMBEDDING_MODEL


    ensure_valid_model_selections(st.session_state)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "Welcome to NexusRAG! Connect a GitHub repository, upload documents (PDF, Word, Excel .xlsx/.xls, PowerPoint, etc.), or input a website to begin intelligent retrieval-augmented analysis.",
            }
        ]

    ################################
    #  Files, Documents & Websites #
    ################################

    if "processed_file_signature" not in st.session_state:
        st.session_state["processed_file_signature"] = None

    if "processing_file_signature" not in st.session_state:
        st.session_state["processing_file_signature"] = None

    if "file_ingestion_error_signature" not in st.session_state:
        st.session_state["file_ingestion_error_signature"] = None

    if "documents" not in st.session_state:
        st.session_state["documents"] = None

    if "file_ingestion_stages" not in st.session_state:
        st.session_state["file_ingestion_stages"] = []

    if "github_repo" not in st.session_state:
        st.session_state["github_repo"] = ""

    if "processed_github_repo" not in st.session_state:
        st.session_state["processed_github_repo"] = None

    if "github_ingestion_stages" not in st.session_state:
        st.session_state["github_ingestion_stages"] = []

    if "websites" not in st.session_state:
        st.session_state["websites"] = []

    if "website_ingestion_stages" not in st.session_state:
        st.session_state["website_ingestion_stages"] = []

    if "active_source" not in st.session_state:
        st.session_state["active_source"] = None

    if "query_engine" not in st.session_state:
        st.session_state["query_engine"] = None

    if "chat_history_cleared" not in st.session_state:
        st.session_state["chat_history_cleared"] = False

    ############
    # Settings #
    ############

    if "top_k" not in st.session_state:
        st.session_state["top_k"] = 3

    if "chat_mode" not in st.session_state:
        st.session_state["chat_mode"] = "compact"

    if "chunk_size" not in st.session_state:
        st.session_state["chunk_size"] = 1024

    if "chunk_overlap" not in st.session_state:
        st.session_state["chunk_overlap"] = 200

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = ""
