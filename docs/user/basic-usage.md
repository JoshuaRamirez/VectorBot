---
title: Basic Usage Guide
description: Essential commands, workflows, and daily usage patterns for Vector Bot
audience: user
level: beginner
keywords: [basic-usage, commands, workflow, daily-usage, cli]
related_docs: [getting-started.md, advanced-features.md, basic-configuration.md, troubleshooting.md]
---

# Basic Usage Guide

This guide covers the essential commands and workflows for daily use of Vector Bot. Once you've completed [Getting Started](getting-started.md), this guide will help you become productive with Vector Bot.

## Core Commands Overview

Vector Bot has three main commands:

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `doctor` | System health check | Before starting work, troubleshooting |
| `ingest` | Index documents | When adding/updating documents |
| `query` | Ask questions | Regular querying of your documents |

## The Doctor Command

Use `doctor` to check that everything is working properly.

### Basic Health Check

```bash
vector-bot doctor
```

**Expected output:**
```
✓ Ollama server is running at http://localhost:11434
✓ Chat model available: llama3.1
✓ Embedding model available: nomic-embed-text
✓ Configuration is valid
✓ Documents directory exists: ./docs (3 documents)
✓ Index directory exists: ./index_storage
```

### Verbose Health Check

```bash
vector-bot doctor --verbose
```

**Shows additional details:**
- Full configuration values
- Available models list
- Directory permissions
- Model loading tests

### When to Use Doctor

- **Start of work session**: Verify everything is working
- **After system changes**: New Ollama models, configuration changes
- **Troubleshooting**: First step when something isn't working
- **Before important work**: Ensure reliability

## The Ingest Command

Use `ingest` to process documents and build the searchable index.

### Basic Document Indexing

```bash
vector-bot ingest
```

**What happens:**
1. Scans the documents directory (`./docs` by default)
2. Processes supported file types (PDF, text, markdown, JSON, CSV)
3. Splits documents into searchable chunks
4. Creates vector embeddings for each chunk
5. Stores the index for fast retrieval

**Expected output:**
```
Loading documents from ./docs...
Found 12 documents to process
Processing documents...
├─ user-manual.pdf: 45 chunks
├─ api-docs.md: 23 chunks
├─ meeting-notes.txt: 8 chunks
└─ project-spec.pdf: 67 chunks
Building vector index...
✓ Index saved to ./index_storage
✓ Indexed 143 chunks from 12 documents
```

### Verbose Indexing

```bash
vector-bot ingest --verbose
```

**Shows additional details:**
- File-by-file processing progress
- Chunk creation details
- Embedding generation progress
- Performance metrics

### When to Use Ingest

- **Initial setup**: Index your document collection
- **Adding documents**: After copying new files to `docs/`
- **Updating documents**: After modifying existing documents
- **Index corruption**: Rebuild if queries aren't working properly

### Important Notes About Ingestion

**✅ Safe to re-run**: Running `ingest` multiple times won't duplicate data
**📁 File limits**: Files over 20MB are automatically skipped
**🔄 Incremental**: Only processes new or changed documents
**💾 Persistent**: Index is saved to disk for fast startup

## The Query Command

Use `query` to ask questions about your indexed documents.

### Basic Questions

```bash
vector-bot query "What is the main topic of these documents?"
```

### Question Formats That Work Well

**Factual questions:**
```bash
vector-bot query "What is the API rate limit?"
vector-bot query "Who are the project stakeholders?"
vector-bot query "When was the last meeting held?"
```

**Analytical questions:**
```bash
vector-bot query "What are the key risks mentioned?"
vector-bot query "Compare the different approaches discussed"
vector-bot query "What are the main recommendations?"
```

**Summary questions:**
```bash
vector-bot query "Summarize the project requirements"
vector-bot query "What are the next steps outlined?"
vector-bot query "List all the technical specifications"
```

### Query Options

#### Controlling Context Amount

```bash
# Default: 4 chunks of context
vector-bot query "explain the architecture"

# More context for complex questions
vector-bot query "explain the architecture" --k 8

# Maximum context for comprehensive analysis
vector-bot query "explain the architecture" --k 12
```

#### Showing Source Documents

```bash
# Show which documents were used
vector-bot query "what are the requirements?" --show-sources
```

**Output includes:**
- The answer based on your documents
- List of source documents used
- Relevance scores for each source

#### Verbose Query Processing

```bash
# See detailed processing steps
vector-bot query "what is the timeline?" --verbose
```

**Shows:**
- Query processing steps
- Document retrieval details
- AI model response generation

## Daily Workflows

### Morning Startup Routine

```bash
# 1. Check system health
vector-bot doctor

# 2. Add any new documents from yesterday
cp ~/Downloads/new-report.pdf docs/

# 3. Update index
vector-bot ingest

# 4. Quick test query
vector-bot query "What's new in the latest report?"
```

### Document Review Workflow

```bash
# Add documents
cp ~/Research/*.pdf docs/

# Index them
vector-bot ingest

# Initial exploration
vector-bot query "What are the main themes across these documents?"
vector-bot query "Are there any contradictory findings?" --k 8
vector-bot query "What methodologies are used?" --show-sources
```

### Meeting Preparation Workflow

```bash
# Add meeting prep materials
cp ~/Meeting-Prep/* docs/

# Index
vector-bot ingest

# Preparation queries
vector-bot query "What are the key discussion points?"
vector-bot query "What decisions need to be made?"
vector-bot query "Who needs to be informed about what?" --k 6
```

