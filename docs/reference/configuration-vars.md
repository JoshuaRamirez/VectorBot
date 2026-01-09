---
title: Configuration Variables Reference
description: Complete reference of all Vector Bot configuration variables with types, defaults, and examples
audience: all
level: reference
keywords: [configuration, variables, reference, settings, environment, parameters]
related_docs: [../user/basic-configuration.md, ../admin/configuration.md, faq.md]
---

# Configuration Variables Reference

Complete reference of all Vector Bot configuration variables, their types, default values, and usage examples.

## Core Configuration Variables

### Document and Index Settings

#### DOCS_DIR
- **Type**: Path (string)
- **Default**: `./docs`
- **Description**: Directory containing documents to be indexed
- **Examples**:
  ```bash
  DOCS_DIR=./documents
  DOCS_DIR=/home/user/research-papers
  DOCS_DIR="C:\Users\User\Documents\Research"
  DOCS_DIR=~/Documents/vector-bot-docs
  ```
- **Notes**: Relative paths resolved from executable directory

#### INDEX_DIR
- **Type**: Path (string)
- **Default**: `./index_storage`
- **Description**: Directory for storing the vector index
- **Examples**:
  ```bash
  INDEX_DIR=./my-index
  INDEX_DIR=/var/lib/vector-bot/index
  INDEX_DIR="C:\Data\VectorBot\Index"
  ```
- **Notes**: Must have write permissions; created automatically if doesn't exist

### Ollama Connection Settings

#### OLLAMA_BASE_URL
- **Type**: URL (string)
- **Default**: `http://localhost:11434`
- **Description**: Base URL for Ollama API server
- **Examples**:
  ```bash
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_BASE_URL=http://192.168.1.100:11434
  OLLAMA_BASE_URL=https://ollama.company.com:11434
  OLLAMA_BASE_URL=http://host.docker.internal:11434
  ```
- **Notes**: Must be accessible from where Vector Bot runs

#### OLLAMA_CHAT_MODEL
- **Type**: String
- **Default**: Auto-detection (uses first available model)
- **Description**: AI model name for generating answers
- **Examples**:
  ```bash
  OLLAMA_CHAT_MODEL=llama3.1
  OLLAMA_CHAT_MODEL=llama3.2
  OLLAMA_CHAT_MODEL=mistral
  OLLAMA_CHAT_MODEL=qwen2.5
  OLLAMA_CHAT_MODEL=codellama
  ```
- **Notes**: Model must be installed in Ollama (`ollama list` to check)

#### OLLAMA_EMBED_MODEL
- **Type**: String
- **Default**: `nomic-embed-text`
- **Description**: Model for creating document embeddings
- **Examples**:
  ```bash
  OLLAMA_EMBED_MODEL=nomic-embed-text
  OLLAMA_EMBED_MODEL=mxbai-embed-large
  OLLAMA_EMBED_MODEL=all-minilm
  ```
- **Notes**: Must be compatible embedding model; auto-installed if missing

### Query Configuration

#### SIMILARITY_TOP_K
- **Type**: Integer
- **Default**: `4`
- **Range**: `1-50` (practical range: `2-12`)
- **Description**: Number of document chunks to retrieve per query
- **Examples**:
  ```bash
  SIMILARITY_TOP_K=2    # Minimal context
  SIMILARITY_TOP_K=4    # Default
  SIMILARITY_TOP_K=8    # More context
  SIMILARITY_TOP_K=12   # Maximum recommended
  ```
- **Performance**: Higher values = slower but more comprehensive answers

## Performance Configuration

### Request and Timeout Settings

#### REQUEST_TIMEOUT
- **Type**: Float (seconds)
- **Default**: `60.0`
- **Description**: Timeout for Ollama API requests
- **Examples**:
  ```bash
  REQUEST_TIMEOUT=30.0     # Fast timeout
  REQUEST_TIMEOUT=60.0     # Default
  REQUEST_TIMEOUT=120.0    # Production/remote server
  REQUEST_TIMEOUT=300.0    # Slow systems
  ```
- **Notes**: Increase for slow systems or complex queries

#### EMBED_BATCH_SIZE
- **Type**: Integer  
- **Default**: `10`
- **Range**: `1-50`
- **Description**: Number of chunks processed per embedding batch
- **Examples**:
  ```bash
  EMBED_BATCH_SIZE=3      # Low memory systems
  EMBED_BATCH_SIZE=5      # Standard systems
  EMBED_BATCH_SIZE=10     # Default
  EMBED_BATCH_SIZE=20     # High performance systems
  ```
