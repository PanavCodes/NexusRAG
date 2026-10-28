import os
from typing import Optional

import streamlit as st
from pydantic import Field

import utils.logs as logs
from utils.settings_validation import validate_chunk_settings
from utils.helpers import validated_document_paths

from llama_index.core.embeddings import BaseEmbedding
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from llama_index.core.ingestion import run_transformations
from llama_index.core.node_parser import SentenceSplitter

MAX_INDEX_NODES = 10000


class ProgressReportingEmbedding(BaseEmbedding):
    """Delegate embeddings while reporting progress for the full index build."""

    wrapped_model: BaseEmbedding
    progress_callback: object = Field(exclude=True)
    total_texts: int
    completed_texts: int = Field(default=0)

    def _get_query_embedding(self, query: str):
        return self.wrapped_model.get_query_embedding(query)

    async def _aget_query_embedding(self, query: str):
        return await self.wrapped_model.aget_query_embedding(query)

    def _get_text_embedding(self, text: str):
        return self.wrapped_model.get_text_embedding(text)

    def get_text_embedding_batch(self, texts, show_progress=False, **kwargs):
        import time
        result = []
        batch_size = self.wrapped_model.embed_batch_size
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            result.extend(
                self.wrapped_model.get_text_embedding_batch(
                    batch,
                    show_progress=False,
                    **kwargs,
                )
            )
            self.completed_texts += len(batch)
            self.progress_callback(self.completed_texts, self.total_texts)
            if start + batch_size < len(texts):
                time.sleep(0.3)
        return result


def setup_embedding_model(
    model: str,
    backend: Optional[str] = None,
    **kwargs,
):
    """
    Sets up a cloud embedding model using Google Gemini or OpenRouter.

    Args:
        model (str): The name of the embedding model to use.
        backend (str, optional): 'Gemini' or 'OpenRouter'. Defaults to Gemini.

    Returns:
        An instance of BaseEmbedding.
    """
    try:
        if backend is None:
            if "/" in model and not model.startswith("models/"):
                backend = "OpenRouter"
            elif st.session_state.get("embedding_backend"):
                backend = st.session_state.get("embedding_backend")
            else:
                backend = "Gemini"

        if backend == "OpenRouter":
            from utils.openrouter import create_openrouter_embedding, get_openrouter_api_key
            api_key = st.session_state.get("openrouter_api_key") or get_openrouter_api_key()
            embedding = create_openrouter_embedding(model_name=model, api_key=api_key)
            logs.log.info(f"Using OpenRouter model {model} to generate embeddings")
        else:
            from utils.gemini import create_gemini_embedding, get_gemini_api_key
            api_key = st.session_state.get("gemini_api_key") or get_gemini_api_key()
            embedding = create_gemini_embedding(model_name=model, api_key=api_key)
            logs.log.info(f"Using Gemini model {model} to generate embeddings")

        return embedding
    except Exception as err:
        logs.log.error(f"Failed to setup the embedding model: {err}")
        raise err


def load_documents(data_dir: str):
    """
    Loads documents from a directory of files.

    Args:
        data_dir (str): The path to the directory containing the documents to be loaded.

    Returns:
        A list of documents, where each document is a string representing the content of the corresponding file.

    Raises:
        Exception: If there is an error creating the data index.
    """
    try:
        paths = validated_document_paths(data_dir)
        if not paths:
            return []
        files = SimpleDirectoryReader(input_files=[str(path) for path in paths])
        documents = files.load_data()
        logs.log.info(f"Loaded {len(documents):,} documents from files")
        return documents
    except Exception as err:
        logs.log.error(f"Error creating data index: {err}")
        raise Exception(f"Error creating data index: {err}")


def create_index(documents, embed_model, chunk_size, chunk_overlap, progress_callback=None):
    """
    Creates an index from the provided documents and service context.

    Args:
        documents (list[str]): A list of strings representing the content of the documents to be indexed.
        embed_model: BaseEmbedding instance.
        chunk_size: Size of chunks.
        chunk_overlap: Overlap of chunks.
        progress_callback: Optional progress reporter callback.

    Returns:
        An instance of `VectorStoreIndex`, containing the indexed data.
    """
    try:
        chunk_size, chunk_overlap = validate_chunk_settings(chunk_size, chunk_overlap)
        nodes = run_transformations(
            documents,
            [SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)],
            show_progress=True,
        )
        if len(nodes) > MAX_INDEX_NODES:
            raise ValueError(f"Too many document chunks. Limit: {MAX_INDEX_NODES}.")

        if progress_callback is not None:
            progress_callback(0, len(nodes))
            embed_model = ProgressReportingEmbedding(
                wrapped_model=embed_model,
                progress_callback=progress_callback,
                model_name=embed_model.model_name,
                embed_batch_size=embed_model.embed_batch_size,
                total_texts=len(nodes),
            )

        index = VectorStoreIndex(
            nodes=nodes,
            embed_model=embed_model,
            show_progress=False,
        )

        logs.log.info("Index created from loaded documents successfully")
        return index
    except Exception as err:
        logs.log.error(f"Index creation failed: {err}")
        err_msg = str(err)
        if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
            raise Exception(
                "Gemini Free Tier embedding quota exceeded (30,000 tokens/min limit). "
                "Please wait a moment before retrying, or switch to 'OpenRouter' embeddings in Settings "
                "for uninterrupted cloud indexing."
            ) from err
        raise Exception(f"Index creation failed: {err}")


def create_query_engine(documents, llm, embed_model, chunk_size, chunk_overlap, progress_callback=None):
    """
    Creates a query engine from the provided documents and service context.
    """
    try:
        index = create_index(documents, embed_model, chunk_size, chunk_overlap, progress_callback=progress_callback)

        query_engine = index.as_query_engine(
            llm=llm,
            similarity_top_k=st.session_state.get("top_k", 3),
            response_mode=st.session_state.get("chat_mode", "compact"),
            streaming=True,
        )

        logs.log.info("Query Engine created successfully")
        return query_engine
    except Exception as e:
        logs.log.error(f"Error when creating Query Engine: {e}")
        raise Exception(f"Error when creating Query Engine: {e}")
