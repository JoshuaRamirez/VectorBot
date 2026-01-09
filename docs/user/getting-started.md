---
title: Getting Started with Vector Bot
description: Quick start guide to get you up and running with Vector Bot in 10 minutes
audience: user
level: beginner
keywords: [getting-started, first-time, setup, quick-start, tutorial]
related_docs: [installation.md, basic-usage.md, basic-configuration.md, troubleshooting.md]
---

# Getting Started with Vector Bot

Welcome to Vector Bot! This guide will get you asking questions about your documents in under 10 minutes.

## What is Vector Bot?

Vector Bot is a powerful tool that lets you ask questions about your documents using AI, all while keeping everything on your computer. No internet connection required, no data sent to the cloud - everything runs locally.

### What Can You Do With It?

- **Query your documents**: Ask natural language questions about PDFs, text files, markdown files
- **Build a knowledge base**: Index technical documentation, research papers, notes
- **Private AI assistant**: Get AI-powered answers without sharing sensitive data
- **Offline operation**: Works completely offline once set up

## Prerequisites Check

Before we start, make sure you have:

1. **Vector Bot installed** - see [Installation Guide](installation.md) if not done yet
2. **Ollama running** - we'll verify this in the next step

## Step 1: Verify Your Setup

First, let's make sure everything is working:

```bash
# Check if Vector Bot is installed
vector-bot --version

# Check system health
vector-bot doctor
```

**Expected output:**
```
✓ Ollama server is running at http://localhost:11434
✓ Chat model available: llama3.1
✓ Embedding model available: nomic-embed-text
✓ Configuration is valid
```

### If the Doctor Check Fails

**"Ollama server not running":**
```bash
ollama serve
```

**"No chat models found":**
```bash
ollama pull llama3.1
```

**"Embedding model not found":**
```bash
ollama pull nomic-embed-text
```

Run `vector-bot doctor` again after fixing issues.

## Step 2: Add Your First Document

Let's create a simple document to test with:

```bash
# Create the documents directory
mkdir docs

# Create a test document
cat > docs/test-document.txt << EOF
Vector Bot Project Overview

Vector Bot is a local RAG (Retrieval-Augmented Generation) system that allows users to ask questions about their documents using AI models. The system works entirely offline and uses Ollama for both chat and embedding models.

Key Features:
- 100% local operation
- Support for multiple document formats (PDF, text, markdown, JSON, CSV)
- Persistent vector index for fast queries
- Simple command-line interface
- Multi-environment configuration support

The system consists of three main commands:
1. doctor - checks system health and configuration
2. ingest - processes documents and builds the vector index
3. query - answers questions based on indexed documents

Installation is available through multiple methods: pip package, npm package, or standalone executables for Windows, macOS, and Linux.
EOF
```

**Using your own documents?** Simply copy them to the `docs/` folder:
```bash
# Copy your files
cp ~/Documents/*.pdf docs/
cp ~/Notes/*.md docs/
```

**Supported formats:**
- `.txt` - Plain text files
- `.md` - Markdown files  
- `.pdf` - PDF documents
- `.json` - JSON files
- `.csv` - CSV files

## Step 3: Index Your Documents

Now let's build the searchable index:

```bash
vector-bot ingest
```

**Expected output:**
```
Loading documents from ./docs...
Found 1 documents to process
Processing documents...
Building vector index...
✓ Index saved to ./index_storage
✓ Indexed 8 chunks from 1 documents
```

**What just happened?**
- Vector Bot read all files in your `docs/` folder
- It split the documents into small, searchable chunks
- It created vector embeddings for each chunk
- It stored everything in `index_storage/` for fast retrieval

**Note**: This step only needs to be done once. Re-run when you add new documents.

## Step 4: Ask Your First Questions

Now for the fun part - let's ask some questions!

### Basic Questions

```bash
# Simple question
vector-bot query "What is Vector Bot?"
```

**Expected response:**
```
Vector Bot is a local RAG (Retrieval-Augmented Generation) system that allows users to ask questions about their documents using AI models. The system works entirely offline and uses Ollama for both chat and embedding models.

Key features include 100% local operation, support for multiple document formats, persistent vector index for fast queries, and a simple command-line interface.
```

### More Specific Questions

```bash
# Ask about features
vector-bot query "What document formats are supported?"

# Ask about installation
vector-bot query "How can I install Vector Bot?"

# Ask about commands
vector-bot query "What are the main commands?"
```

