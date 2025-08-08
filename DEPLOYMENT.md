# Deployment Guide

This guide covers deploying the Local Ollama RAG application in different environments.

## Multi-Environment Support

The application supports multiple deployment environments with specific configurations:

### Environment Configuration Priority

1. **Command-line specified**: `--env production`
2. **Environment variable**: `RAG_ENV=production`
3. **Local .env file**: `.env` in current directory
4. **Default**: `configs/development.env`

### Available Environments

#### Development (`--env development`)
- Local development with verbose logging
- Documents in `./docs`
- Index storage in `./index_storage`
- Auto-detection enabled

#### Production (`--env production`)
- Optimized for server deployment
- Documents in `/data/documents`
- Index storage in `/data/index_storage`
- Reduced logging, improved performance

#### Docker (`--env docker`)
- Containerized deployment
- Uses Docker-specific paths and networking
- Ollama at `host.docker.internal:11434`

## Deployment Methods

### 1. Standalone Executable

Build a single executable with all dependencies:

```bash
# Build executable
make build-exe

# Deploy executable with configs
cp dist/rag /usr/local/bin/
cp -r configs /usr/local/share/rag/
```

**Usage:**
```bash
# Use specific environment
rag --env production doctor
rag --env production ingest
rag --env production query "What are the requirements?"

# Check configuration
rag --config-info --env production
```

### 2. Python Package Installation

For environments with Python already installed:

```bash
# Install in production environment
pip install -e .

# Set environment
export RAG_ENV=production
export DOCS_DIR=/data/documents
export INDEX_DIR=/data/index_storage

# Run commands
python -m rag.cli doctor
```

### 3. Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install -e .

# Create data directories
RUN mkdir -p /app/docs /app/index_storage

# Set environment
ENV RAG_ENV=docker

ENTRYPOINT ["python", "-m", "rag.cli"]
CMD ["--help"]
```

**Build and run:**
```bash
docker build -t rag-local .

# Run with volume mounts
docker run -v /host/docs:/app/docs \
           -v /host/index:/app/index_storage \
           rag-local --env docker doctor
```

### 4. System Service (Linux)

Create a systemd service for production deployment:

```ini
# /etc/systemd/system/rag-indexer.service
[Unit]
Description=RAG Document Indexer
After=network.target

[Service]
Type=oneshot
User=rag
Group=rag
Environment=RAG_ENV=production
Environment=DOCS_DIR=/data/documents
Environment=INDEX_DIR=/data/index_storage
ExecStart=/usr/local/bin/rag ingest
WorkingDirectory=/opt/rag

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable rag-indexer.service
sudo systemctl start rag-indexer.service
```

## Configuration Management

### Environment-Specific Settings

#### Custom Environment Variables

```bash
# Override any setting via environment
export OLLAMA_BASE_URL="http://remote-ollama:11434"
export DOCS_DIR="/custom/path/docs"
export SIMILARITY_TOP_K=6
```

#### Configuration Validation

The application validates all configuration on startup:
- Checks directory permissions
- Validates URL formats  
- Confirms numeric values are valid
- Creates missing directories

### Path Resolution

The application intelligently resolves paths:

1. **Absolute paths**: Used as-is
2. **Relative paths**: Resolved relative to executable location
3. **Executable bundled**: Works with PyInstaller bundles

### Configuration Debugging

```bash
# Show current configuration
rag --config-info --env production

# Show verbose config loading
RAG_VERBOSE=true rag doctor --env production
```

## Production Deployment Checklist

### Pre-deployment

- [ ] Ollama installed and running on target system
- [ ] Required models pulled (`ollama pull llama3.1`, `ollama pull nomic-embed-text`)
- [ ] Data directories created with proper permissions
- [ ] Network connectivity to Ollama verified

### Deployment

- [ ] Copy executable to target location
- [ ] Copy configuration files
- [ ] Set appropriate environment variables
- [ ] Test with `rag --config-info --env production`
- [ ] Run health check: `rag --env production doctor`

### Post-deployment

- [ ] Initial document ingestion: `rag --env production ingest`
- [ ] Test querying: `rag --env production query "test question"`
- [ ] Set up monitoring/logging as needed
- [ ] Configure automated document updates

## Environment-Specific Considerations

### Development
- Uses local paths for easy iteration
- Verbose logging enabled
- Auto-detection of models

### Production
- Uses absolute paths for stability
- Optimized timeouts and batch sizes
- Reduced logging for performance
- Configurable resource limits

### Docker
- Special networking for Ollama connectivity
- Container-specific paths
- Volume mount support for persistence

### Windows
- Uses Windows-style paths automatically
- Service deployment via NSSM or similar
- Batch file wrappers if needed

## Security Considerations

- Run with dedicated user account (not root)
- Restrict file permissions on data directories
- Consider network security for Ollama access
- Validate input document sources
- Monitor resource usage

## Troubleshooting

### Configuration Issues
```bash
# Debug configuration loading
RAG_VERBOSE=true rag --config-info --env production
```

### Path Resolution Problems
```bash
# Check executable location detection
python -c "from rag.config import get_executable_dir; print(get_executable_dir())"
```

### Environment Loading
```bash
# Test specific environment
rag --env production --config-info
```

### Ollama Connectivity
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags
rag --env production doctor
```