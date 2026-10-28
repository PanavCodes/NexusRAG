# NexusRAG Pipeline Architecture

NexusRAG implements an in-memory LlamaIndex VectorStore architecture optimized for low-latency indexing, multi-engine intelligence, and strict security boundaries.

---

## Ingestion Flow

1. **Source Acquisition & Security Validation**:
   - Files are validated against extension allowlists, size limits, and zip bomb decompression ratios.
   - GitHub repositories are shallow-cloned (`--depth 1`) into temporary sandbox folders.
   - Websites are fetched via HTTPS with redirect limiters and IP address boundary enforcement.
2. **Document Parsing**:
   - Specialized readers parse tabular spreadsheets, slides, word processor docs, notebooks, and source code.
3. **Chunking & Token Partitioning**:
   - `SentenceSplitter` segments loaded text into overlapping token windows using configured `chunk_size` and `chunk_overlap`.
4. **Vector Embedding Generation**:
   - Chunks are vectorized using the selected embedding backend:
     - **Google Gemini**: 3072-dimensional semantic embeddings.
     - **OpenRouter**: Cloud embeddings (`baai/bge-large-en-v1.5`, `text-embedding-3-small`).
5. **Index Assembly**:
   - Vector embeddings and chunk metadata are loaded into an in-memory `VectorStoreIndex`.
6. **Workspace Cleanup**:
   - Transient ingestion files are immediately unlinked and removed from disk.

---

## Query Synthesis Flow

```
[User Query]
     │
     ▼
[Vector Index Search] ──▶ Retrieve Top-K Relevant Document Chunks
     │
     ▼
[Prompt Assembly] ──────▶ Combine User Query + Retrieved Context Chunks + System Prompt
     │
     ▼
[AI Model Synthesis] ───▶ Stream Response via Google Gemini or OpenRouter Free Model
     │
     ▼
[UI Delivery] ──────────▶ Stream text chunks to chatbox with source node citations
```

---

## Error Resilience & Backoff

- **Rate Limits (429 / RESOURCE_EXHAUSTED)**: NexusRAG detects API rate limiting and applies exponential backoff jitter before transparently retrying requests.
- **Source Failures**: If an import fails, the existing index and conversation state are preserved without interruption.
