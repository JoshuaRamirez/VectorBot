---
title: Frequently Asked Questions
description: Common questions and quick answers about Vector Bot
audience: all
level: beginner
keywords: [faq, questions, answers, help, common-issues, quick-help]
related_docs: [../user/troubleshooting.md, ../user/installation.md, ../user/getting-started.md, glossary.md]
---

# Frequently Asked Questions (FAQ)

Quick answers to the most common questions about Vector Bot.

## Installation and Setup

### Q: What do I need to run Vector Bot?

**A:** You need:
1. **Ollama** installed and running
2. At least one **AI model** (like `llama3.1`)
3. The **embedding model** (`nomic-embed-text`)
4. **Vector Bot** installed via npm, pip, or executable

```bash
# Quick setup
ollama pull llama3.1
ollama pull nomic-embed-text
npm install -g @joshuaramirez/vector-bot
```

### Q: Which installation method should I use?

**A:** For most users, **npm is recommended**:
- **npm**: Best for most users, easiest updates
- **pip**: Good for Python developers
- **Executable**: Good for single-file deployment
- **Source**: For developers and contributors

### Q: Can Vector Bot run completely offline?

**A:** Yes! After initial setup, Vector Bot works 100% offline with no internet connection required.

### Q: What operating systems are supported?

**A:** Vector Bot runs on:
- Windows 10/11
- macOS 10.14+ (Intel and Apple Silicon)
- Linux (Ubuntu 18.04+, CentOS 7+, or equivalent)

## Basic Usage

### Q: How do I know if Vector Bot is working?

**A:** Run the health check command:
```bash
vector-bot doctor
```
You should see all checkmarks (✓) for Ollama server, models, and configuration.

### Q: What file formats does Vector Bot support?

**A:** Supported formats:
- **PDF files** (`.pdf`)
- **Text files** (`.txt`)
- **Markdown files** (`.md`)
- **JSON files** (`.json`)
- **CSV files** (`.csv`)

### Q: How do I add documents?

**A:** Simple! Just copy files to your `docs` folder:
```bash
mkdir docs
cp your-files.pdf docs/
vector-bot ingest
```

### Q: Do I need to re-index when I add new documents?

**A:** Yes, run `vector-bot ingest` after adding new documents. It's safe to run multiple times.

### Q: How do I ask questions?

**A:** Use the query command:
```bash
vector-bot query "What are the main topics in these documents?"
vector-bot query "How do I configure the API?" --show-sources
```

## Troubleshooting

### Q: "Command not found: vector-bot"

**A:** Vector Bot isn't installed or not in PATH:

**If installed via npm:**
```bash
npm install -g @joshuaramirez/vector-bot
```

**If using executable:**
- Use full path: `/path/to/vector-bot --version`
- Or add to PATH

### Q: "Ollama server not running"

**A:** Start Ollama:
```bash
ollama serve
```

Then test: `curl http://localhost:11434/api/tags`

### Q: "No suitable chat model found"

**A:** Install an AI model:
```bash
ollama pull llama3.1
# Or: ollama pull mistral, llama3.2, qwen2.5
```

### Q: "Embedding model not found"

**A:** Install the embedding model:
```bash
ollama pull nomic-embed-text
```

### Q: "No documents found"

**A:** Check your document directory:
```bash
ls docs/  # Should show your files
# If empty, add files: cp *.pdf docs/
```

### Q: "Index not found"

**A:** Build the index first:
```bash
vector-bot ingest
```

## Models and Performance

### Q: Which AI model should I use?

**A:** Recommendations by use case:
- **General use**: `llama3.1` (good balance)
- **Latest features**: `llama3.2` 
- **Speed priority**: `mistral`
- **Coding tasks**: `codellama`

```bash
# Set your preferred model
export OLLAMA_CHAT_MODEL=llama3.1
```

### Q: How do I make queries faster?

**A:** Several options:
- Use fewer context chunks: `--k 2`
- Use a faster model: `OLLAMA_CHAT_MODEL=mistral`
- Reduce document size (split large files)
- Use SSD storage for index

### Q: How do I get better answers?

**A:** Try these approaches:
- Use more context: `--k 8`
- Be more specific in questions
- Use keywords from your documents
- Check sources: `--show-sources`

### Q: Why are my large files being skipped?

**A:** Files over 20MB are automatically skipped. Solutions:
- Split large PDFs into smaller files
- Extract key sections manually
- Convert to text format if possible

## Configuration

### Q: How do I change where documents are stored?

**A:** Set the `DOCS_DIR` variable:
```bash
export DOCS_DIR=~/my-documents
# Or create .env file with: DOCS_DIR=~/my-documents
```

### Q: Can I use a different Ollama server?

**A:** Yes, set the URL:
```bash
export OLLAMA_BASE_URL=http://192.168.1.100:11434
```

### Q: How do I see my current configuration?

**A:** Use the config info command:
```bash
vector-bot --config-info
```

