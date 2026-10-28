import unittest
from unittest.mock import patch

from components import ingestion_prerequisites


class IngestionPrerequisitesTests(unittest.TestCase):
    def test_openrouter_requires_valid_api_key_and_model(self):
        session = {
            "selected_model": "chat",
            "model_provider": "OpenRouter",
            "openrouter_api_key": "",
            "embedding_backend": "OpenRouter",
            "openrouter_embedding_model": "baai/bge-large-en-v1.5",
            "openrouter_embedding_models": ["baai/bge-large-en-v1.5"]
        }
        with patch.object(ingestion_prerequisites.st, "session_state", session):
            self.assertFalse(ingestion_prerequisites.ingestion_is_configured())
            session["openrouter_api_key"] = "test-key"
            self.assertTrue(ingestion_prerequisites.ingestion_is_configured())

    def test_retained_model_names_do_not_enable_import_without_discovery(self):
        session = {
            "selected_model": "chat",
            "gemini_models": [],
            "embedding_backend": "Gemini",
            "gemini_embedding_model": "embedding",
            "gemini_embedding_models": []
        }
        with patch.object(ingestion_prerequisites.st, "session_state", session):
            self.assertFalse(ingestion_prerequisites.ingestion_is_configured())


if __name__ == "__main__":
    unittest.main()