- **Performance**: Larger batches = faster but more memory usage

### Memory and Processing

#### MAX_DOCUMENT_SIZE
- **Type**: Integer (bytes)
- **Default**: `20971520` (20MB)
- **Description**: Maximum size for individual documents
- **Examples**:
  ```bash
  MAX_DOCUMENT_SIZE=10485760    # 10MB
  MAX_DOCUMENT_SIZE=20971520    # 20MB (default)
  MAX_DOCUMENT_SIZE=52428800    # 50MB
  MAX_DOCUMENT_SIZE=104857600   # 100MB
  ```
- **Notes**: Larger files are automatically skipped during ingestion

#### PARALLEL_WORKERS
- **Type**: Integer
- **Default**: `1`
- **Range**: `1-8`
- **Description**: Number of parallel workers for document processing
- **Examples**:
  ```bash
  PARALLEL_WORKERS=1    # Single-threaded (default)
  PARALLEL_WORKERS=2    # Dual-core systems  
  PARALLEL_WORKERS=4    # Quad-core systems
  PARALLEL_WORKERS=8    # High-end systems
  ```
- **Notes**: Limited by CPU cores and available memory

## Logging and Debug Settings

### Logging Configuration

#### LOG_LEVEL
- **Type**: String (enum)
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Description**: Minimum logging level
- **Examples**:
  ```bash
  LOG_LEVEL=DEBUG      # Development/troubleshooting
  LOG_LEVEL=INFO       # Production default
  LOG_LEVEL=WARNING    # Minimal logging
  LOG_LEVEL=ERROR      # Error-only logging
  ```

#### ENABLE_VERBOSE_OUTPUT
- **Type**: Boolean
- **Default**: `false`
- **Description**: Show detailed processing information
- **Examples**:
  ```bash
  ENABLE_VERBOSE_OUTPUT=true     # Show verbose output
  ENABLE_VERBOSE_OUTPUT=false    # Standard output
  ENABLE_VERBOSE_OUTPUT=1        # True (alternative)
  ENABLE_VERBOSE_OUTPUT=0        # False (alternative)
  ```

#### LOG_FORMAT
- **Type**: String (enum)
- **Default**: `text`
- **Options**: `text`, `json`
- **Description**: Log output format
- **Examples**:
  ```bash
  LOG_FORMAT=text    # Human-readable logs
  LOG_FORMAT=json    # Structured logs for parsing
  ```

#### LOG_FILE
- **Type**: Path (string)
- **Default**: None (stdout/stderr)
- **Description**: File path for log output
- **Examples**:
  ```bash
  LOG_FILE=/var/log/vector-bot/vector-bot.log
  LOG_FILE=./vector-bot.log
  LOG_FILE="C:\Logs\VectorBot\app.log"
  ```

## Environment and System Settings

### Environment Control

#### RAG_ENV
- **Type**: String
- **Default**: `development`
- **Options**: `development`, `production`, `docker`, or custom
- **Description**: Environment profile to load
- **Examples**:
  ```bash
  RAG_ENV=development    # Development profile
  RAG_ENV=production     # Production profile
  RAG_ENV=docker        # Docker profile
  RAG_ENV=staging       # Custom staging profile
  ```

#### RAG_VERBOSE
- **Type**: Boolean
- **Default**: `false`
- **Description**: Show configuration loading details
- **Examples**:
  ```bash
  RAG_VERBOSE=true     # Show config loading
  RAG_VERBOSE=false    # Silent loading
  ```

### System Integration

#### ENABLE_METRICS
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable Prometheus metrics endpoint
- **Examples**:
  ```bash
  ENABLE_METRICS=true     # Enable metrics
  ENABLE_METRICS=false    # Disable metrics
  ```

#### METRICS_PORT
- **Type**: Integer
- **Default**: `9090`
- **Description**: Port for metrics endpoint
- **Examples**:
  ```bash
  METRICS_PORT=9090    # Default Prometheus port
  METRICS_PORT=8080    # Alternative port
  ```

## Security Settings

### Authentication and Access

#### ENABLE_AUTHENTICATION
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable user authentication
- **Examples**:
  ```bash
  ENABLE_AUTHENTICATION=true     # Require auth
  ENABLE_AUTHENTICATION=false    # Open access
  ```

#### AUTH_METHOD
- **Type**: String (enum)
- **Default**: `none`
- **Options**: `none`, `basic`, `jwt`, `oauth`
- **Description**: Authentication method
- **Examples**:
  ```bash
  AUTH_METHOD=none     # No authentication
  AUTH_METHOD=basic    # Basic HTTP auth
  AUTH_METHOD=jwt      # JWT tokens
  ```

