# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project Overview

NexusRAG is a Streamlit application for high-performance Retrieval-Augmented Generation (RAG) powered entirely by cloud AI models (Google Gemini and OpenRouter Free Tier), LlamaIndex, local files, GitHub repositories, and live websites.

Primary entry points:

- `main.py`: Streamlit app bootstrap.
- `components/`: Streamlit UI pieces.
- `utils/`: Ingestion, Gemini & OpenRouter integrations, browser settings, and RAG pipeline helpers.
- `tests/`: Local unit tests.

## Setup & Execution

Use the project virtual environment rather than system Python:

```bash
# Windows
setup.bat
run.bat

# Linux / macOS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

## Verification

Run the full pytest suite before submitting or committing changes:

```bash
pytest
python -m py_compile main.py components/page_state.py components/tabs/settings.py utils/browser_settings.py utils/gemini.py utils/openrouter.py
```

## Browser Settings

Settings persistence uses browser `localStorage` through the local Streamlit component in `utils/browser_storage_component/`.

- Persisted settings are defined in `utils/browser_settings.py`.
- Do not reintroduce query-parameter persistence for settings.
- Cloud backends supported: Google Gemini and OpenRouter.

## Security-Sensitive Areas

Be careful when editing:

- File uploads, decompression bomb detection, and path handling in `utils/helpers.py`.
- Website ingestion and SSRF/URL validation in `components/tabs/website.py`.
- GitHub cloning and shallow clones in `components/tabs/github_repo.py`.
- Any code that handles API keys or creates network sessions.
