import hashlib
import json
import os

import streamlit as st
import streamlit.components.v1 as components
from utils.settings_validation import (
    CHAT_MODES, bounded_integer, validate_chunk_settings,
)

PERSISTED_SETTING_TYPES = {
    "llm_provider": str,
    "openrouter_api_key": str,
    "openrouter_model": str,
    "gemini_api_key": str,
    "gemini_model": str,
    "gemini_embedding_model": str,
    "openrouter_embedding_model": str,
    "embedding_backend": str,
    "embedding_model": str,
    "other_embedding_model": str,
    "selected_model": str,
    "top_k": int,
    "chat_mode": str,
    "chunk_size": int,
    "chunk_overlap": int,
    "advanced": bool,
}
BROWSER_STORAGE_KEY = "nexusrag:settings"
PERSISTED_SETTINGS_HASH_STATE_KEY = "browser_settings_persisted_hash"
_COMPONENT_PATH = os.path.join(os.path.dirname(__file__), "browser_storage_component")
_browser_storage_component = components.declare_component(
    "browser_storage", path=_COMPONENT_PATH
)


def _coerce_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.lower()
        if normalized == "true":
            return True
        if normalized == "false":
            return False
    raise ValueError("invalid boolean")


def apply_persisted_settings(state, raw_settings):
    """Apply valid browser-persisted settings before defaults initialize."""
    for key, expected_type in PERSISTED_SETTING_TYPES.items():
        if key not in raw_settings:
            continue
        raw_value = raw_settings[key]
        try:
            if key in {"chunk_size", "chunk_overlap", "top_k"}:
                bounds = {"chunk_size": (256, 8192), "chunk_overlap": (0, 2048), "top_k": (1, 10)}
                value = bounded_integer(raw_value, *bounds[key], key)
            elif expected_type is bool:
                value = _coerce_bool(raw_value)
            else:
                if not isinstance(raw_value, str) or len(raw_value) > 256:
                    continue
                value = expected_type(raw_value)
            options = {
                "embedding_backend": {"Gemini", "OpenRouter"},
                "chat_mode": CHAT_MODES,
            }
            if key in options and value not in options[key]:
                continue
        except (TypeError, ValueError):
            continue
        state[key] = value

    try:
        validate_chunk_settings(state.get("chunk_size", 1024), state.get("chunk_overlap", 200))
    except ValueError:
        state["chunk_size"], state["chunk_overlap"] = 1024, 200


def serialize_persisted_settings(state):
    """Return only browser-persistable user settings from session state."""
    return {
        key: state[key]
        for key in PERSISTED_SETTING_TYPES
        if key in state
        and state[key] is not None
        and str(state[key]).strip() != ""
    }


def deserialize_persisted_settings(payload):
    """Return persisted settings from a browser localStorage JSON payload."""
    if not isinstance(payload, str) or not payload or len(payload) > 16384:
        return {}
    try:
        settings = json.loads(payload)
    except (TypeError, ValueError):
        return {}
    if not isinstance(settings, dict):
        return {}
    return settings


def browser_storage_payload(settings):
    """Return the JSON string stored in browser localStorage."""
    return json.dumps(settings)


def restore_settings_from_browser_storage():
    """Load browser settings once per session before widgets instantiate."""
    if st.session_state.get("browser_settings_restored"):
        return

    result = _browser_storage_component(
        action="get", storage_key=BROWSER_STORAGE_KEY, key="browser_storage_restore"
    )
    if result is None:
        st.stop()

    payload = result.get("value")
    settings = deserialize_persisted_settings(payload)
    apply_persisted_settings(st.session_state, settings)
    st.session_state[PERSISTED_SETTINGS_HASH_STATE_KEY] = hashlib.sha256(
        browser_storage_payload(serialize_persisted_settings(st.session_state)).encode("utf-8")
    ).hexdigest()
    st.session_state["browser_settings_restored"] = True


def persist_settings_to_browser_storage():
    """Persist settings to browser localStorage whenever they change."""
    if not st.session_state.get("browser_settings_restored"):
        return

    persisted_settings = serialize_persisted_settings(st.session_state)
    payload = browser_storage_payload(persisted_settings)
    current_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    if st.session_state.get(PERSISTED_SETTINGS_HASH_STATE_KEY) == current_hash:
        return

    st.session_state[PERSISTED_SETTINGS_HASH_STATE_KEY] = current_hash
    _browser_storage_component(
        action="set",
        storage_key=BROWSER_STORAGE_KEY,
        value=payload,
        key="browser_storage_persist",
    )
