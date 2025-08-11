# Vector Bot

[![CI](https://github.com/joshuaramirez/vector-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/joshuaramirez/vector-bot/actions/workflows/ci.yml)
[![Security](https://github.com/joshuaramirez/vector-bot/actions/workflows/security.yml/badge.svg)](https://github.com/joshuaramirez/vector-bot/actions/workflows/security.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)](https://github.com/joshuaramirez/vector-bot)
[![Tests](https://img.shields.io/badge/tests-135%20passing-brightgreen.svg)](https://github.com/joshuaramirez/vector-bot)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Vector Bot is a fully local Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex with Ollama. Ask natural language questions about your documents, with everything running offline on your computer.

## 📖 Documentation

- **[USER_GUIDE.md](USER_GUIDE.md)** - Complete user guide with examples and troubleshooting
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Multi-environment deployment guide
- **[TESTING.md](TESTING.md)** - Comprehensive testing documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability reporting
- **[CLAUDE.md](CLAUDE.md)** - Development guidelines

## Features

- **100% Local**: No cloud APIs, no telemetry, fully offline after installation
- **Multi-Environment**: Development, production, and Docker configurations
- **Executable Distribution**: Single-file deployment with no Python required
- **Document Support**: PDF, Markdown, text, JSON, CSV files
- **Persistent Storage**: Indexes are saved to disk for fast subsequent queries
- **Clean CLI**: Simple command-line interface with doctor, ingest, and query commands
- **CI/CD Pipeline**: Automated testing, building, and PyPI publishing
- **Comprehensive Testing**: 135 passing tests with 99% code coverage
- **Security Scanning**: Automated vulnerability detection and CodeQL analysis

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

### Option 1: Using Pre-built Executable (Recommended)

If you have the `vector-bot.exe` file:

1. **Install Ollama** and a chat model:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

2. **Verify setup**:
   ```bash
   vector-bot doctor
   ```

3. **Add documents and start querying**:
   ```bash
   # Add your documents to docs/ folder
   mkdir docs
   cp your-files.pdf docs/

   # Index documents
   vector-bot ingest

   # Ask questions
   vector-bot query "What is this document about?"
   ```

See [USER_GUIDE.md](USER_GUIDE.md) for complete instructions.

### Option 2: From Source

```bash
# Clone and enter the project directory
cd vector-bot

# Copy environment template
cp .env.example .env

# Edit .env and set OLLAMA_CHAT_MODEL to one of your installed models
# For example: OLLAMA_CHAT_MODEL=llama3.1

# Install the package
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

## Example Workflow

```bash
# 1. Check system status
vector-bot doctor

# 2. Add your documents
mkdir docs
cp *.pdf docs/
cp *.md docs/

# 3. Index documents
vector-bot ingest

# 4. Ask questions
vector-bot query "What are the main topics covered?"
vector-bot query "Summarize the key findings" --show-sources
vector-bot query "What does the document say about security?" --k 8

# 5. Use different environments
vector-bot --env production ingest
vector-bot --env development query "How do I deploy this?"
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
├── src/rag/          # Main package (vector-bot)
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

## Multi-Environment Support

The application supports different deployment environments:

```bash
# Development (default)
vector-bot doctor

# Production deployment
vector-bot --env production doctor

# Docker deployment  
vector-bot --env docker doctor

# Show current configuration
vector-bot --config-info --env production
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed multi-environment setup.

## Building Executable

To create a standalone executable:

```bash
# Build executable (all platforms)
make build-exe

# Or manually
python build_executable.py
```

This creates a single executable file in `dist/vector-bot` (or `dist/vector-bot.exe` on Windows) that includes all dependencies and configuration files. The target system only needs:
- Ollama installed and running
- No Python installation required

## Development

```bash
# Run all tests
make test
pytest tests/ -v

# Run unit tests only
pytest tests/unit/ -v

# Run with coverage
pytest tests/ --cov=src/rag --cov-report=html

# Type checking
mypy src/

# Linting
ruff check src/

# Run security checks
safety check
bandit -r src/

# Use the test runner
python run_tests.py

# Clean generated files (including build artifacts)
make clean
```

### Testing

The project includes comprehensive testing:
- **114 unit tests** passing (99.1% pass rate)
- **99% code coverage** across all modules
- **100% mocked external dependencies** - tests run offline
- **Professional test structure** following best practices
- **CI-ready** - all tests run in under 20 seconds

See [TESTING.md](TESTING.md) for detailed testing documentation.

## License

MIT