### Q: How do I use different settings for different projects?

**A:** Use project-specific `.env` files:
```bash
# Project A
cd project-a
echo "DOCS_DIR=./project-a-docs" > .env
echo "OLLAMA_CHAT_MODEL=llama3.1" >> .env

# Project B  
cd ../project-b
echo "DOCS_DIR=./project-b-docs" > .env
echo "OLLAMA_CHAT_MODEL=mistral" >> .env
```

## Advanced Questions

### Q: Can Vector Bot work in a corporate environment?

**A:** Yes! Vector Bot:
- Runs entirely on-premises
- Makes no external network calls
- Supports enterprise deployment patterns
- Can integrate with existing infrastructure

### Q: How do I backup my data?

**A:** Backup your **documents**, not the index:
```bash
# Backup documents (important)
tar -czf my-docs-backup.tar.gz docs/

# Index can be rebuilt
rm -rf index_storage/
vector-bot ingest
```

### Q: Can I run multiple Vector Bot instances?

**A:** Yes, use different directories:
```bash
# Instance 1
DOCS_DIR=./project1/docs INDEX_DIR=./project1/index vector-bot ingest

# Instance 2  
DOCS_DIR=./project2/docs INDEX_DIR=./project2/index vector-bot ingest
```

### Q: How do I integrate Vector Bot with my application?

**A:** Several approaches:
- **Command line**: Call via subprocess
- **REST wrapper**: Create HTTP API wrapper
- **Direct integration**: Use the Python package

Example Python integration:
```python
import subprocess
result = subprocess.run(['vector-bot', 'query', 'question'], 
                       capture_output=True, text=True)
answer = result.stdout
```

### Q: Can I use Vector Bot for sensitive documents?

**A:** Yes! Vector Bot is designed for privacy:
- All processing happens locally
- No data sent to external services
- No telemetry or tracking
- You control all data and models

### Q: How do I update Vector Bot?

**A:** Depends on installation method:

**npm:**
```bash
npm update -g @joshuaramirez/vector-bot
```

**pip:**
```bash
pip install --upgrade vector-bot
```

**Executable:** Download new version from releases page

## Error Messages

### Q: What does "Connection timeout" mean?

**A:** Vector Bot can't reach Ollama in time:
- Check if Ollama is running: `ollama serve`
- Increase timeout: `export REQUEST_TIMEOUT=120`
- Check network connectivity

### Q: What does "Permission denied" mean?

**A:** File or directory permission issue:
```bash
# Make executable (Linux/macOS)
chmod +x vector-bot

# Fix directory permissions
chmod -R +r docs/
chmod -R +w index_storage/
```

### Q: What does "Model loading failed" mean?

**A:** The AI model couldn't load:
- Check available memory (models need several GB)
- Try a smaller model: `export OLLAMA_CHAT_MODEL=llama3.1`
- Restart Ollama: `ollama serve`

## Getting More Help

### Q: Where can I find more detailed help?

**A:** Check these resources:

**For specific problems:**
- [Troubleshooting Guide](../user/troubleshooting.md) - Step-by-step problem solving

**For learning:**
- [Getting Started](../user/getting-started.md) - First-time setup
- [Basic Usage](../user/basic-usage.md) - Daily workflows
- [Examples](../user/examples.md) - Real-world use cases

**For configuration:**
- [Basic Configuration](../user/basic-configuration.md) - Essential settings
- [Configuration Variables](configuration-vars.md) - Complete reference

**For advanced users:**
- [Advanced Features](../user/advanced-features.md) - Power user capabilities
- [Admin Configuration](../admin/configuration.md) - Enterprise deployment

### Q: How do I report a bug or request a feature?

**A:** Check the project documentation for contribution guidelines:
- [Contributing Guide](../../CONTRIBUTING.md)
- [Security Policy](../../SECURITY.md)

### Q: Is there a community or forum?

**A:** Check the project repository for:
- Issues and discussions
- Community contributions
- Latest updates and releases

## Quick Reference

### Essential Commands
```bash
vector-bot doctor                    # Check system health
vector-bot ingest                    # Index documents
vector-bot query "your question"     # Ask questions
vector-bot --config-info             # Show configuration
```

### Common Environment Variables
```bash
DOCS_DIR=./documents                 # Document location
OLLAMA_CHAT_MODEL=llama3.1          # AI model to use
SIMILARITY_TOP_K=4                   # Context chunks
OLLAMA_BASE_URL=http://localhost:11434  # Ollama server
```

### Quick Troubleshooting
1. **Run** `vector-bot doctor` first
2. **Check** if Ollama is running: `ollama serve`
3. **Verify** models are installed: `ollama list`
4. **Confirm** documents exist: `ls docs/`
5. **Build** index if needed: `vector-bot ingest`

---

**Can't find your question?** Check the [Troubleshooting Guide](../user/troubleshooting.md) or [Glossary](glossary.md) for more detailed information.