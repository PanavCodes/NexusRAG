import os
import json
import urllib.request
import streamlit as st
import utils.logs as logs
from llama_index.llms.openrouter import OpenRouter

DEFAULT_OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Curated list of verified FREE models on OpenRouter (exclusively :free models)
OPENROUTER_FREE_MODELS = [
    "liquid/lfm-2.5-2.6b:free",
    "cohere/north-mini-code:free",
    "google/gemma-4-31b-it:free",
    "google/gemma-4-26b-a4b-it:free",
    "nvidia/nemotron-3.5-lightning:free",
    "thinkingmachines/inkling:free",
    "thinkingmachines/inkling-small:free",
    "poolside/laguna-s-2.1:free",
    "poolside/laguna-xs-2.1:free",
    "recursive/flint-v1.0:free",
    "xingchen-agi/xing4.0-29b-a4b:free",
    "dots-studio/dots-3-note-preview:free",
]
DEFAULT_OPENROUTER_MODEL = "cohere/north-mini-code:free"


def get_openrouter_api_key() -> str:
    """Retrieve OpenRouter API key from session state, environment, or default."""
    if "openrouter_api_key" in st.session_state and st.session_state["openrouter_api_key"]:
        return st.session_state["openrouter_api_key"]
    return os.environ.get("OPENROUTER_API_KEY", DEFAULT_OPENROUTER_API_KEY)


def fetch_openrouter_free_models(api_key: str | None = None) -> list[str]:
    """Fetch all currently active :free models directly from OpenRouter API."""
    key = api_key or get_openrouter_api_key()
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"} if key else {},
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8")).get("data", [])
            free_models = [
                m["id"]
                for m in data
                if ":free" in m.get("id", "") or m.get("pricing", {}).get("prompt") == "0"
            ]
            if free_models:
                return free_models
    except Exception as err:
        logs.log.warning(f"Could not fetch dynamic OpenRouter model list: {err}")
    return list(OPENROUTER_FREE_MODELS)


def create_openrouter_llm(
    model: str = DEFAULT_OPENROUTER_MODEL,
    api_key: str | None = None,
    system_prompt: str | None = None,
) -> OpenRouter:
    """Create an OpenRouter LLM instance configured with OpenRouter API (only free models allowed)."""
    key = api_key or get_openrouter_api_key()
    if not key:
        raise ValueError("OpenRouter API key is required. Please configure it in Settings or set OPENROUTER_API_KEY.")

    # Strictly enforce only free models
    if not (model.endswith(":free") or ":free" in model):
        logs.log.warning(f"Model {model} is not a free model; defaulting to {DEFAULT_OPENROUTER_MODEL}")
        model = DEFAULT_OPENROUTER_MODEL

    kwargs = {
        "model": model,
        "api_key": key,
        "default_headers": {
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "NexusRAG",
        },
    }
    if system_prompt:
        kwargs["system_prompt"] = system_prompt

    logs.log.info(f"Creating OpenRouter LLM instance (model: {model})")
    return OpenRouter(**kwargs)


OPENROUTER_EMBEDDING_MODELS = [
    "baai/bge-large-en-v1.5",
    "baai/bge-base-en-v1.5",
    "text-embedding-3-small",
    "text-embedding-3-large",
    "google/gemini-embedding-001",
]
DEFAULT_OPENROUTER_EMBEDDING_MODEL = "baai/bge-large-en-v1.5"


def create_openrouter_embedding(
    model_name: str = DEFAULT_OPENROUTER_EMBEDDING_MODEL,
    api_key: str | None = None,
    embed_batch_size: int = 10,
):
    """Create an OpenRouter Embedding instance using OpenAI-compatible /v1/embeddings endpoint."""
    from llama_index.embeddings.openai import OpenAIEmbedding

    key = api_key or get_openrouter_api_key()
    if not key:
        raise ValueError("OpenRouter API key is required. Please configure it in Settings or set OPENROUTER_API_KEY.")

    logs.log.info(f"Creating OpenRouter Embedding instance (model: {model_name})")
    return OpenAIEmbedding(
        model_name=model_name,
        api_key=key,
        api_base="https://openrouter.ai/api/v1",
        embed_batch_size=embed_batch_size,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "NexusRAG",
        },
    )
