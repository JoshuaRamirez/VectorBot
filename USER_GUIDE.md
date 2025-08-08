# User Guide - Local Ollama RAG

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [First-Time Setup](#first-time-setup)
4. [Basic Usage](#basic-usage)
5. [Working with Documents](#working-with-documents)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)
8. [Command Reference](#command-reference)
9. [Best Practices](#best-practices)

## Introduction

Local Ollama RAG is a powerful tool that lets you ask questions about your documents using AI, all while keeping everything on your computer. No internet connection required, no data sent to the cloud - everything runs locally.

### What Can You Do With It?

- **Query your documents**: Ask natural language questions about PDFs, text files, markdown files
- **Build a knowledge base**: Index technical documentation, research papers, notes
- **Private AI assistant**: Get AI-powered answers without sharing sensitive data
- **Offline operation**: Works completely offline once set up

## Installation

### Method 1: Using the Standalone Executable (Easiest)

If you received `rag.exe` (Windows) or `rag` (Mac/Linux):

1. **Place the executable** in a convenient location (e.g., `C:\Tools\` or `/usr/local/bin/`)
2. **Add to PATH** (optional) for easier access
3. **Test it works**:
   ```bash
   rag --version
   ```

### Method 2: From Source Code

1. **Install Python 3.10+** from [python.org](https://python.org)
2. **Clone or download** the project
3. **Install dependencies**:
   ```bash
   pip install -e .
   ```

### Installing Ollama

1. **Download Ollama** from [ollama.ai](https://ollama.ai)
2. **Install and start** Ollama:
   ```bash
   ollama serve
   ```
3. **Install a chat model**:
   ```bash
   # Install a model (only needed once)
   ollama pull llama3.1
   
   # List available models
   ollama list
   ```

## First-Time Setup

### Step 1: Verify Installation

```bash
# Check if everything is working
rag doctor

# Expected output:
# ✓ Ollama server is running
# ✓ Chat model: llama3.1
# ✓ Embedding model: nomic-embed-text
```

### Step 2: Install Embedding Model

If the doctor command shows the embedding model is missing:

```bash
ollama pull nomic-embed-text
```

### Step 3: Configure Settings (Optional)

Create a `.env` file in your working directory:

```bash
# Copy the example configuration
cp .env.example .env

# Edit with your preferences
notepad .env  # Windows
nano .env     # Mac/Linux
```

Common settings to adjust:
- `DOCS_DIR`: Where to look for documents (default: `./docs`)
- `OLLAMA_CHAT_MODEL`: Which AI model to use (default: auto-detect)
- `SIMILARITY_TOP_K`: How many relevant chunks to retrieve (default: 4)

## Basic Usage

### The Three-Step Workflow

#### 1. Add Your Documents

Create a `docs` folder and add your files:

```bash
mkdir docs
# Copy your PDFs, text files, markdown files into docs/
cp ~/Documents/*.pdf docs/
```

Supported formats:
- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.json` - JSON files
- `.csv` - CSV files

#### 2. Index Your Documents

Build the searchable index:

```bash
rag ingest

# Output:
# Loading 15 documents...
# Building vector index...
# ✓ Index saved to ./index_storage
# ✓ Indexed 127 chunks
```

**Note**: This step only needs to be done once. Re-run when you add new documents.

#### 3. Ask Questions

Query your documents:

```bash
# Simple question
rag query "What are the project requirements?"

# Question with more context chunks
rag query "Explain the authentication flow" --k 6

# Show which documents were used
rag query "What is the deployment process?" --show-sources
```

## Working with Documents

### Document Organization Tips

```
docs/
├── projects/
│   ├── project-a-spec.pdf
│   └── project-b-notes.md
├── guides/
│   ├── user-manual.pdf
│   └── admin-guide.md
└── references/
    ├── api-docs.md
    └── troubleshooting.txt
```

### Handling Large Documents

- Documents over 20MB are automatically skipped
- Break large documents into smaller parts if needed
- Use markdown format when possible (faster processing)

### Updating Your Index

When you add new documents:

```bash
# Add new files to docs/
cp new-document.pdf docs/

# Re-run ingestion (safe - won't duplicate)
rag ingest
```

To completely rebuild the index:

```bash
# Remove old index
rm -rf index_storage/  # Unix
rmdir /s index_storage  # Windows

# Rebuild
rag ingest
```

## Advanced Features

### Environment-Specific Configurations

Use different settings for different scenarios:

```bash
# Development mode (verbose output)
rag --env development doctor

# Production mode (optimized)
rag --env production ingest

# Check current configuration
rag --config-info --env production
```

### Custom Model Selection

Override the default model:

```bash
# Set via environment variable
export OLLAMA_CHAT_MODEL=llama3.3
rag query "What is the summary?"

# Or in .env file
OLLAMA_CHAT_MODEL=mistral
```

### Batch Processing

Process multiple questions from a file:

```bash
# Create questions file
echo "What is the main purpose?" > questions.txt
echo "List all requirements" >> questions.txt
echo "Explain the architecture" >> questions.txt

# Process all questions
while IFS= read -r question; do
    echo "Q: $question"
    rag query "$question"
    echo "---"
done < questions.txt
```

### Integration with Scripts

```python
# Python script example
import subprocess
import json

def query_rag(question):
    result = subprocess.run(
        ["rag", "query", question],
        capture_output=True,
        text=True
    )
    return result.stdout

answer = query_rag("What are the key features?")
print(answer)
```

## Troubleshooting

### Common Issues and Solutions

#### "Ollama server not running"

```bash
# Start Ollama
ollama serve

# Check if it's running
curl http://localhost:11434/api/tags
```

#### "No suitable chat model found"

```bash
# Install a model
ollama pull llama3.1

# List available models
ollama list

# Set in configuration
export OLLAMA_CHAT_MODEL=llama3.1
```

#### "No documents found"

```bash
# Check documents directory
ls docs/

# Verify path in config
rag --config-info

# Use absolute path if needed
export DOCS_DIR=/full/path/to/documents
```

#### "Index not found"

```bash
# Build the index first
rag ingest

# Check index location
ls index_storage/
```

#### Slow Performance

- Reduce similarity chunks: `rag query "question" --k 2`
- Use a faster model: `OLLAMA_CHAT_MODEL=llama3.1`
- Check available RAM and close other applications

### Port Conflicts

If Ollama is on a different port:

```bash
# Set custom URL
export OLLAMA_BASE_URL=http://localhost:8080
rag doctor
```

## Command Reference

### Global Options

```bash
rag [--env ENV] [--config-info] COMMAND
```

- `--env ENV`: Use specific environment (development, production, docker)
- `--config-info`: Show configuration and exit
- `--version`: Show version
- `--help`: Show help

### Commands

#### `doctor` - System Health Check

```bash
rag doctor [--verbose]
```

Checks:
- Ollama server connectivity
- Available models
- Configuration validity

#### `ingest` - Index Documents

```bash
rag ingest [--verbose]
```

Options:
- `--verbose`: Show detailed progress

#### `query` - Ask Questions

```bash
rag query "your question" [OPTIONS]
```

Options:
- `--k N`: Number of similar chunks to retrieve (default: 4)
- `--show-sources`: Display source documents used
- `--verbose`: Show detailed processing

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DOCS_DIR` | Documents directory | `./docs` |
| `INDEX_DIR` | Index storage location | `./index_storage` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_CHAT_MODEL` | Chat model to use | Auto-detect |
| `OLLAMA_EMBED_MODEL` | Embedding model | `nomic-embed-text` |
| `SIMILARITY_TOP_K` | Retrieval chunks | `4` |
| `RAG_ENV` | Environment profile | `development` |

## Best Practices

### Document Preparation

1. **Use descriptive filenames**: `project-spec-v2.pdf` instead of `doc1.pdf`
2. **Break up large documents**: Split >20MB files into chapters
3. **Prefer text formats**: Markdown and text process faster than PDFs
4. **Include context**: Add summary sections to technical documents

### Query Strategies

1. **Be specific**: "What is the login process?" vs "How does it work?"
2. **Use keywords**: Include important terms from your documents
3. **Iterate**: If first answer isn't complete, refine your question
4. **Adjust retrieval**: Use `--k` to get more or fewer context chunks

### Performance Optimization

1. **Index once**: Don't rebuild unless adding documents
2. **Choose appropriate models**:
   - Fast: `llama3.1` (7B parameters)
   - Balanced: `llama3.3` (70B parameters)
   - Best: `mixtral` (8x7B parameters)
3. **Limit document size**: Break PDFs >10MB into sections
4. **Use SSD storage**: Place index on fast storage

### Security Considerations

1. **Keep documents local**: Never put sensitive docs in cloud folders
2. **Control access**: Restrict `docs/` and `index_storage/` permissions
3. **No telemetry**: This tool never sends data externally
4. **Audit models**: Verify Ollama models are from trusted sources

## Examples

### Academic Research

```bash
# Index research papers
cp ~/Research/Papers/*.pdf docs/
rag ingest

# Find relevant studies
rag query "What studies discuss quantum computing applications?"
rag query "Summarize findings about machine learning in healthcare" --k 8
```

### Software Documentation

```bash
# Index API docs and guides
cp -r ~/project/docs/* docs/
rag ingest

# Quick lookups
rag query "How do I authenticate API requests?"
rag query "What are the rate limits?"
rag query "Show example of webhook implementation" --show-sources
```

### Personal Knowledge Base

```bash
# Index notes and articles
cp ~/Notes/*.md docs/
rag ingest

# Search your notes
rag query "What did I learn about Docker networking?"
rag query "Find my notes about Python decorators"
```

### Technical Support

```bash
# Index manuals and guides
cp ~/Manuals/*.pdf docs/
rag ingest

# Troubleshooting
rag query "How to reset the printer?"
rag query "What does error code E45 mean?"
```

## Getting Help

### Resources

- **README.md**: Technical documentation and setup
- **DEPLOYMENT.md**: Multi-environment deployment guide
- **CLAUDE.md**: Development guidelines

### Common Commands for Help

```bash
# Check system status
rag doctor --verbose

# Show configuration
rag --config-info

# Command help
rag --help
rag query --help

# Version information
rag --version
```

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Ollama server not running" | Can't connect to Ollama | Start with `ollama serve` |
| "No models installed" | No AI models available | Run `ollama pull llama3.1` |
| "No documents found" | Empty docs directory | Add files to `docs/` folder |
| "Index not found" | Haven't built index | Run `rag ingest` first |

---

## Quick Reference Card

```bash
# Initial setup
ollama pull llama3.1           # Install AI model
ollama pull nomic-embed-text   # Install embedding model
rag doctor                      # Verify setup

# Daily workflow
cp document.pdf docs/           # Add document
rag ingest                      # Build/update index
rag query "question?"           # Ask question

# Useful options
rag query "question?" --k 6 --show-sources
rag --env production ingest
rag --config-info

# Troubleshooting
ollama serve                    # Start Ollama
ollama list                     # List models
ls docs/                        # Check documents
```

---

*This guide covers Local Ollama RAG version 1.0.0*