import unittest
from unittest.mock import patch

from components.page_state import (
    default_chat_model,
    ensure_valid_model_selections,
    set_initial_state,
)


class PageStateTests(unittest.TestCase):
    def test_default_chat_model_selects_first_or_fallback(self):
        self.assertEqual(
            default_chat_model(["gemini-3.5-flash-lite", "gemini-flash-latest"]),
            "gemini-3.5-flash-lite",
        )

    def test_ensure_valid_model_selections_repairs_inconsistent_chat_model(self):
        state = {
            "llm_provider": "Google Gemini",
            "gemini_model": "missing:latest",
            "gemini_models": ["gemini-3.5-flash-lite"],
            "embedding_backend": "Gemini",
        }

        ensure_valid_model_selections(state)

        self.assertEqual(state["gemini_model"], "gemini-3.5-flash-lite")
        self.assertEqual(state["selected_model"], "gemini-3.5-flash-lite")

    def test_ensure_valid_model_selections_preserves_preferences_when_valid(self):
        state = {
            "llm_provider": "OpenRouter (Free Models)",
            "openrouter_model": "cohere/north-mini-code:free",
            "openrouter_models": ["cohere/north-mini-code:free", "deepseek/deepseek-r1:free"],
            "embedding_backend": "OpenRouter",
            "openrouter_embedding_model": "baai/bge-large-en-v1.5",
            "openrouter_embedding_models": ["baai/bge-large-en-v1.5"],
        }

        ensure_valid_model_selections(state)

        self.assertEqual(state["openrouter_model"], "cohere/north-mini-code:free")
        self.assertEqual(state["openrouter_embedding_model"], "baai/bge-large-en-v1.5")
        self.assertEqual(state["selected_model"], "cohere/north-mini-code:free")

    def test_initial_state_hydrates_from_browser_storage(self):
        state = {}

        def restore_from_local_storage():
            state.update(
                {
                    "browser_settings_restored": True,
                    "llm_provider": "Google Gemini",
                    "gemini_model": "gemini-3.5-flash-lite",
                    "embedding_backend": "Gemini",
                    "gemini_embedding_model": "models/gemini-embedding-2",
                }
            )

        with patch("components.page_state.st.session_state", state), patch(
            "components.page_state.restore_settings_from_browser_storage",
            side_effect=restore_from_local_storage,
        ):
            set_initial_state()

        self.assertEqual(state["llm_provider"], "Google Gemini")
        self.assertEqual(state["gemini_model"], "gemini-3.5-flash-lite")
        self.assertEqual(state["gemini_embedding_model"], "models/gemini-embedding-2")
        self.assertIn("Welcome to NexusRAG!", state["messages"][0]["content"])


if __name__ == "__main__":
    unittest.main()
