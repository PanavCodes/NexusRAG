"""Security regression tests with local fixtures and mocked network calls."""

from contextlib import nullcontext
import os
import inspect
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, Mock, patch
from zipfile import ZipFile

from llama_index.core import Document
from llama_index.core.embeddings import MockEmbedding
from llama_index.core.llms import MockLLM

from components.tabs import github_repo, settings
from utils import browser_settings, helpers, llama_index, rag_pipeline
from utils.settings_validation import validate_chunk_settings


class StopSignal(BaseException):
    pass


def state():
    return {
        "selected_model": "gemini-3.5-flash-lite",
        "gemini_api_key": "fixture-key",
        "llm_provider": "Google Gemini",
        "system_prompt": "",
        "embedding_backend": "Gemini",
        "embedding_model": "Default (gte-modernbert-base)",
        "gemini_embedding_model": "models/gemini-embedding-2",
        "chunk_size": 1024,
        "chunk_overlap": 200,
        "top_k": 3,
        "chat_mode": "compact",
    }

class SettingsBoundaryTests(unittest.TestCase):
    def test_chunk_limits_and_ordinary_settings(self):
        self.assertEqual(validate_chunk_settings("1024", "200"), (1024, 200))
        self.assertEqual(validate_chunk_settings(8192, 2048), (8192, 2048))
        for size, overlap in [
            (255, 0),
            (8193, 0),
            (256, 129),
            (1024, -1),
            (True, 0),
            ("123456", 0),
        ]:
            with self.subTest(size=size, overlap=overlap), self.assertRaises(
                ValueError
            ):
                validate_chunk_settings(size, overlap)

    def test_restored_options_cannot_bypass_validation(self):
        restored = {}
        browser_settings.apply_persisted_settings(
            restored,
            {
                "embedding_backend": "unsupported",
                "embedding_model": "Other",
                "chat_mode": "unsupported",
                "top_k": 99,
                "chunk_size": 256,
                "chunk_overlap": 200,
            },
        )
        self.assertEqual(restored, {
            "chunk_size": 1024, "chunk_overlap": 200,
            "embedding_model": "Other",
        })

    def test_diagnostics_exclude_sensitive_values(self):
        diagnostic = settings.sanitized_diagnostics(
            {
                "documents": ["private document"],
                "messages": ["private prompt"],
                "api_endpoint": "private endpoint",
                "llm": object(),
                "query_engine": object(),
            }
        )
        self.assertEqual(
            diagnostic,
            {"documents_loaded": True, "llm_ready": True, "index_ready": True},
        )

    
class ArchiveBoundaryTests(unittest.TestCase):
    def test_small_archive_passes_and_limits_reject_before_reader(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "book.epub"
            with ZipFile(path, "w") as archive:
                archive.writestr("mimetype", "application/epub+zip")
                archive.writestr("chapter.txt", "A small chapter.")
            self.assertEqual(helpers.validated_document_paths(directory), [path])
            for limit in [
                "MAX_ARCHIVE_MEMBERS",
                "MAX_ARCHIVE_EXPANDED_BYTES",
                "MAX_ARCHIVE_MEMBER_BYTES",
            ]:
                with self.subTest(limit=limit), patch.object(
                    helpers, limit, 1
                ), patch.object(llama_index, "SimpleDirectoryReader") as reader:
                    with self.assertRaisesRegex(Exception, "archive"):
                        llama_index.load_documents(directory)
                    reader.assert_not_called()

    def test_symbolic_links_are_not_parsed(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "source.txt").write_text("Ordinary document")
            try:
                (Path(directory) / "alias.txt").symlink_to(Path(directory) / "source.txt")
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks not supported on this platform/privilege level")
            with self.assertRaisesRegex(ValueError, "Symbolic"):
                helpers.validated_document_paths(directory)


class ModelIsolationTests(unittest.TestCase):
    def setUp(self):
        session_patch = patch.object(llama_index.st, "session_state", state())
        session_patch.start()
        self.addCleanup(session_patch.stop)

    def test_two_query_engines_keep_their_own_models(self):
        first_embedding = MockEmbedding(embed_dim=4)
        second_embedding = MockEmbedding(embed_dim=8)
        first_llm, second_llm = MockLLM(), MockLLM()
        with patch.object(llama_index.st, "session_state", state()):
            first = llama_index.create_query_engine(
                [Document(text="First ordinary document.")],
                first_llm,
                first_embedding,
                1024,
                200,
            )
            second = llama_index.create_query_engine(
                [Document(text="Second ordinary document.")],
                second_llm,
                second_embedding,
                512,
                100,
            )
        self.assertIs(first._response_synthesizer._llm, first_llm)
        self.assertIs(second._response_synthesizer._llm, second_llm)
        self.assertIs(first.retriever._embed_model, first_embedding)
        self.assertIs(second.retriever._embed_model, second_embedding)
        self.assertTrue(str(first.query("What is the document about?")))

    def test_llm_creation_returns_independent_explicit_clients(self):
        from utils.gemini import create_gemini_llm
        from utils.openrouter import create_openrouter_llm

        with patch("google.genai.Client"), patch("openai.OpenAI"):
            llm1 = create_gemini_llm("gemini-3.5-flash-lite", "key1", "prompt 1")
            llm2 = create_openrouter_llm("cohere/north-mini-code:free", "key2", "prompt 2")
            self.assertIsNotNone(llm1)
            self.assertIsNotNone(llm2)
            self.assertIsNot(llm1, llm2)

    def test_cloud_embeddings_creation_returns_independent_clients(self):
        from utils.gemini import create_gemini_embedding
        from utils.openrouter import create_openrouter_embedding

        with patch("llama_index.embeddings.google_genai.GoogleGenAIEmbedding"), patch("llama_index.embeddings.openai.OpenAIEmbedding"):
            emb1 = create_gemini_embedding("models/gemini-embedding-2", "key1")
            emb2 = create_openrouter_embedding("baai/bge-large-en-v1.5", "key2")
            self.assertIsNotNone(emb1)
            self.assertIsNotNone(emb2)
            self.assertIsNot(emb1, emb2)