#### SESSION_TIMEOUT
- **Type**: Integer (seconds)
- **Default**: `3600` (1 hour)
- **Description**: User session timeout
- **Examples**:
  ```bash
  SESSION_TIMEOUT=1800    # 30 minutes
  SESSION_TIMEOUT=3600    # 1 hour (default)
  SESSION_TIMEOUT=7200    # 2 hours
  ```

### Network Security

#### ALLOWED_IP_RANGES
- **Type**: String (comma-separated CIDR ranges)
- **Default**: None (all allowed)
- **Description**: IP ranges allowed to access Vector Bot
- **Examples**:
  ```bash
  ALLOWED_IP_RANGES=192.168.1.0/24
  ALLOWED_IP_RANGES=10.0.0.0/8,172.16.0.0/12
  ALLOWED_IP_RANGES=127.0.0.1/32  # Localhost only
  ```

#### ENABLE_TLS
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable TLS/SSL encryption
- **Examples**:
  ```bash
  ENABLE_TLS=true     # Enable TLS
  ENABLE_TLS=false    # Plain HTTP
  ```

#### TLS_CERT_FILE
- **Type**: Path (string)
- **Default**: None
- **Description**: Path to TLS certificate file
- **Examples**:
  ```bash
  TLS_CERT_FILE=/etc/ssl/vector-bot/cert.pem
  TLS_CERT_FILE=./tls/certificate.pem
  ```

## Advanced Configuration

### Data Processing

#### CHUNK_SIZE
- **Type**: Integer (characters)
- **Default**: `1000`
- **Description**: Size of document chunks for processing
- **Examples**:
  ```bash
  CHUNK_SIZE=500     # Smaller chunks, more precision
  CHUNK_SIZE=1000    # Default balance
  CHUNK_SIZE=2000    # Larger chunks, more context
  ```

#### CHUNK_OVERLAP
- **Type**: Integer (characters)
- **Default**: `200`
- **Description**: Overlap between adjacent chunks
- **Examples**:
  ```bash
  CHUNK_OVERLAP=100    # Minimal overlap
  CHUNK_OVERLAP=200    # Default overlap
  CHUNK_OVERLAP=400    # High overlap
  ```

### Storage and Caching

#### ENABLE_INDEX_COMPRESSION
- **Type**: Boolean
- **Default**: `true`
- **Description**: Compress index files to save space
- **Examples**:
  ```bash
  ENABLE_INDEX_COMPRESSION=true     # Enable compression
  ENABLE_INDEX_COMPRESSION=false    # Disable compression
  ```

#### INDEX_CACHE_SIZE
- **Type**: Integer (MB)
- **Default**: `100`
- **Description**: Size of index cache in memory
- **Examples**:
  ```bash
  INDEX_CACHE_SIZE=50     # Low memory systems
  INDEX_CACHE_SIZE=100    # Default
  INDEX_CACHE_SIZE=500    # High memory systems
  ```

## Environment-Specific Variables

### Development Environment

```bash
# Development defaults
LOG_LEVEL=DEBUG
ENABLE_VERBOSE_OUTPUT=true
REQUEST_TIMEOUT=60.0
EMBED_BATCH_SIZE=10
DOCS_DIR=./docs
INDEX_DIR=./index_storage
```

### Production Environment

```bash
# Production optimized
LOG_LEVEL=INFO
ENABLE_VERBOSE_OUTPUT=false
REQUEST_TIMEOUT=120.0
EMBED_BATCH_SIZE=5
DOCS_DIR=/var/lib/vector-bot/documents
INDEX_DIR=/var/lib/vector-bot/index
ENABLE_METRICS=true
```

### Docker Environment

```bash
# Container optimized
LOG_LEVEL=INFO
ENABLE_VERBOSE_OUTPUT=false
REQUEST_TIMEOUT=90.0
EMBED_BATCH_SIZE=8
DOCS_DIR=/app/docs
INDEX_DIR=/app/index_storage
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

## Configuration File Examples

### Complete Development Configuration

```bash
# .env for development
# Core paths
DOCS_DIR=./project-docs
INDEX_DIR=./project-index

# Ollama connection
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text

# Query settings
SIMILARITY_TOP_K=4

# Performance
REQUEST_TIMEOUT=60.0
EMBED_BATCH_SIZE=10
MAX_DOCUMENT_SIZE=20971520

# Logging
LOG_LEVEL=DEBUG
ENABLE_VERBOSE_OUTPUT=true
LOG_FORMAT=text

