# Deployment Guide

This guide covers deploying the Vector Bot application in different environments.

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

## CI/CD Pipeline

This project includes comprehensive GitHub Actions workflows for automated testing, building, and deployment:

### Continuous Integration
- **Multi-platform testing**: Ubuntu, Windows, macOS
- **Python version matrix**: 3.10, 3.11, 3.12
- **Automated security scanning**: CodeQL, Bandit, Safety
- **Code quality checks**: ruff, mypy, pytest
- **Test coverage**: 99% code coverage requirement

### Continuous Deployment
- **Automated releases**: Tag-triggered PyPI publishing
- **Multi-platform executables**: Built for all major platforms
- **GitHub Releases**: Automatic asset attachment

### GitHub Repository Setup

To enable the CI/CD pipeline in your GitHub repository:

1. **Push the code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with CI/CD setup"
   git remote add origin https://github.com/joshuaramirez/vector-bot.git
   git push -u origin main
   ```

2. **Configure Repository Secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Add `PYPI_API_TOKEN` for PyPI publishing
   - This token is required for the release workflow

3. **Enable GitHub Actions:**
   - Actions should be enabled by default
   - First push will trigger the CI workflow
   - Check Actions tab to see workflow runs

4. **Configure Branch Protection (Optional):**
   - Go to Settings → Branches
   - Add rule for `main` branch
   - Enable "Require status checks to pass"
   - Select CI workflow checks

5. **Create a Release:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```
   This triggers the release workflow which:
   - Publishes to PyPI
   - Builds executables for all platforms
   - Creates GitHub release with assets

See `.github/workflows/` for workflow configurations.

## Deployment Methods

### 1. Standalone Executable

Build a single executable with all dependencies:

```bash
# Build executable
make build-exe

# Deploy executable with configs
cp dist/vector-bot /usr/local/bin/
cp -r configs /usr/local/share/vector-bot/
```

**Usage:**
```bash
# Use specific environment
vector-bot --env production doctor
vector-bot --env production ingest
vector-bot --env production query "What are the requirements?"

# Check configuration
vector-bot --config-info --env production
```

### 2. Python Package Installation

#### From PyPI (Recommended)
```bash
# Install from PyPI
pip install local-ollama-vector-bot

# Set environment
export RAG_ENV=production
export DOCS_DIR=/data/documents
export INDEX_DIR=/data/index_storage

# Run commands
vector-bot doctor
vector-bot ingest
vector-bot query "your question"
```

#### From Source
```bash
# Install in production environment
pip install -e .

# Set environment
export RAG_ENV=production
export DOCS_DIR=/data/documents
export INDEX_DIR=/data/index_storage

# Run commands
python -m vector-bot.cli doctor
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

ENTRYPOINT ["python", "-m", "vector-bot.cli"]
CMD ["--help"]
```

**Build and run:**
```bash
docker build -t vector-bot-local .

# Run with volume mounts
docker run -v /host/docs:/app/docs \
           -v /host/index:/app/index_storage \
           vector-bot-local --env docker doctor
```

### 4. System Service (Linux)

Create a systemd service for production deployment:

```ini
# /etc/systemd/system/vector-bot-indexer.service
[Unit]
Description=RAG Document Indexer
After=network.target

[Service]
Type=oneshot
User=vector-bot
Group=vector-bot
Environment=RAG_ENV=production
Environment=DOCS_DIR=/data/documents
Environment=INDEX_DIR=/data/index_storage
ExecStart=/usr/local/bin/vector-bot ingest
WorkingDirectory=/opt/vector-bot

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vector-bot-indexer.service
sudo systemctl start vector-bot-indexer.service
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
vector-bot --config-info --env production

# Show verbose config loading
RAG_VERBOSE=true vector-bot doctor --env production
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
- [ ] Test with `vector-bot --config-info --env production`
- [ ] Run health check: `vector-bot --env production doctor`

### Post-deployment

- [ ] Initial document ingestion: `vector-bot --env production ingest`
- [ ] Test querying: `vector-bot --env production query "test question"`
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
RAG_VERBOSE=true vector-bot --config-info --env production
```

### Path Resolution Problems
```bash
# Check executable location detection
python -c "from vector-bot.config import get_executable_dir; print(get_executable_dir())"
```

### Environment Loading
```bash
# Test specific environment
vector-bot --env production --config-info
```

### Ollama Connectivity
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags
vector-bot --env production doctor
```