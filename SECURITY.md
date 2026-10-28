# NexusRAG Security Policy

## Security Model & Protections

NexusRAG is designed with defensive security controls to safeguard local files and network communications:

- **SSRF Mitigation**: Web ingestion validates target URLs, prohibiting loopback (`127.0.0.1`), private networks, and cloud metadata endpoints (`169.254.169.254`, `metadata.google.internal`).
- **Path Traversal & Archive Bomb Defense**: All uploaded filenames are normalized and restricted. Archive-based files (`.docx`, `.xlsx`, `.pptx`, `.epub`) are verified against maximum decompression ratios and member limits before parsing.
- **Memory & Resource Caps**: Document limits, chunk thresholds, and API rate limits are enforced to protect host resources.

## Reporting Security Issues

Please report any suspected vulnerabilities directly to project maintainers. Avoid publishing sensitive credentials, model prompts containing secrets, or private data in reports.
