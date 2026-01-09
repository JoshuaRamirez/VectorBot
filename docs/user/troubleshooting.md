---
title: Troubleshooting Guide
description: Comprehensive troubleshooting guide for Vector Bot with step-by-step solutions
audience: user
level: intermediate
keywords: [troubleshooting, problems, solutions, errors, debug, fix]
related_docs: [installation.md, basic-configuration.md, ../reference/faq.md, basic-usage.md]
---

# Troubleshooting Guide

This guide provides step-by-step solutions for common Vector Bot issues. Start with the diagnostic tools, then find your specific issue below.

## Quick Diagnostic Tools

Before diving into specific issues, use these tools to understand what's happening:

### 1. System Health Check

```bash
# Basic health check
vector-bot doctor

# Detailed health check
vector-bot doctor --verbose
```

### 2. Configuration Check

```bash
# Show current configuration
vector-bot --config-info

# Show configuration for specific environment
vector-bot --config-info --env production
```

### 3. Version Information

```bash
# Check Vector Bot version
vector-bot --version

# Check Ollama version
ollama --version
```

## Installation Issues

### Issue: "Command not found: vector-bot"

This means Vector Bot isn't installed properly or isn't in your PATH.

**Diagnosis:**
```bash
# Check if installed via npm
npm list -g @joshuaramirez/vector-bot

# Check if installed via pip
pip show vector-bot

# Check PATH
echo $PATH
```

**Solutions:**

**For npm installation:**
```bash
# Reinstall globally
npm install -g @joshuaramirez/vector-bot

# Or run without installing
npx @joshuaramirez/vector-bot --version
```

**For pip installation:**
```bash
# Reinstall
pip install vector-bot

# If using --user install, ensure user bin directory is in PATH
python -m site --user-base
# Add ~/.local/bin to PATH (Linux/macOS) or similar for Windows
```

**For executable installation:**
```bash
# Use full path
/path/to/vector-bot --version

# Or add to PATH
export PATH="$PATH:/path/to/vector-bot-directory"
```

### Issue: "Permission denied" (Linux/macOS)

**Solution:**
```bash
# Make executable file executable
chmod +x vector-bot

# If installed in system directory, use sudo
sudo chmod +x /usr/local/bin/vector-bot
```

### Issue: Python version conflicts

**Diagnosis:**
```bash
# Check Python version
python --version
python3 --version

# Check which Python pip uses
pip --version
```

**Solution:**
```bash
# Use specific Python version
python3.10 -m pip install vector-bot

# Or use virtual environment
python -m venv vector-bot-env
source vector-bot-env/bin/activate  # Linux/macOS
vector-bot-env\Scripts\activate     # Windows
pip install vector-bot
```

## Ollama Connection Issues

### Issue: "Ollama server not running"

This is the most common issue - Vector Bot can't connect to Ollama.

**Diagnosis:**
```bash
# Test Ollama connection directly
curl http://localhost:11434/api/tags

# Check if Ollama process is running
ps aux | grep ollama  # Linux/macOS
tasklist | findstr ollama  # Windows
```

**Solutions:**

**Start Ollama:**
```bash
# Start Ollama server
ollama serve

# Or start as background service (Linux/macOS)
nohup ollama serve &

# Windows: Start as service or in separate PowerShell window
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
```

**Check port conflicts:**
```bash
# Check what's using port 11434
netstat -an | grep 11434  # Linux/macOS
netstat -an | findstr 11434  # Windows

# If different port, update configuration
export OLLAMA_BASE_URL=http://localhost:YOUR_PORT
```

**Firewall issues:**
```bash
# Add firewall exception (Linux)
sudo ufw allow 11434

# Windows: Check Windows Defender Firewall settings
```

### Issue: "Connection refused" or timeout

**Diagnosis:**
```bash
# Test specific URL
curl -v http://localhost:11434/api/tags

# Check Ollama logs
ollama logs  # If available
```

**Solutions:**

**Network configuration:**
```bash
# Try different base URL formats
export OLLAMA_BASE_URL=http://127.0.0.1:11434
export OLLAMA_BASE_URL=http://localhost:11434

# For Docker setups
export OLLAMA_BASE_URL=http://host.docker.internal:11434
```

**Increase timeout:**
```bash
# Set longer timeout in configuration
export REQUEST_TIMEOUT=120

# Or create .env file
echo "REQUEST_TIMEOUT=120.0" > .env
```

## Model Issues

### Issue: "No suitable chat model found"

Vector Bot can't find an AI model to use for generating answers.

**Diagnosis:**
```bash
# List installed models
ollama list

# Check what Vector Bot is looking for
vector-bot doctor --verbose
```

**Solutions:**

**Install a chat model:**
```bash
# Install recommended model
ollama pull llama3.1

# Or alternative models
ollama pull llama3.2
ollama pull mistral
ollama pull qwen2.5
```

