# Setup & Installation Guide

Before starting with NexusRAG, ensure you have:

- **Python 3.10, 3.11, or 3.12+**
- An API Key for **Google Gemini** (Free tier available at [Google AI Studio](https://aistudio.google.com/)) and/or **OpenRouter** (Free tier models available at [OpenRouter](https://openrouter.ai/keys)).

---

## Windows Quick Setup

NexusRAG includes automated scripts for Windows:

1. **Install Dependencies**:
   ```cmd
   setup.bat
   ```
   This will:
   - Verify Python installation.
   - Create an isolated `.venv` virtual environment.
   - Upgrade `pip` to the latest version.
   - Install all required packages from `requirements.txt`.
   - Initialize `.env` from `.env.example`.

2. **Configure API Keys**:
   Open `.env` in any text editor and paste your API keys:
   ```env
   GEMINI_API_KEY=your_key_here
   OPENROUTER_API_KEY=your_key_here
   ```

3. **Launch NexusRAG**:
   ```cmd
   run.bat
   ```
   This launches the Streamlit server and automatically opens your default browser at `http://localhost:8501`.

---

## Linux / macOS Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/PanavCodes/NexusRAG.git
cd NexusRAG

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install requirements
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env

# 5. Run Streamlit
streamlit run main.py
```

---