### Research Analysis Workflow

```bash
# Comprehensive analysis
vector-bot query "What are the key findings?" --k 8
vector-bot query "What evidence supports the main conclusion?" --show-sources
vector-bot query "What are the limitations mentioned?"
vector-bot query "How do these findings compare to previous work?"
```

## Working with Different Document Types

### PDF Documents

**Best for**: Research papers, reports, manuals, presentations

```bash
# PDFs work well for structured content
vector-bot query "What does the executive summary say?"
vector-bot query "Find the methodology section"
```

**Tips for PDFs:**
- Ensure text is selectable (not scanned images)
- Break large PDFs (>20MB) into smaller sections
- Use descriptive filenames

### Markdown Documents

**Best for**: Notes, documentation, structured text

```bash
# Markdown preserves structure well
vector-bot query "What are the installation steps?"
vector-bot query "Show me the code examples"
```

**Tips for Markdown:**
- Use clear headings and structure
- Include code blocks for technical content
- Link related documents

### Text Files

**Best for**: Meeting notes, logs, unstructured content

```bash
# Plain text is processed efficiently
vector-bot query "What was discussed about the budget?"
vector-bot query "Are there any action items?"
```

**Tips for text files:**
- Use consistent formatting
- Include dates and context
- Separate different topics clearly

### JSON and CSV Files

**Best for**: Structured data, logs, API responses

```bash
# Query structured data
vector-bot query "What errors occurred most frequently?"
vector-bot query "What are the performance metrics?"
```

**Tips for structured data:**
- Include field descriptions in your queries
- Reference specific data points
- Consider converting to markdown for complex analysis

## Optimization Tips

### Query Optimization

**📝 Be specific with your questions:**
- Instead of: "Tell me about the project"
- Try: "What are the project deliverables and timeline?"

**🎯 Use domain-specific terms:**
- Use the same terminology as your documents
- Include relevant keywords from your field

**📊 Adjust context based on question complexity:**
- Simple facts: default (`--k 4`)
- Complex analysis: more context (`--k 8-12`)

### Document Organization

**📁 Organize by topic or project:**
```bash
docs/
├── project-alpha/
│   ├── requirements.pdf
│   └── design-docs.md
├── project-beta/
│   ├── research.pdf
│   └── notes.txt
└── reference/
    └── standards.pdf
```

**📝 Use descriptive filenames:**
- Good: `2024-Q1-performance-report.pdf`
- Poor: `report.pdf`

**🗂️ Keep documents current:**
- Remove outdated versions
- Update index after changes
- Archive completed projects

### Performance Optimization

**🚀 Faster queries:**
- Use fewer context chunks for simple questions
- Keep documents under 20MB
- Use SSD storage for index directory

**💾 Efficient indexing:**
- Process documents in batches
- Use markdown format when possible
- Remove unnecessary files before indexing

## Common Usage Patterns

### Academic Research

```bash
# Literature review
vector-bot query "What papers discuss neural networks in healthcare?" --k 8
vector-bot query "Compare the methodologies used" --show-sources
vector-bot query "What are the main research gaps identified?"
```

### Business Analysis

```bash
# Market research
vector-bot query "What are the key market trends mentioned?"
vector-bot query "What competitive advantages are discussed?" --k 6
vector-bot query "What risks and opportunities are identified?"
```

### Technical Documentation

```bash
# API exploration
vector-bot query "How do I authenticate API requests?"
vector-bot query "What are the available endpoints?" --show-sources
vector-bot query "Show me examples of error responses"
```

### Personal Knowledge Management

```bash
# Note exploration
vector-bot query "What did I learn about productivity this week?"
vector-bot query "Find my notes about the Johnson meeting"
vector-bot query "What ideas did I have for the new project?"
```

## Best Practices

### Document Management

1. **Regular maintenance**: Remove outdated documents monthly
2. **Consistent naming**: Use clear, descriptive filenames
3. **Logical organization**: Group related documents in folders
4. **Size management**: Keep individual files under 20MB

### Query Strategies

1. **Start broad, then narrow**: General overview, then specific details
2. **Use progressive questions**: Build on previous answers
3. **Validate with sources**: Use `--show-sources` for important information
4. **Iterate and refine**: Adjust questions based on results

### Index Management

1. **Regular updates**: Run `ingest` after adding documents
2. **Health checks**: Use `doctor` before important work
3. **Clean rebuilds**: Occasionally delete and rebuild index
4. **Backup strategy**: Keep document sources backed up

## Global Options

All commands support these global options:

```bash
# Use specific environment
vector-bot --env production query "test"

# Show configuration and exit
vector-bot --config-info

# Show version
vector-bot --version

# Show help
vector-bot --help
```

## Command Reference Quick Card

```bash
# System health
vector-bot doctor [--verbose]

# Index documents  
vector-bot ingest [--verbose]

# Ask questions
vector-bot query "your question" [--k N] [--show-sources] [--verbose]

# Configuration
vector-bot --config-info [--env ENV]
```

---

## What's Next?

Now that you understand basic usage:

- **[Advanced Features](advanced-features.md)** - Power user capabilities
- **[Basic Configuration](basic-configuration.md)** - Customize for your needs
- **[Examples](examples.md)** - Real-world usage scenarios
- **[Troubleshooting](troubleshooting.md)** - Solve common issues

**Need quick answers?** Check the [FAQ](../reference/faq.md)