**Set specific model:**
```bash
# Set model explicitly
export OLLAMA_CHAT_MODEL=llama3.1
vector-bot doctor

# Or in .env file
echo "OLLAMA_CHAT_MODEL=llama3.1" > .env
```

### Issue: "Embedding model not found"

Vector Bot needs an embedding model to create searchable indexes.

**Diagnosis:**
```bash
# Check for embedding models
ollama list | grep embed
```

**Solution:**
```bash
# Install default embedding model
ollama pull nomic-embed-text

# Or alternative
ollama pull mxbai-embed-large
export OLLAMA_EMBED_MODEL=mxbai-embed-large
```

### Issue: Model download or loading errors

**Diagnosis:**
```bash
# Check disk space
df -h  # Linux/macOS
dir  # Windows

# Check available memory
free -h  # Linux
top  # macOS
tasklist  # Windows
```

**Solutions:**

**Free up space:**
```bash
# Remove unused models
ollama rm old-model-name

# Check model sizes
ollama list
```

**Memory issues:**
```bash
# Use smaller model
ollama pull llama3.1  # Instead of larger models
export OLLAMA_CHAT_MODEL=llama3.1
```

## Document and Index Issues

### Issue: "No documents found"

Vector Bot can't find documents to process.

**Diagnosis:**
```bash
# Check document directory
ls -la docs/  # Linux/macOS
dir docs\  # Windows

# Check configuration
vector-bot --config-info | grep DOCS_DIR
```

**Solutions:**

**Fix document directory:**
```bash
# Create directory if missing
mkdir docs

# Add some test documents
echo "Test content" > docs/test.txt
cp ~/Documents/*.pdf docs/

# Verify path in configuration
export DOCS_DIR=./docs
```

**Check file permissions:**
```bash
# Fix permissions (Linux/macOS)
chmod -R +r docs/
```

### Issue: "Index not found" or "Failed to load index"

Vector Bot can't find or load the search index.

**Diagnosis:**
```bash
# Check index directory
ls -la index_storage/  # Linux/macOS
dir index_storage\  # Windows

# Check configuration
vector-bot --config-info | grep INDEX_DIR
```

**Solutions:**

**Rebuild index:**
```bash
# Remove corrupted index
rm -rf index_storage/  # Linux/macOS
rmdir /s index_storage  # Windows

# Rebuild
vector-bot ingest
```

**Fix permissions:**
```bash
# Ensure write permissions (Linux/macOS)
chmod -R +w index_storage/
```

### Issue: "Large files skipped"

Files over 20MB are automatically skipped during ingestion.

**Solutions:**

**Split large files:**
```bash
# For PDFs, split into smaller parts
# Use PDF tools or online splitters

# For text files
split -b 15M large-file.txt split-file-
```

**Alternative approaches:**
- Convert large PDFs to multiple smaller files
- Extract key sections manually
- Use markdown format for better processing

### Issue: Documents not updating after changes

**Diagnosis:**
```bash
# Check if documents were actually modified
ls -lt docs/

# Check ingestion output
vector-bot ingest --verbose
```

**Solution:**
```bash
# Force complete re-indexing
rm -rf index_storage/
vector-bot ingest
```

## Query and Performance Issues

### Issue: Poor or irrelevant answers

The AI is giving unhelpful responses.

**Diagnosis:**
```bash
# Test with show-sources to see what documents were used
vector-bot query "your question" --show-sources

# Try with more context
vector-bot query "your question" --k 8
```

**Solutions:**

**Improve query phrasing:**
```bash
# Be more specific
# Instead of: "What does this say?"
# Try: "What are the project requirements?"

# Use keywords from your documents
# If documents mention "API authentication", use that term
```

**Adjust context:**
```bash
# More context for complex questions
vector-bot query "complex question" --k 8

# Less context for simple questions
vector-bot query "simple question" --k 2
```

**Check document quality:**
- Ensure documents are readable (not scanned images)
- Use descriptive filenames
- Include context in documents

### Issue: Slow query performance

Queries take too long to complete.

**Diagnosis:**
```bash
# Time a query
time vector-bot query "test question"

# Check system resources
top  # Linux/macOS
taskmgr  # Windows
```

**Solutions:**

**Reduce context:**
```bash
# Use fewer chunks
vector-bot query "question" --k 2
```

**Use faster model:**
```bash
# Switch to faster model
export OLLAMA_CHAT_MODEL=llama3.1
vector-bot query "question"
```

**Optimize index:**
```bash
# Rebuild with smaller batch size
export EMBED_BATCH_SIZE=5
rm -rf index_storage/
vector-bot ingest
```

### Issue: Memory errors or crashes

**Diagnosis:**
```bash
# Check available memory
free -h  # Linux
vm_stat  # macOS

# Check error messages in terminal
vector-bot query "test" --verbose
```

**Solutions:**

