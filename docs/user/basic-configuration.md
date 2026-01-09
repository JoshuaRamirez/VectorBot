---
title: Basic Configuration Guide
description: Essential configuration settings for Vector Bot users
audience: user
level: beginner
keywords: [configuration, settings, customization, environment, models, paths]
related_docs: [installation.md, getting-started.md, basic-usage.md, ../admin/configuration.md]
---

# Basic Configuration Guide

This guide covers the essential configuration settings for Vector Bot. For advanced configuration, see the [Admin Configuration Guide](../admin/configuration.md).

## Quick Configuration Overview

Vector Bot works out-of-the-box with sensible defaults, but you can customize these key settings:

| Setting | Purpose | Default | Common Values |
|---------|---------|---------|---------------|
| `DOCS_DIR` | Where your documents are stored | `./docs` | `./documents`, `~/Documents/research` |
| `OLLAMA_CHAT_MODEL` | AI model for answers | *auto-detect* | `llama3.1`, `mistral` |
| `SIMILARITY_TOP_K` | Context chunks per query | `4` | `2-12` depending on complexity |
| `OLLAMA_BASE_URL` | Ollama server location | `http://localhost:11434` | Different ports or remote servers |

## Configuration Methods

You can configure Vector Bot in three ways (in order of priority):

1. **Command-line environment variables** (highest priority)
2. **`.env` file** in your working directory
3. **Built-in defaults** (lowest priority)

## Method 1: Environment Variables

Set configuration for the current session:

### Temporary Configuration (Current Session)

```bash
# Set for current terminal session
export DOCS_DIR=~/Documents/research
export OLLAMA_CHAT_MODEL=llama3.1
export SIMILARITY_TOP_K=6

# Now all Vector Bot commands use these settings
vector-bot doctor
vector-bot ingest
vector-bot query "What are the main topics?"
```

### One-Time Configuration (Single Command)

```bash
# Set for just one command
SIMILARITY_TOP_K=8 vector-bot query "complex question"
DOCS_DIR=/custom/path vector-bot ingest
OLLAMA_CHAT_MODEL=mistral vector-bot query "test"
```

### Windows Environment Variables

**PowerShell:**
```powershell
# Set for session
$env:DOCS_DIR = "C:\MyDocuments"
$env:OLLAMA_CHAT_MODEL = "llama3.1"

# Set for single command
$env:SIMILARITY_TOP_K = "8"; vector-bot query "question"
```

**Command Prompt:**
```batch
rem Set for session
set DOCS_DIR=C:\MyDocuments
set OLLAMA_CHAT_MODEL=llama3.1

rem Use the settings
vector-bot doctor
```

## Method 2: Configuration File (.env)

Create a `.env` file in your working directory for persistent settings:

### Creating a Configuration File

```bash
# Create configuration file
cat > .env << EOF
# Document settings
DOCS_DIR=./my-documents
INDEX_DIR=./my-index

# Model settings
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text

# Query settings
SIMILARITY_TOP_K=6

# Ollama connection
OLLAMA_BASE_URL=http://localhost:11434
EOF
```

### Example Configuration Files

#### Personal Research Setup
```bash
# .env for research work
DOCS_DIR=~/Research/Papers
INDEX_DIR=~/Research/vector-index
OLLAMA_CHAT_MODEL=llama3.2
SIMILARITY_TOP_K=8
LOG_LEVEL=INFO
```

#### Business Documents Setup
```bash
# .env for business documents
DOCS_DIR=./company-docs
INDEX_DIR=./company-index
OLLAMA_CHAT_MODEL=mistral
SIMILARITY_TOP_K=6
REQUEST_TIMEOUT=90
```

#### Development Setup
```bash
# .env for development work
DOCS_DIR=./project-docs
INDEX_DIR=./project-index
OLLAMA_CHAT_MODEL=llama3.1
SIMILARITY_TOP_K=4
LOG_LEVEL=DEBUG
ENABLE_VERBOSE_OUTPUT=true
```

## Essential Settings

### Document Directory (DOCS_DIR)

Where Vector Bot looks for your documents to index.

```bash
# Use relative path (from where you run vector-bot)
DOCS_DIR=./documents

# Use absolute path
DOCS_DIR=/home/user/research-papers  # Linux/macOS
DOCS_DIR=C:\Documents\Research        # Windows

# Use home directory shortcut (Unix)
DOCS_DIR=~/Documents/vector-bot-docs
```

**Tips:**
- Create the directory before running `vector-bot ingest`
- Use descriptive names like `./research-docs` or `./project-files`
- Avoid spaces in paths, or use quotes: `DOCS_DIR="/path/with spaces"`

