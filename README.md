# Local Ollama RAG

A fully local Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex with Ollama. This project provides offline question-answering capabilities by indexing local documents without any external network calls.

## Features

- **100% Local**: No cloud APIs, no telemetry, fully offline after installation
- **Reuses Existing Models**: Uses your already-installed Ollama chat models
- **Persistent Storage**: Indexes are saved to disk for fast subsequent queries
- **Clean CLI**: Simple command-line interface with doctor, ingest, and query commands
- **Minimal Dependencies**: Lean, reproducible setup with only essential packages

## Prerequisites

1. **Python 3.10+** installed
2. **Ollama** installed and running
   ```bash
   # Check Ollama version
   ollama --version
   
   # Start Ollama server (if not running)
   ollama serve
   
   # List installed models
   ollama list
   ```

3. At least one chat model installed in Ollama:
   ```bash
   # If you don't have any models, install one:
   ollama pull llama3.1
   ```

## Quick Start

### 1. Setup

```bash
# Clone and enter the project directory
cd local-ollama-rag

# Copy environment template
cp .env.example .env

# Edit .env and set OLLAMA_CHAT_MODEL to one of your installed models
# For example: OLLAMA_CHAT_MODEL=llama3.1

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### 2. Check System Health

```bash
# Using Make (Linux/macOS)
make doctor

# Windows/Direct Python
python -m rag.cli doctor
```

This will verify:
- Ollama server is running
- Available chat models
- Embedding model status

### 3. Pull Embedding Model (if needed)

If the doctor command shows the embedding model is missing:
```bash
ollama pull nomic-embed-text
```

### 4. Add Documents

Place your documents (`.txt`, `.md`, `.pdf`, `.json`, `.csv`) in the `./docs` directory:
```bash
mkdir -p docs
echo "The capital of France is Paris." > docs/sample.txt
```

### 5. Build Index

```bash
# Using Make
make ingest

# Windows/Direct Python
python -m rag.cli ingest
```

### 6. Query Your Documents

```bash
# Using Make
make query Q="What is the capital of France?"

# Windows/Direct Python
python -m rag.cli query "What is the capital of France?"

# With options
python -m rag.cli query "Your question" --k 6 --show-sources
```

### 7. Run Smoke Test

Verify everything works with an in-memory test:
```bash
# Using Make
make smoke

# Windows/Direct Python
python scripts/rag_smoke.py
```

## Windows Instructions

For Windows users without `make`, use these Python commands directly:

```powershell
# Install
pip install -e .

# Check health
python -m rag.cli doctor

# Ingest documents
python -m rag.cli ingest

# Query
python -m rag.cli query "Your question here"

# Run smoke test
python scripts/rag_smoke.py

# Run unit tests
pytest tests/ -v
```

## Configuration

Edit `.env` or set environment variables:

- `DOCS_DIR`: Directory containing documents (default: `./docs`)
- `INDEX_DIR`: Directory for storing index (default: `./index_storage`)
- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://localhost:11434`)
- `OLLAMA_CHAT_MODEL`: Chat model to use (no default - uses auto-detection)
- `OLLAMA_EMBED_MODEL`: Embedding model (default: `nomic-embed-text`)
- `SIMILARITY_TOP_K`: Number of similar chunks to retrieve (default: 4)

## Project Structure

```
.
├── src/rag/          # Main package
│   ├── cli.py        # CLI interface
│   ├── config.py     # Configuration management
│   ├── ingest.py     # Document ingestion
│   ├── query.py      # Query engine
│   └── ollama_check.py # Ollama health checks
├── scripts/          # Utility scripts
│   └── rag_smoke.py  # Smoke test
├── tests/            # Unit tests
├── docs/             # Your documents go here
└── index_storage/    # Persisted vector index
```

## Troubleshooting

### Ollama Server Not Running
```bash
# Start Ollama
ollama serve

# Check if it's running (should show version info)
curl http://localhost:11434/api/version
```

### No Models Found
```bash
# List available models
ollama list

# Pull a model (but NOT required if you already have one)
ollama pull llama3.1
```

### Port Conflicts
If Ollama is running on a different port, update `.env`:
```
OLLAMA_BASE_URL=http://localhost:YOUR_PORT
```

### Large Files Skipped
Files over 20MB are automatically skipped during ingestion. Split large documents or adjust the limit in the code if needed.

### Missing Embedding Model
The default embedding model is `nomic-embed-text`. If not installed:
```bash
ollama pull nomic-embed-text

# Or use an alternative like mxbai-embed-large
ollama pull mxbai-embed-large
# Then update .env: OLLAMA_EMBED_MODEL=mxbai-embed-large
```

## Important Notes

- **No Auto-Pull for Chat Models**: This tool will NEVER automatically download chat models. It only uses models you've already installed.
- **Idempotent Ingestion**: Re-running `ingest` is safe and won't duplicate data.
- **Fully Offline**: After `pip install`, no internet connection is required.
- **Local Only**: All operations use `localhost` - no external API calls.

## Development

```bash
# Run tests
make test

# Type checking
mypy src/

# Linting
ruff check src/

# Clean generated files
make clean
```

## License

MIT