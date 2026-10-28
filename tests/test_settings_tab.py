import unittest
from types import SimpleNamespace
from unittest.mock import patch

from components.tabs import settings as settings_tab


class _Container:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


class _StreamlitStub:
    def __init__(self, state):
        self.session_state = state
        self.selectbox_calls = []

    def header(self, *args, **kwargs):
        pass

    def caption(self, *args, **kwargs):
        pass

    def subheader(self, *args, **kwargs):
        pass

    def container(self, *args, **kwargs):
        return _Container()

    def text_input(self, *args, **kwargs):
        pass

    def selectbox(self, label, options, **kwargs):
        self.selectbox_calls.append((label, kwargs))
        return self.session_state.get(kwargs.get("key"))

    def button(self, *args, **kwargs):
        pass

    def toggle(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def download_button(self, *args, **kwargs):
        pass


class SettingsTabTests(unittest.TestCase):
    def test_gemini_settings_render(self):
        state = {
            "advanced": False,
            "llm_provider": "Google Gemini",
            "gemini_api_key": "test-key",
            "gemini_models": ["gemini-3.5-flash-lite"],
            "gemini_model": "gemini-3.5-flash-lite",
            "embedding_backend": "Gemini",
            "gemini_embedding_models": ["models/gemini-embedding-2"],
            "gemini_embedding_model": "models/gemini-embedding-2",
            "messages": [],
        }
        streamlit = _StreamlitStub(state)

        with patch("components.tabs.settings.st", streamlit):
            settings_tab.settings()

        keyed_selectboxes = {
            kwargs["key"]: kwargs
            for _, kwargs in streamlit.selectbox_calls
            if "key" in kwargs
        }
        self.assertIn("gemini_model", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["gemini_model"])
        self.assertIn("embedding_backend", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["embedding_backend"])
        self.assertIn("gemini_embedding_model", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["gemini_embedding_model"])

    def test_openrouter_embedding_settings_render(self):
        state = {
            "advanced": False,
            "llm_provider": "Google Gemini",
            "gemini_api_key": "test-key",
            "gemini_models": ["gemini-3.5-flash-lite"],
            "gemini_model": "gemini-3.5-flash-lite",
            "embedding_backend": "OpenRouter",
            "openrouter_embedding_models": ["baai/bge-large-en-v1.5"],
            "openrouter_embedding_model": "baai/bge-large-en-v1.5",
            "messages": [],
        }
        streamlit = _StreamlitStub(state)

        with patch("components.tabs.settings.st", streamlit):
            settings_tab.settings()

        keyed_selectboxes = {
            kwargs["key"]: kwargs
            for _, kwargs in streamlit.selectbox_calls
            if "key" in kwargs
        }
        self.assertIn("openrouter_embedding_model", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["openrouter_embedding_model"])


    def test_openrouter_settings_render(self):
        state = {
            "advanced": False,
            "llm_provider": "OpenRouter (Free Models)",
            "openrouter_api_key": "test-or-key",
            "openrouter_models": ["liquid/lfm-2.5-2.6b:free", "google/gemma-4-31b-it:free"],
            "openrouter_model": "liquid/lfm-2.5-2.6b:free",
            "embedding_backend": "Gemini",
            "gemini_embedding_models": ["models/gemini-embedding-2"],
            "gemini_embedding_model": "models/gemini-embedding-2",
            "messages": [],
        }
        streamlit = _StreamlitStub(state)

        with patch("components.tabs.settings.st", streamlit):
            settings_tab.settings()

        keyed_selectboxes = {
            kwargs["key"]: kwargs
            for _, kwargs in streamlit.selectbox_calls
            if "key" in kwargs
        }
        self.assertIn("llm_provider", keyed_selectboxes)
        self.assertIn("openrouter_model", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["openrouter_model"])



    def test_openrouter_embedding_settings_render(self):
        state = {
            "advanced": False,
            "llm_provider": "OpenRouter (Free Models)",
            "openrouter_api_key": "test-key",
            "openrouter_models": ["cohere/north-mini-code:free"],
            "openrouter_model": "cohere/north-mini-code:free",
            "embedding_backend": "OpenRouter",
            "openrouter_embedding_models": ["baai/bge-large-en-v1.5", "text-embedding-3-small"],
            "openrouter_embedding_model": "baai/bge-large-en-v1.5",
            "messages": [],
        }
        streamlit = _StreamlitStub(state)

        with patch("components.tabs.settings.st", streamlit):
            settings_tab.settings()

        keyed_selectboxes = {
            kwargs["key"]: kwargs
            for _, kwargs in streamlit.selectbox_calls
            if "key" in kwargs
        }
        self.assertIn("embedding_backend", keyed_selectboxes)
        self.assertIn("openrouter_embedding_model", keyed_selectboxes)
        self.assertNotIn("index", keyed_selectboxes["openrouter_embedding_model"])

if __name__ == "__main__":
    unittest.main()