### Index Storage Directory (INDEX_DIR)

Where Vector Bot stores the searchable index.

```bash
# Default location
INDEX_DIR=./index_storage

# Custom location
INDEX_DIR=./my-project-index
INDEX_DIR=/data/vector-indexes/project-alpha
```

**Tips:**
- Keep on fast storage (SSD) for better performance
- Back up your documents, not the index (index can be rebuilt)
- Each project should have its own index directory

### AI Model Selection (OLLAMA_CHAT_MODEL)

Which AI model to use for generating answers.

```bash
# Let Vector Bot auto-detect (recommended for beginners)
# OLLAMA_CHAT_MODEL=  # Leave unset

# Use specific model
OLLAMA_CHAT_MODEL=llama3.1    # Good balance of speed and quality
OLLAMA_CHAT_MODEL=llama3.2    # Latest model
OLLAMA_CHAT_MODEL=mistral     # Fast model
OLLAMA_CHAT_MODEL=qwen2.5     # Alternative model
```

**Choosing a model:**
- **New users**: Leave unset for auto-detection
- **Speed priority**: `llama3.1` or `mistral`
- **Quality priority**: `llama3.2` or `llama3.3`
- **Must match installed models**: Check with `ollama list`

### Context Amount (SIMILARITY_TOP_K)

How many document chunks to use when answering questions.

```bash
SIMILARITY_TOP_K=2    # Minimal context - for simple facts
SIMILARITY_TOP_K=4    # Default - good for most questions
SIMILARITY_TOP_K=8    # More context - for complex questions
SIMILARITY_TOP_K=12   # Maximum context - for comprehensive analysis
```

**Choosing context amount:**
- **Simple facts**: 2-3 chunks
- **General questions**: 4-6 chunks (default)
- **Complex analysis**: 8-12 chunks
- **More chunks = slower but more comprehensive answers**

## Common Configuration Scenarios

### Scenario 1: Personal Research

You're researching a topic with academic papers and notes.

```bash
# .env file
DOCS_DIR=~/Research/ML-Healthcare
INDEX_DIR=~/Research/ML-Healthcare-index
OLLAMA_CHAT_MODEL=llama3.2
SIMILARITY_TOP_K=8
LOG_LEVEL=INFO
```

**Usage:**
```bash
# Add papers and notes
cp ~/Downloads/*.pdf ~/Research/ML-Healthcare/
cp ~/Notes/meeting-*.md ~/Research/ML-Healthcare/

# Index and query
vector-bot ingest
vector-bot query "What methodologies are used across these papers?" --show-sources
```

### Scenario 2: Work Documentation

You're indexing company documentation and guides.

```bash
# .env file
DOCS_DIR=./work-docs
INDEX_DIR=./work-index
OLLAMA_CHAT_MODEL=mistral
SIMILARITY_TOP_K=6
REQUEST_TIMEOUT=60
```

**Usage:**
```bash
# Add documentation
cp ~/Work/Docs/*.pdf ./work-docs/
cp ~/Work/Guides/*.md ./work-docs/

# Index and query
vector-bot ingest
vector-bot query "What is the deployment process?"
vector-bot query "Who do I contact for database access?"
```

### Scenario 3: Learning and Study

You're studying multiple subjects with textbooks and notes.

```bash
# .env file
DOCS_DIR=./study-materials
INDEX_DIR=./study-index
OLLAMA_CHAT_MODEL=llama3.1
SIMILARITY_TOP_K=4
ENABLE_VERBOSE_OUTPUT=false
```

**Usage:**
```bash
# Organize by subject
mkdir -p study-materials/{math,physics,programming}
cp textbooks/math*.pdf study-materials/math/
cp textbooks/physics*.pdf study-materials/physics/

# Index and study
vector-bot ingest
vector-bot query "Explain the concept of derivatives"
vector-bot query "What is quantum entanglement?"
```

### Scenario 4: Multi-Project Setup

You work on different projects with separate document sets.

```bash
# Create project structure
mkdir -p projects/{alpha,beta,gamma}

# Project Alpha
cat > projects/alpha/.env << EOF
DOCS_DIR=./docs
INDEX_DIR=./index
OLLAMA_CHAT_MODEL=llama3.1
SIMILARITY_TOP_K=4
EOF

# Project Beta
cat > projects/beta/.env << EOF
DOCS_DIR=./docs  
INDEX_DIR=./index
OLLAMA_CHAT_MODEL=mistral
SIMILARITY_TOP_K=6
EOF
```

**Usage:**
```bash
# Work on Project Alpha
cd projects/alpha
cp ~/ProjectAlpha/docs/* ./docs/
vector-bot ingest
vector-bot query "What are Alpha's requirements?"

# Switch to Project Beta
cd ../beta
cp ~/ProjectBeta/docs/* ./docs/
vector-bot ingest
vector-bot query "What is Beta's timeline?"
```

