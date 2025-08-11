# Quick Reference - Local Ollama RAG

## Essential Commands

```bash
# System check
rag doctor

# Index documents
rag ingest

# Query documents
rag query "your question"

# Show configuration
rag --config-info
```

## File Structure

```
your-project/
├── rag.exe           # Executable
├── docs/             # Your documents go here
├── index_storage/    # Generated index (don't edit)
└── .env              # Optional config file
```

## Document Types Supported

- **PDF files** (`.pdf`)
- **Text files** (`.txt`)
- **Markdown** (`.md`)
- **JSON files** (`.json`)
- **CSV files** (`.csv`)

## Common Usage Patterns

### First Time Setup
```bash
ollama pull llama3.1                    # Install AI model
ollama pull nomic-embed-text            # Install embedder
rag doctor                              # Check setup
```

### Daily Workflow
```bash
cp new-document.pdf docs/               # Add document
rag ingest                              # Update index
rag query "What's new in this doc?"     # Ask question
```

### Advanced Queries
```bash
rag query "summary?" --k 8              # More context
rag query "details?" --show-sources     # Show sources
```

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DOCS_DIR` | `./docs` | Where documents are stored |
| `OLLAMA_CHAT_MODEL` | *auto* | Which AI model to use |
| `SIMILARITY_TOP_K` | `4` | Context chunks to retrieve |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Server not running" | `ollama serve` |
| "No models" | `ollama pull llama3.1` |
| "No documents found" | Add files to `docs/` |
| "Index not found" | Run `rag ingest` |

## Development Commands

```bash
# Run tests
pytest tests/ -v
python run_tests.py

# Test coverage
pytest tests/ --cov=rag

# Code quality
ruff check src/
mypy src/

# Security scan
safety check
bandit -r src/
```

## Quick Tips

- **Add documents**: Drop files in `docs/` folder
- **Re-index**: Run `rag ingest` after adding files
- **Better answers**: Try `--k 6` for more context
- **Find sources**: Use `--show-sources` flag
- **Check config**: Use `rag --config-info`
- **Run tests**: Use `pytest tests/` or `python run_tests.py`
- **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

*Full documentation: [USER_GUIDE.md](USER_GUIDE.md) | Testing: [TESTING.md](TESTING.md)*