### Advanced Query Options

```bash
# Get more context (more chunks from documents)
vector-bot query "Tell me about Vector Bot features" --k 6

# See which documents were used to answer
vector-bot query "What is RAG?" --show-sources
```

## Step 5: Understanding the Output

When you ask a question, Vector Bot:

1. **Searches** your indexed documents for relevant content
2. **Retrieves** the most similar chunks (default: 4 chunks)
3. **Combines** the chunks with your question
4. **Sends** everything to the AI model for a comprehensive answer
5. **Returns** the answer based on your documents

### Query Options Explained

- **Default behavior**: `vector-bot query "question"`
- **More context**: `--k 8` (retrieves 8 chunks instead of 4)
- **Show sources**: `--show-sources` (shows which documents were used)
- **Verbose output**: `--verbose` (shows processing details)

## Step 6: Add More Documents and Update Index

As you add more documents:

```bash
# Add new files to docs/
cp new-research-paper.pdf docs/
cp project-notes.md docs/

# Update the index (safe - won't duplicate existing content)
vector-bot ingest

# Now you can ask questions about all documents
vector-bot query "What does the research paper say about methodology?"
```

## Common Workflows

### Daily Usage Pattern

```bash
# Morning: Add new documents
cp today-notes.md docs/

# Update index
vector-bot ingest

# Ask questions throughout the day
vector-bot query "What were my key insights from today?"
vector-bot query "Find references to the Johnson study"
vector-bot query "Summarize the main findings"
```

### Research Workflow

```bash
# Add research papers
cp ~/Research/Papers/*.pdf docs/

# Index everything
vector-bot ingest

# Research queries
vector-bot query "What studies discuss machine learning in healthcare?" --k 8
vector-bot query "Find papers published after 2020" --show-sources
vector-bot query "Compare methodologies across papers"
```

### Documentation Workflow

```bash
# Add technical docs
cp -r ~/project/docs/* docs/

# Index
vector-bot ingest

# Documentation queries
vector-bot query "How do I set up the development environment?"
vector-bot query "What are the API rate limits?"
vector-bot query "Show examples of authentication"
```

## Tips for Better Results

### 1. Be Specific in Your Questions

**Good**: "What is the authentication process for the API?"
**Better**: "How do I authenticate API requests using tokens?"

### 2. Use Keywords from Your Documents

If your documents mention "JWT tokens", use that term in your questions rather than just "tokens".

### 3. Adjust Context When Needed

- For simple facts: default (`--k 4`) is fine
- For complex topics: use more context (`--k 8`)
- For comprehensive analysis: use maximum context (`--k 12`)

### 4. Use Document Organization

```bash
# Organize by topic
docs/
├── research/
│   ├── paper-1.pdf
│   └── paper-2.pdf
├── notes/
│   ├── meeting-notes.md
│   └── ideas.md
└── references/
    └── api-docs.md
```

### 5. Keep Documents Up to Date

- Remove outdated documents from `docs/`
- Re-run `vector-bot ingest` after changes
- Use descriptive filenames

## What's Next?

Now that you have Vector Bot working, explore these areas:

### Immediate Next Steps
1. **[Basic Usage](basic-usage.md)** - Learn all the essential commands and workflows
2. **[Basic Configuration](basic-configuration.md)** - Customize settings for your needs
3. **[Examples](examples.md)** - See real-world usage patterns

### When You're Ready for More
4. **[Advanced Features](advanced-features.md)** - Power user capabilities
5. **[Troubleshooting](troubleshooting.md)** - Solutions for common issues
6. **[FAQ](../reference/faq.md)** - Quick answers to common questions

### If You Have Issues
- **[Troubleshooting Guide](troubleshooting.md)** - Step-by-step problem solving
- **[FAQ](../reference/faq.md)** - Common questions and quick answers

## Quick Reference

```bash
# Essential commands
vector-bot doctor                      # Check system health
vector-bot ingest                      # Index documents  
vector-bot query "your question"       # Ask questions
vector-bot --config-info               # Show configuration

# Useful options
vector-bot query "question" --k 6 --show-sources
vector-bot ingest --verbose
vector-bot doctor --verbose
```

---

**Congratulations!** You've successfully set up Vector Bot and asked your first questions. The system is now ready to help you explore your documents using natural language queries.

**Need help?** Check the [Troubleshooting Guide](troubleshooting.md) or [FAQ](../reference/faq.md).