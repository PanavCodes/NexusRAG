import os
import re
import time
import streamlit as st
import utils.logs as logs
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

DEFAULT_GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

GEMINI_CHAT_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash",
    "gemini-flash-latest",
]
DEFAULT_GEMINI_CHAT_MODEL = "gemini-3.5-flash-lite"

GEMINI_EMBEDDING_MODELS = [
    "models/gemini-embedding-2",
    "models/gemini-embedding-001",
]
DEFAULT_GEMINI_EMBEDDING_MODEL = "models/gemini-embedding-2"


def get_gemini_api_key() -> str:
    """Retrieve Gemini API key from session state, environment, or default."""
    if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
        return st.session_state["gemini_api_key"]
    return os.environ.get("GEMINI_API_KEY", DEFAULT_GEMINI_API_KEY)


def extract_retry_delay(err: Exception | str) -> float:
    """Extract retry delay seconds from Google GenAI 429 error, adding a 1.0s safety buffer."""
    text = str(err)
    m_json = re.search(r'''["']retryDelay["']\s*:\s*["']([0-9]+(?:\.[0-9]+)?)s?["']''', text)
    if m_json:
        return float(m_json.group(1)) + 1.0
    m_text = re.search(r'''retry\s+(?:in|after)?\s*([0-9]+(?:\.[0-9]+)?)\s*s''', text, re.IGNORECASE)
    if m_text:
        return float(m_text.group(1)) + 1.0
    return 25.0


class ResilientGeminiEmbedding(GoogleGenAIEmbedding):
    """
    GoogleGenAIEmbedding with automated rate-limit recovery for Gemini Free Tier (30,000 TPM limit).
    Catches 429 RESOURCE_EXHAUSTED, extracts the server retryDelay, and automatically retries.
    """

    def _embed_texts(self, texts, task_type=None):
        max_attempts = 6
        for attempt in range(1, max_attempts + 1):
            try:
                return super()._embed_texts(texts, task_type=task_type)
            except Exception as err:
                err_str = str(err)
                is_quota_err = (
                    "429" in err_str
                    or "RESOURCE_EXHAUSTED" in err_str
                    or "quota" in err_str.lower()
                )
                if is_quota_err and attempt < max_attempts:
                    delay = extract_retry_delay(err)
                    logs.log.warning(
                        f"Gemini Free Tier rate limit reached (30k tokens/min). "
                        f"Waiting {delay:.1f}s for quota to refresh (attempt {attempt}/{max_attempts})..."
                    )
                    try:
                        st.toast(
                            f"Gemini 30k tokens/min quota limit reached. Pausing {int(delay)}s to refresh quota...",
                            icon="⏳",
                        )
                    except Exception:
                        pass
                    time.sleep(delay)
                else:
                    if is_quota_err:
                        logs.log.error(
                            "Gemini Free Tier 30k tokens/min quota exhausted after multiple retries. "
                            "Please wait a moment and retry, or select OpenRouter embeddings in Settings."
                        )
                        raise ValueError(
                            "Gemini Free Tier embedding quota exceeded (30,000 tokens/min limit). "
                            "Please wait a moment and retry, or select OpenRouter embeddings in Settings "
                            "for unlimited, free, and fast local indexing without API quotas."
                        ) from err
                    raise


def create_gemini_llm(
    model: str = DEFAULT_GEMINI_CHAT_MODEL,
    api_key: str | None = None,
    system_prompt: str | None = None,
) -> GoogleGenAI:
    """Create a GoogleGenAI LLM instance configured with Gemini API."""
    key = api_key or get_gemini_api_key()
    if not key:
        raise ValueError("Gemini API key is required. Please configure it in Settings or set GEMINI_API_KEY.")

    kwargs = {
        "model": model,
        "api_key": key,
    }
    if system_prompt:
        kwargs["system_prompt"] = system_prompt

    logs.log.info(f"Creating Gemini LLM instance (model: {model})")
    return GoogleGenAI(**kwargs)


def create_gemini_embedding(
    model_name: str = DEFAULT_GEMINI_EMBEDDING_MODEL,
    api_key: str | None = None,
    embed_batch_size: int = 4,
) -> ResilientGeminiEmbedding:
    """Create a ResilientGeminiEmbedding instance configured with Gemini API and rate-limit safety."""
    key = api_key or get_gemini_api_key()
    if not key:
        raise ValueError("Gemini API key is required for Gemini embeddings.")

    logs.log.info(f"Creating Resilient Gemini Embedding instance (model: {model_name}, batch_size: {embed_batch_size})")
    return ResilientGeminiEmbedding(
        model_name=model_name,
        api_key=key,
        embed_batch_size=embed_batch_size,
    )


def context_chat(prompt: str, query_engine):
    """Initiates a chat with context using the Llama-Index query_engine."""
    try:
        stream = query_engine.query(prompt)
        if hasattr(stream, "response_gen") and stream.response_gen is not None:
            for text in stream.response_gen:
                yield str(text)
        elif hasattr(stream, "response") and stream.response is not None:
            yield str(stream.response)
        else:
            yield str(stream)
    except Exception as err:
        logs.log.error(f"Gemini chat stream error: {err}")
        raise
