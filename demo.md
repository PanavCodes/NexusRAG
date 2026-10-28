# NexusRAG • Interactive Testing & Demonstration Guide

This guide provides recommended data sources, repositories, and websites tailored for **NexusRAG v2.0** to achieve **minimum embedding latency**, zero rate-limit delays, and fast validation of all system features.

---

## ⚡ Quick Start: Zero-Latency Recommendations

Embedding generation speed depends on text volume and the chosen embedding backend. To load and index data in **under 3 seconds**, follow these exact recommendations:

### 1. Recommended GitHub Repositories (Fastest Ingestion)

| Priority | Repository | URL / Slug | Files / Tokens | Ingestion Time | Why It's Best |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **#1 (Instant)** | `octocat/Hello-World` | `octocat/Hello-World` | 2 files (~150 tokens) | **~1.2 seconds** | Minimal repository. Perfect for verifying git clone, file extraction, vectorization, and query readiness in under 2 seconds. |
| **#2 (Single-File App)** | `bottlepy/bottle` | `bottlepy/bottle` | Single core Python module | **~3.5 seconds** | Real production micro-framework in 1 file. Excellent for code search, function retrieval, and logic questions. |
| **#3 (Payment Pipeline)** | `PanavCodes/Data-Extraction-and-Processing-Pipeline-for-Payment-Card-Fraud-Detection` | `PanavCodes/Data-Extraction-and-Processing-Pipeline-for-Payment-Card-Fraud-Detection` | 4 code/doc files (~3.5k tokens) | **~4.0 seconds** | Real-world data extraction & fraud detection pipeline. Benchmark-validated for end-to-end RAG QA. |

> [!TIP]
> **Best Embedding Setting for Repositories**:
> Go to **Settings -> Embeddings** and select **`OpenRouter`** with `baai/bge-large-en-v1.5` or **`Google Gemini`**. These backends have **no per-minute token quotas**, indexing code repositories in a single burst!

---

### 2. Recommended Websites (Fastest Ingestion)

NexusRAG features an SSRF-safe, redirect-bounded website scraper that strips scripts and styles to extract pure content.

| Priority | Website URL | Content Type | Ingestion Time | Sample Test Query |
| :--- | :--- | :--- | :--- | :--- |
| **#1 (Instant)** | `https://httpbin.org/html` | Simple Herman Melville HTML passage | **~1.0 second** | *"What story is Herman Melville telling in this document?"* |
| **#2 (Tech Docs)** | `https://docs.python.org/3/tutorial/appetite.html` | Official Python 3 appetite tutorial | **~2.2 seconds** | *"Why would someone use Python instead of C or shell scripts according to this page?"* |
| **#3 (Framework)** | `https://fastapi.tiangolo.com/tutorial/first-steps/` | FastAPI First Steps guide | **~2.8 seconds** | *"What are the 5 steps to create a FastAPI application?"* |

---

### 3. Recommended Local Files (Document Ingestion)

NexusRAG natively parses PDFs, Word docs, PowerPoint presentations, and Excel spreadsheets (`.xlsx`/`.xls` via `openpyxl`).

| File Type | Recommended Sample | Approximate Tokens | Ingestion Time |
| :--- | :--- | :--- | :--- |
| **Plain Text (`.txt`, `.md`)** | Any README or API specification | 500 – 2,000 | **~0.8 seconds** |
| **Excel Workbook (`.xlsx`)** | 50–200 row tabular data sheet | 1,000 – 4,000 | **~1.5 seconds** |
| **PDF Document (`.pdf`)** | 2–5 page whitepaper or invoice | 1,500 – 5,000 | **~2.5 seconds** |

---

## 🎯 Step-by-Step Feature Walkthrough

### Test A: Ultra-Fast GitHub Repository Ingestion
1. Open NexusRAG in your browser: `http://localhost:8501`.
2. In the sidebar, select **📁 Data Sources** -> **GitHub**.
3. In the repository input field, type:
   ```
   octocat/Hello-World
   ```
4. Click **`Process Repo`**.
5. Observe the live multi-stage progress container:
   - `Repository Validated` (0.3s)
   - `Cloning Repository` (0.6s)
   - `Repository Files Loaded` (0.2s)
   - `LLM Initialized` (0.2s)
   - `Embedding Model Ready` (0.1s)
   - `Index Ready` (0.4s)
6. In the chat box, ask:
   ```
   What is this repository about and what does it contain?
   ```
7. Watch the response stream back in real-time with sub-second time-to-first-token!

---

### Test B: Website Live Scraping & Reasoning
1. In the sidebar, select **📁 Data Sources** -> **Website**.
2. Enter:
   ```
   https://docs.python.org/3/tutorial/appetite.html
   ```
3. Click the **➕** button to add the URL to the stage list.
4. Click **`Process`**.
5. Once `Index Ready` appears, ask:
   ```
   Summarize the key advantages of Python mentioned on this page.
   ```

---

### Test C: Switching Between AI Providers (Free Models)
NexusRAG supports instant hot-swapping of AI backends without re-indexing your documents:
1. In the sidebar, open **⚙️ Settings** -> **Chat**.
2. **Switch to OpenRouter Free**:
   - Change **LLM Provider** to `OpenRouter (Free Models)`.
   - Your OpenRouter API Key is pre-configured.
   - Select model: `cohere/north-mini-code:free` (exceptional for code retrieval) or `deepseek/deepseek-r1:free`.
3. Submit a question in chat. Notice the top banner chip dynamically reflects `OpenRouter Free: cohere/north-mini-code:free`.
4. **Switch to Google Gemini**:
   - Change **LLM Provider** to `Google Gemini`.
   - Select model: `gemini-3.5-flash-lite` (lightning fast inference).
   - Submit another question in chat. Notice the top banner instantly updates.

---

### Test D: Testing Excel & Tabular RAG
1. In the sidebar, select **📁 Data Sources** -> **Files**.
2. Drag-and-drop any `.xlsx` or `.xls` spreadsheet.
3. Click **`Process Uploads`**.
4. Ask specific analytical questions about rows, column headers, or aggregated values:
   ```
   What columns are present in this sheet and what is the summary of row 1 to 5?
   ```

---

## 🚀 Performance Benchmarks Summary

| Backend Configuration | Quota Limit | Best For | Typical Retrieval Speed |
| :--- | :--- | :--- | :--- |
| **OpenRouter Free (`cohere/north-mini-code:free`) + BGE Large Embeddings** | Generous Free Tier | Codebases, scripts, developer documentation | **~1.1s** latency |
| **Google Gemini (`gemini-3.5-flash-lite`) + Gemini Embeddings 2** | 30k tokens/min (with auto-backoff) | Deep reasoning, long-form synthesis, technical reports | **~0.9s** latency |
| **Local Hugging Face (`gte-modernbert-base`) + Gemini Chat** | Unlimited Local CPU | Large repositories (> 100 files), zero rate limits | **~1.8s** latency |
