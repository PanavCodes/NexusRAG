# Contributing to NexusRAG

We welcome community contributions, bug fixes, and feature additions!

---

## Development Workflow

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/PanavCodes/NexusRAG.git
   cd NexusRAG
   ```

2. **Environment Setup**:
   - Windows: Run `setup.bat`
   - Linux/macOS: Create a virtual environment and run `pip install -r requirements.txt`

3. **Code Style**:
   - Follow PEP 8 guidelines.
   - Maintain type annotations and descriptive docstrings.
   - Keep defensive security controls intact (path normalization, SSRF defenses).

4. **Running Tests**:
   Before submitting any changes, verify the full test suite passes:
   ```bash
   pytest
   ```
   All 110+ unit and integration tests must pass cleanly.

5. **Submitting Pull Requests**:
   - Provide a clear, concise description of your changes.
   - Reference any relevant issues.
