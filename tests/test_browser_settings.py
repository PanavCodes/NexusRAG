import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from utils.browser_settings import (
    apply_persisted_settings,
    browser_storage_payload,
    deserialize_persisted_settings,
    persist_settings_to_browser_storage,
    restore_settings_from_browser_storage,
    serialize_persisted_settings,
)


class BrowserSettingsTests(unittest.TestCase):
    def test_apply_persisted_settings_updates_supported_keys(self):
        state = {}
        apply_persisted_settings(
            state,
            {
                "top_k": "5",
                "chunk_size": "2048",
                "chunk_overlap": "256",
                "advanced": "true",
                "llm_provider": "Google Gemini",
                "embedding_backend": "OpenRouter",
            },
        )

        self.assertEqual(state["top_k"], 5)
        self.assertEqual(state["chunk_size"], 2048)
        self.assertEqual(state["chunk_overlap"], 256)
        self.assertTrue(state["advanced"])
        self.assertEqual(state["llm_provider"], "Google Gemini")
        self.assertEqual(state["embedding_backend"], "OpenRouter")

    def test_apply_persisted_settings_ignores_invalid_values(self):
        state = {}
        apply_persisted_settings(state, {"top_k": "not-a-number", "advanced": "maybe"})

        self.assertNotIn("top_k", state)
        self.assertNotIn("advanced", state)

    def test_serialize_persisted_settings_only_includes_supported_keys(self):
        payload = serialize_persisted_settings(
            {
                "llm_provider": "Google Gemini",
                "top_k": 4,
                "messages": ["do not persist"],
            }
        )

        self.assertEqual(
            payload,
            {
                "llm_provider": "Google Gemini",
                "top_k": 4,
            },
        )

    def test_deserialize_persisted_settings_requires_json_object(self):
        self.assertEqual(deserialize_persisted_settings("not-json"), {})
        self.assertEqual(deserialize_persisted_settings("[1, 2, 3]"), {})

    def test_browser_storage_payload_writes_json_for_local_storage(self):
        payload = browser_storage_payload({"advanced": True, "top_k": 4})

        self.assertEqual(deserialize_persisted_settings(payload)["top_k"], 4)
        self.assertIn('"advanced": true', payload)
        self.assertNotIn("query_params", payload)

    def test_restore_hydrates_settings_from_browser_storage(self):
        state = {}
        stored_settings = browser_storage_payload(
            {
                "llm_provider": "OpenRouter (Free Models)",
                "selected_model": "cohere/north-mini-code:free",
                "embedding_backend": "OpenRouter",
                "openrouter_embedding_model": "baai/bge-large-en-v1.5",
            }
        )
        storage_component = Mock(return_value={"value": stored_settings})

        with patch("utils.browser_settings.st", SimpleNamespace(session_state=state)), patch(
            "utils.browser_settings._browser_storage_component", storage_component
        ):
            restore_settings_from_browser_storage()

        self.assertTrue(state["browser_settings_restored"])
        self.assertEqual(state["llm_provider"], "OpenRouter (Free Models)")
        self.assertEqual(state["selected_model"], "cohere/north-mini-code:free")
        self.assertEqual(state["embedding_backend"], "OpenRouter")
        self.assertEqual(state["openrouter_embedding_model"], "baai/bge-large-en-v1.5")

    def test_persist_writes_model_settings_after_restore(self):
        state = {
            "browser_settings_restored": True,
            "llm_provider": "Google Gemini",
            "selected_model": "gemini-3.5-flash-lite",
            "embedding_backend": "Gemini",
            "gemini_embedding_model": "models/gemini-embedding-2",
            "messages": ["do not persist"],
        }
        storage_component = Mock()

        with patch("utils.browser_settings.st", SimpleNamespace(session_state=state)), patch(
            "utils.browser_settings._browser_storage_component", storage_component
        ):
            persist_settings_to_browser_storage()

        storage_component.assert_called_once()
        persisted_payload = storage_component.call_args.kwargs["value"]
        persisted_settings = deserialize_persisted_settings(persisted_payload)
        self.assertEqual(
            persisted_settings,
            {
                "llm_provider": "Google Gemini",
                "embedding_backend": "Gemini",
                "gemini_embedding_model": "models/gemini-embedding-2",
                "selected_model": "gemini-3.5-flash-lite",
            },
        )

    def test_persist_skips_redundant_component_write_for_same_settings(self):
        state = {
            "browser_settings_restored": True,
            "llm_provider": "Google Gemini",
            "selected_model": "gemini-3.5-flash-lite",
        }
        storage_component = Mock()

        with patch("utils.browser_settings.st", SimpleNamespace(session_state=state)), patch(
            "utils.browser_settings._browser_storage_component", storage_component
        ):
            persist_settings_to_browser_storage()
            persist_settings_to_browser_storage()

        storage_component.assert_called_once()

    def test_browser_storage_set_action_does_not_emit_component_value(self):
        component_html = (
            Path(__file__).resolve().parents[1]
            / "utils"
            / "browser_storage_component"
            / "index.html"
        ).read_text(encoding="utf-8")

        set_branch = component_html.split('if (args.action === "set") {', 1)[1]
        set_branch = set_branch.split("}", 1)[0]

        self.assertIn("localStorage.setItem", set_branch)
        self.assertNotIn("sendDataToPython", set_branch)

    def test_restore_stops_until_browser_local_storage_payload_is_available(self):
        state = {}
        storage_component = Mock(return_value=None)
        streamlit = SimpleNamespace(session_state=state, stop=Mock(side_effect=RuntimeError("stopped")))

        with patch("utils.browser_settings.st", streamlit), patch(
            "utils.browser_settings._browser_storage_component", storage_component
        ):
            with self.assertRaisesRegex(RuntimeError, "stopped"):
                restore_settings_from_browser_storage()

        streamlit.stop.assert_called_once()
        self.assertNotIn("browser_settings_restored", state)

    def test_persist_does_not_write_local_storage_before_browser_restore(self):
        state = {
            "llm_provider": "Google Gemini",
            "selected_model": "gemini-3.5-flash-lite",
        }
        storage_component = Mock()

        with patch("utils.browser_settings.st", SimpleNamespace(session_state=state)), patch(
            "utils.browser_settings._browser_storage_component", storage_component
        ):
            persist_settings_to_browser_storage()

        storage_component.assert_not_called()


if __name__ == "__main__":
    unittest.main()