**Reduce memory usage:**
```bash
# Smaller embedding batch size
export EMBED_BATCH_SIZE=3

# Fewer similarity chunks
export SIMILARITY_TOP_K=3

# Use lighter model
export OLLAMA_CHAT_MODEL=llama3.1
```

## Configuration Issues

### Issue: Configuration not being applied

**Diagnosis:**
```bash
# Check configuration precedence
vector-bot --config-info

# Check environment variables
env | grep -E "(RAG_|DOCS_|OLLAMA_)"
```

**Solutions:**

**Check configuration priority:**
1. Command-line environment variables (highest)
2. Shell environment variables
3. .env file in current directory
4. Environment profile files
5. Built-in defaults (lowest)

**Set configuration explicitly:**
```bash
# Set for single command
DOCS_DIR=/custom/path vector-bot ingest

# Set for session
export DOCS_DIR=/custom/path
vector-bot ingest
```

### Issue: Environment profile not working

**Diagnosis:**
```bash
# Check if profile file exists
ls configs/production.env

# Check environment setting
echo $RAG_ENV
```

**Solution:**
```bash
# Set environment explicitly
export RAG_ENV=production
vector-bot --config-info

# Or use command-line flag
vector-bot --env production --config-info
```

## Error Message Reference

### Common Error Messages and Solutions

| Error Message | Likely Cause | Quick Fix |
|---------------|--------------|-----------|
| "Command not found: vector-bot" | Not installed or not in PATH | Reinstall or check PATH |
| "Ollama server not running" | Ollama not started | Run `ollama serve` |
| "No suitable chat model found" | No AI models installed | Run `ollama pull llama3.1` |
| "Embedding model not found" | No embedding model | Run `ollama pull nomic-embed-text` |
| "No documents found" | Empty docs directory | Add files to `docs/` |
| "Index not found" | Haven't built index | Run `vector-bot ingest` |
| "Connection timeout" | Network or performance issue | Increase `REQUEST_TIMEOUT` |
| "Permission denied" | File permissions issue | Fix permissions with `chmod` |

## Advanced Troubleshooting

### Enable Debug Logging

```bash
# Enable verbose output
export LOG_LEVEL=DEBUG
export ENABLE_VERBOSE_OUTPUT=true

# Run with verbose flags
vector-bot doctor --verbose
vector-bot ingest --verbose
vector-bot query "test" --verbose
```

### Network Debugging

```bash
# Test Ollama API directly
curl -X POST http://localhost:11434/api/generate \
     -H "Content-Type: application/json" \
     -d '{"model": "llama3.1", "prompt": "Hello", "stream": false}'
```

### File System Debugging

```bash
# Check disk space
df -h

# Check file permissions
ls -la docs/ index_storage/

# Check file types
file docs/*
```

### Process Debugging

```bash
# Check running processes
ps aux | grep -E "(ollama|vector-bot)"

# Check system resources
htop  # Linux
Activity Monitor  # macOS
Task Manager  # Windows
```

## Getting Additional Help

If you're still having issues after trying these solutions:

### 1. Collect Debug Information

```bash
# Create debug report
echo "=== Vector Bot Debug Report ===" > debug-report.txt
echo "Date: $(date)" >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Version Information ===" >> debug-report.txt
vector-bot --version >> debug-report.txt
ollama --version >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Configuration ===" >> debug-report.txt
vector-bot --config-info >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Health Check ===" >> debug-report.txt
vector-bot doctor --verbose >> debug-report.txt
echo "" >> debug-report.txt

echo "=== Environment ===" >> debug-report.txt
env | grep -E "(RAG_|DOCS_|OLLAMA_)" >> debug-report.txt
```

### 2. Check Documentation

- **[FAQ](../reference/faq.md)** - Common questions and answers
- **[Configuration Guide](basic-configuration.md)** - Configuration details
- **[Installation Guide](installation.md)** - Installation troubleshooting

### 3. Common Solutions Checklist

Before seeking help, verify you've tried:

- [ ] `vector-bot doctor` shows all checks passing
- [ ] Ollama is running (`ollama serve`)
- [ ] At least one chat model is installed (`ollama list`)
- [ ] Documents exist in the docs directory
- [ ] Index has been built (`vector-bot ingest`)
- [ ] Configuration is valid (`vector-bot --config-info`)

### 4. Systematic Problem Solving

Use this approach for complex issues:

1. **Isolate**: Test with minimal configuration
2. **Reproduce**: Can you consistently reproduce the issue?
3. **Document**: Note exact error messages and steps
4. **Test**: Try each solution one at a time
5. **Verify**: Confirm the fix works before moving on

---

**Remember**: Most Vector Bot issues are related to Ollama connectivity or missing models. Start with `vector-bot doctor` and work through the diagnostics systematically.

**Still stuck?** Check the [FAQ](../reference/faq.md) for quick answers to common questions.