## Viewing Current Configuration

### Check All Settings

```bash
# Show current configuration
vector-bot --config-info
```

**Example output:**
```
Configuration Summary:
  Environment: development
  Executable Directory: /usr/local/bin
  Documents Directory: ./docs (exists: yes, files: 12)
  Index Directory: ./index_storage (exists: yes)
  
  Ollama Configuration:
    Base URL: http://localhost:11434
    Chat Model: llama3.1
    Embedding Model: nomic-embed-text
  
  Query Settings:
    Similarity Top K: 4
    Request Timeout: 60.0s
```

### Check Specific Settings

```bash
# Check environment variables
env | grep -E "(DOCS_DIR|OLLAMA|SIMILARITY)"

# Check if .env file exists and its contents
cat .env
```

## Validating Configuration

### System Health Check

```bash
# Verify all settings work together
vector-bot doctor

# Detailed health check
vector-bot doctor --verbose
```

**Expected healthy output:**
```
✓ Ollama server is running at http://localhost:11434
✓ Chat model available: llama3.1
✓ Embedding model available: nomic-embed-text
✓ Documents directory exists: ./docs (5 documents)
✓ Index directory exists: ./index_storage
✓ Configuration is valid
```

### Test Configuration

```bash
# Test with a simple document and query
echo "Test document about Vector Bot configuration" > docs/test.txt
vector-bot ingest
vector-bot query "What is this document about?"
```

## Configuration Best Practices

### 1. Start Simple

```bash
# Begin with minimal configuration
DOCS_DIR=./docs
OLLAMA_CHAT_MODEL=llama3.1
```

### 2. Use Project-Specific Configurations

```bash
# Each project gets its own .env file
project-a/
├── .env          # Project A specific settings
├── docs/         # Project A documents
└── index_storage/ # Project A index

project-b/
├── .env          # Project B specific settings  
├── docs/         # Project B documents
└── index_storage/ # Project B index
```

### 3. Document Your Configuration

```bash
# Add comments to .env files
cat > .env << EOF
# Project: Customer Support Documentation
# Updated: 2024-01-15
# Purpose: Index help articles and FAQs

# Document location
DOCS_DIR=./support-docs

# Fast model for quick answers
OLLAMA_CHAT_MODEL=llama3.1

# Standard context for support queries
SIMILARITY_TOP_K=4
EOF
```

### 4. Version Control Considerations

```bash
# Create .env.example for sharing (without sensitive data)
cp .env .env.example

# Add .env to .gitignore to avoid committing personal paths
echo ".env" >> .gitignore
```

## Common Configuration Mistakes

### Issue: Paths with spaces

```bash
# Wrong - will cause errors
DOCS_DIR=~/My Documents/Research

# Right - use quotes
DOCS_DIR="~/My Documents/Research"
```

### Issue: Relative vs absolute paths

```bash
# Be aware of where relative paths resolve
DOCS_DIR=./docs  # Relative to where you run vector-bot

# Use absolute paths if unsure
DOCS_DIR=/full/path/to/documents
```

### Issue: Model not installed

```bash
# Setting model that doesn't exist
OLLAMA_CHAT_MODEL=nonexistent-model

# Check available models first
ollama list

# Install model if needed
ollama pull llama3.1
```

## Quick Setup Templates

### Research Template

```bash
mkdir research-project
cd research-project

cat > .env << EOF
DOCS_DIR=./research-docs
INDEX_DIR=./research-index
OLLAMA_CHAT_MODEL=llama3.2
SIMILARITY_TOP_K=8
EOF

mkdir research-docs
echo "Setup complete! Add your research papers to research-docs/"
```

### Business Template

```bash
mkdir business-docs-project
cd business-docs-project

cat > .env << EOF
DOCS_DIR=./business-docs
INDEX_DIR=./business-index
OLLAMA_CHAT_MODEL=mistral
SIMILARITY_TOP_K=6
REQUEST_TIMEOUT=90
EOF

mkdir business-docs
echo "Setup complete! Add your business documents to business-docs/"
```

---

## What's Next?

Once you have your basic configuration working:

- **[Basic Usage](basic-usage.md)** - Learn essential commands and workflows
- **[Advanced Features](advanced-features.md)** - Multi-environment setups and automation  
- **[Admin Configuration](../admin/configuration.md)** - Advanced configuration management
- **[Examples](examples.md)** - Real-world usage scenarios

**Having configuration issues?** Check the [Troubleshooting Guide](troubleshooting.md)