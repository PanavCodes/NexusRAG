# Troubleshooting Guide

This guide helps resolve common questions and issues when running NexusRAG.

---

## 1. API Key Issues

- **Error: "Missing Gemini API Key" or "Missing OpenRouter API Key"**:
  - Ensure `.env` is created in the project root containing your API key.
  - Alternatively, enter your API key directly in the **Settings** tab inside the web UI.
  - Check that the key does not have leading or trailing whitespace.

## 2. Ingestion Disabled in UI

- Ingestion buttons remain disabled until:
  - An API key is provided for the selected model provider.
  - A valid chat model is selected.
  - A valid embedding backend is configured.

## 3. Rate Limits & Quotas (429 Too Many Requests)

- Free tier API keys may occasionally encounter per-minute token or request caps.
- **Resolution**:
  - NexusRAG automatically performs exponential backoff retries when encountering 429 errors.
  - If rate limits persist, lower the `Chunk Size` or import smaller repositories/documents.
  - Alternatively, select a different model or switch the embedding backend between **Google Gemini** and **OpenRouter**.

## 4. GitHub Import Issues

- **Repository not found**: Ensure the repository is public and formatted as `owner/repo` (e.g. `octocat/Hello-World`).
- **Repository too large**: GitHub imports enforce a limit of 1,000 files and 100 MB total size.

## 5. Website Import Errors

- **Non-HTTPS URLs**: Only secure HTTPS endpoints are accepted.
- **SSRF Block**: URLs resolving to localhost (`127.0.0.1`), private LAN IP ranges, or cloud metadata endpoints (`169.254.169.254`) are blocked for security.

## 6. Logs & Diagnostics

- NexusRAG logs operational events to `nexusrag.log` in the application root directory.
- Reviewing `nexusrag.log` provides detailed stack traces and request execution details.