# Environment
RAG_ENV=development
```

### Complete Production Configuration

```bash
# configs/production.env
# Core paths (absolute for reliability)
DOCS_DIR=/var/lib/vector-bot/documents
INDEX_DIR=/var/lib/vector-bot/index

# Ollama connection
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text

# Query settings
SIMILARITY_TOP_K=4

# Performance (production optimized)
REQUEST_TIMEOUT=120.0
EMBED_BATCH_SIZE=5
MAX_DOCUMENT_SIZE=52428800
PARALLEL_WORKERS=2

# Logging (structured for parsing)
LOG_LEVEL=INFO
ENABLE_VERBOSE_OUTPUT=false
LOG_FORMAT=json
LOG_FILE=/var/log/vector-bot/vector-bot.log

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Security
ENABLE_AUTHENTICATION=true
AUTH_METHOD=jwt
SESSION_TIMEOUT=3600

# Environment
RAG_ENV=production
```

## Variable Type Reference

### Boolean Values

Boolean variables accept these values:

**True values**: `true`, `True`, `1`, `yes`, `on`
**False values**: `false`, `False`, `0`, `no`, `off`

```bash
# These are all equivalent
ENABLE_VERBOSE_OUTPUT=true
ENABLE_VERBOSE_OUTPUT=True  
ENABLE_VERBOSE_OUTPUT=1
ENABLE_VERBOSE_OUTPUT=yes
```

### Path Values

Path variables support:

- **Relative paths**: Resolved from executable directory
- **Absolute paths**: Used as-is
- **Home directory**: `~` expansion (Unix/Linux/macOS)
- **Environment variables**: `$HOME`, `${USER}` expansion

```bash
# Path examples
DOCS_DIR=./docs                    # Relative
DOCS_DIR=/var/lib/vector-bot/docs  # Absolute
DOCS_DIR=~/Documents/vector-bot    # Home directory
DOCS_DIR=${HOME}/vector-bot/docs   # Environment variable
```

### URL Values

URL variables must be valid HTTP/HTTPS URLs:

```bash
# Valid URL formats
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_BASE_URL=https://ollama.company.com:11434
OLLAMA_BASE_URL=http://192.168.1.100:8080
```

## Configuration Validation

Vector Bot validates configuration on startup:

### Automatic Validations

- **Path existence**: Directories must exist or be creatable
- **URL format**: URLs must be valid HTTP/HTTPS
- **Numeric ranges**: Numbers must be within valid ranges
- **Boolean format**: Booleans must be recognizable
- **Model availability**: Required models must be accessible

### Manual Validation

```bash
# Validate current configuration
vector-bot doctor

# Validate specific environment
vector-bot --env production doctor

# Show computed configuration
vector-bot --config-info
```

## Configuration Precedence Examples

Understanding how configuration values are resolved:

### Example 1: Simple Override

```bash
# .env file
SIMILARITY_TOP_K=4

# Environment variable override
export SIMILARITY_TOP_K=8

# Command line override
SIMILARITY_TOP_K=12 vector-bot query "test"

# Result: Uses SIMILARITY_TOP_K=12 (command line wins)
```

### Example 2: Environment Profile

```bash
# configs/production.env
SIMILARITY_TOP_K=6
LOG_LEVEL=INFO

# .env file  
SIMILARITY_TOP_K=4
DOCS_DIR=./local-docs

# Running with environment
vector-bot --env production --config-info

# Result: 
# SIMILARITY_TOP_K=4 (local .env overrides profile)
# LOG_LEVEL=INFO (from profile)
# DOCS_DIR=./local-docs (from local .env)
```

---

## Quick Reference

### Most Common Variables

```bash
# Essential settings most users need
DOCS_DIR=./documents
OLLAMA_CHAT_MODEL=llama3.1  
SIMILARITY_TOP_K=4
LOG_LEVEL=INFO
```

### Performance Tuning Variables

```bash
# For performance optimization
EMBED_BATCH_SIZE=10
REQUEST_TIMEOUT=120.0
PARALLEL_WORKERS=2
INDEX_CACHE_SIZE=200
```

### Debug Variables

```bash
# For troubleshooting
LOG_LEVEL=DEBUG
ENABLE_VERBOSE_OUTPUT=true
RAG_VERBOSE=true
```

---

For usage examples and configuration scenarios, see:
- [Basic Configuration Guide](../user/basic-configuration.md)
- [Admin Configuration Guide](../admin/configuration.md)
- [FAQ](faq.md)