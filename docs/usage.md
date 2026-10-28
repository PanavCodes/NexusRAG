# Using NexusRAG

## Quick Start Workflow

1. **Configure API Key**: In the **Settings** tab, verify or enter your Google Gemini or OpenRouter API key.
2. **Select Chat Model**: Choose your preferred model (e.g. `gemini-3.5-flash-lite`, `cohere/north-mini-code:free`).
3. **Choose Embedding Backend**: Select **Google Gemini** or **OpenRouter**.
4. **Import Data**: In the sidebar, select **Local Files**, **GitHub Repo**, or **Websites** and click Import.
5. **Ask Questions**: Once indexing finishes, query your documents in the main chat interface.

---

## Settings Reference

Settings are persisted in your browser's `localStorage` across refreshes.

### AI Model Provider & Reasoning
| Setting | Description | Default |
| --- | --- | --- |
| **Model Provider** | Switch between Google Gemini and OpenRouter Free models. | Gemini |
| **Chat Model** | Active LLM for answer synthesis. | `gemini-3.5-flash-lite` |
| **Top K** | Number of relevant context chunks retrieved per query. | `3` |
| **Chat Mode** | Query synthesis mode (`compact`, `refine`, etc.). | `compact` |

### Embeddings Configuration
| Setting | Description | Default |
| --- | --- | --- |
| **Backend** | Vector embedding generator (`Gemini`, `OpenRouter`). | `Gemini` |
| **OpenRouter Model** | Embedding model for OpenRouter (`baai/bge-large-en-v1.5`, etc.). | `baai/bge-large-en-v1.5` |
| **Chunk Size** | Maximum tokens per text chunk (256 - 8192). | `1024` |
| **Chunk Overlap** | Token overlap between consecutive chunks (0 - 2048). | `200` |

---

## Data Sources

### 1. Local Files
- **Supported Formats**: Excel (`.xlsx`, `.xls`), Word (`.docx`), PDF (`.pdf`), PowerPoint (`.pptx`, `.ppt`), CSV (`.csv`), Notebooks (`.ipynb`), Markdown (`.md`), Plain Text (`.txt`), EPUB (`.epub`), RTF (`.rtf`).
- **Limits**: Up to 10 files per upload, 25 MB per file, 100 MB total.

### 2. GitHub Repositories
- **Input**: Enter `owner/repo` (e.g. `octocat/Hello-World`) or full URL `https://github.com/owner/repo`.
- **Cloning**: Shallow clone (`--depth 1`) directly into a secure temporary workspace.
- **Limits**: Up to 1,000 files, 100 MB total.

### 3. Websites
- **Input**: Enter up to 5 public HTTPS URLs.
- **Parsing**: Clean HTML article extraction with automated boilerplate removal.
- **Security**: Prohibits localhost, loopback, private networks, and cloud metadata services.

---

## Exporting Data
Download your conversation transcripts at any time via `Settings > Export Data > Chat History` in JSON format.
