---
title: Advanced Features Guide
description: Power user features including batch processing, custom environments, and integration patterns
audience: user
level: advanced
keywords: [advanced-features, batch-processing, environments, integration, automation, scripting]
related_docs: [basic-usage.md, basic-configuration.md, ../admin/configuration.md, troubleshooting.md]
---

# Advanced Features Guide

This guide covers advanced Vector Bot features for power users, including multi-environment configurations, batch processing, automation, and integration patterns.

## Environment-Specific Configurations

Vector Bot supports different configuration profiles for various deployment scenarios.

### Available Environments

| Environment | Use Case | Key Features |
|-------------|----------|--------------|
| `development` | Local development, testing | Verbose output, relative paths |
| `production` | Production deployment | Optimized settings, absolute paths |
| `docker` | Container deployment | Container networking, volume paths |

### Using Environment Profiles

#### Via Command Line Flag

```bash
# Use specific environment for one command
vector-bot --env development doctor
vector-bot --env production ingest
vector-bot --env docker query "test question"
```

#### Via Environment Variable

```bash
# Set environment for entire session
export RAG_ENV=production
vector-bot doctor
vector-bot ingest
vector-bot query "questions"

# Override for single command
RAG_ENV=development vector-bot doctor
```

### Environment Configuration Details

#### Development Environment
```bash
# Optimized for local development
vector-bot --env development --config-info

# Shows:
# - Relative paths (./docs, ./index_storage)
# - Verbose logging enabled
# - Debug output enabled
# - Localhost Ollama connection
```

#### Production Environment
```bash
# Optimized for server deployment
vector-bot --env production --config-info

# Shows:
# - Absolute paths (/data/documents, /data/index)
# - Minimal logging
# - Performance optimizations
# - Longer timeouts
```

#### Docker Environment
```bash
# Optimized for container deployment
vector-bot --env docker --config-info

# Shows:
# - Container paths (/app/docs, /app/index)
# - Host networking configuration
# - Container-optimized settings
```

### Creating Custom Environments

Create custom environment configurations:

```bash
# Create custom environment file
cat > configs/staging.env << EOF
# Staging environment settings
DOCS_DIR=/staging/documents
INDEX_DIR=/staging/index
OLLAMA_BASE_URL=http://staging-ollama:11434
OLLAMA_CHAT_MODEL=llama3.1
LOG_LEVEL=INFO
SIMILARITY_TOP_K=6
REQUEST_TIMEOUT=90.0
EOF

# Use custom environment
vector-bot --env staging doctor
```

## Batch Processing

Automate Vector Bot operations for large-scale document processing and querying.

### Batch Document Processing

#### Processing Multiple Document Sets

```bash
#!/bin/bash
# batch-process.sh

# Define document sets
declare -a PROJECTS=("project-alpha" "project-beta" "project-gamma")

for project in "${PROJECTS[@]}"; do
    echo "Processing $project..."
    
    # Set project-specific configuration
    export DOCS_DIR="./projects/$project/docs"
    export INDEX_DIR="./projects/$project/index"
    
    # Process documents
    vector-bot ingest
    
    echo "✓ $project processing complete"
done
```

#### Automated Document Updates

```bash
#!/bin/bash
# auto-update.sh

# Watch for new documents and auto-ingest
WATCH_DIR="./incoming-docs"
DOCS_DIR="./docs"

# Move new documents and ingest
if [ "$(ls -A $WATCH_DIR)" ]; then
    echo "New documents found, processing..."
    mv $WATCH_DIR/* $DOCS_DIR/
    vector-bot ingest
    echo "✓ Documents processed"
fi
```

### Batch Querying

#### Processing Question Lists

```bash
#!/bin/bash
# batch-query.sh

# Read questions from file
QUESTIONS_FILE="questions.txt"
OUTPUT_DIR="./query-results"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r question; do
    echo "Processing: $question"
    
    # Generate safe filename
    filename=$(echo "$question" | sed 's/[^a-zA-Z0-9]/_/g' | cut -c1-50)
    
    # Query and save result
    vector-bot query "$question" --show-sources > "$OUTPUT_DIR/${filename}.txt"
    
    echo "✓ Saved to ${filename}.txt"
done < "$QUESTIONS_FILE"
```

#### Automated Report Generation

```bash
#!/bin/bash
# generate-reports.sh

# Configuration
REPORT_DATE=$(date +%Y-%m-%d)
REPORT_DIR="./reports/$REPORT_DATE"

mkdir -p "$REPORT_DIR"

# Generate various reports
declare -a QUERIES=(
    "What are the key findings from this week?"
    "What action items need attention?"
    "What risks were identified?"
    "What are the next steps?"
)

for query in "${QUERIES[@]}"; do
    echo "Generating report: $query"
    
    filename=$(echo "$query" | sed 's/[^a-zA-Z0-9]/_/g' | cut -c1-30)
    
    vector-bot query "$query" --k 8 --show-sources > "$REPORT_DIR/${filename}.txt"
done

echo "✓ Reports generated in $REPORT_DIR"
```

### Windows Batch Scripts

#### PowerShell Batch Processing

```powershell
# batch-process.ps1

$projects = @("project-alpha", "project-beta", "project-gamma")

foreach ($project in $projects) {
    Write-Host "Processing $project..."
    
    $env:DOCS_DIR = ".\projects\$project\docs"
    $env:INDEX_DIR = ".\projects\$project\index"
    
    vector-bot.exe ingest
    
    Write-Host "✓ $project processing complete"
}
```

#### Windows Batch File

```batch
@echo off
rem batch-query.bat

set QUESTIONS_FILE=questions.txt
set OUTPUT_DIR=query-results

mkdir %OUTPUT_DIR% 2>nul

for /f "delims=" %%i in (%QUESTIONS_FILE%) do (
    echo Processing: %%i
    vector-bot.exe query "%%i" --show-sources > "%OUTPUT_DIR%\result_%%~nI.txt"
    echo ✓ Saved result
)
```

## Custom Model Selection

Configure different AI models for different use cases.

### Model Selection Strategies

#### Performance-Optimized Setup
```bash
# Fast models for quick queries
export OLLAMA_CHAT_MODEL=llama3.1        # 7B parameters - fastest
export OLLAMA_EMBED_MODEL=nomic-embed-text # Efficient embedding model

vector-bot query "quick question"
```

#### Quality-Optimized Setup
```bash
# Larger models for complex analysis
export OLLAMA_CHAT_MODEL=llama3.3        # 70B parameters - better quality
export OLLAMA_EMBED_MODEL=mxbai-embed-large # Higher quality embeddings

vector-bot query "complex analytical question" --k 8
```

#### Task-Specific Models
```bash
# Different models for different tasks
case "$TASK_TYPE" in
    "code")
        export OLLAMA_CHAT_MODEL=codellama
        ;;
    "analysis") 
        export OLLAMA_CHAT_MODEL=mixtral
        ;;
    "general")
        export OLLAMA_CHAT_MODEL=llama3.1
        ;;
esac

vector-bot query "$QUESTION"
```

### Model Testing and Comparison

```bash
#!/bin/bash
# model-comparison.sh

QUESTION="What are the main themes in these documents?"
MODELS=("llama3.1" "llama3.2" "mistral")

for model in "${MODELS[@]}"; do
    echo "Testing model: $model"
    echo "Question: $QUESTION"
    echo "---"
    
    OLLAMA_CHAT_MODEL=$model vector-bot query "$QUESTION"
    
    echo ""
    echo "========================="
    echo ""
done
```

## Integration with External Systems

### Python Integration

```python
# python-integration.py
import subprocess
import json
import os

class VectorBotClient:
    def __init__(self, docs_dir=None, model=None):
        if docs_dir:
            os.environ['DOCS_DIR'] = docs_dir
        if model:
            os.environ['OLLAMA_CHAT_MODEL'] = model
    
    def query(self, question, k=4, show_sources=False):
        cmd = ['vector-bot', 'query', question, '--k', str(k)]
        if show_sources:
            cmd.append('--show-sources')
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    
    def ingest(self):
        result = subprocess.run(['vector-bot', 'ingest'], capture_output=True, text=True)
        return result.returncode == 0
    
    def health_check(self):
        result = subprocess.run(['vector-bot', 'doctor'], capture_output=True, text=True)
        return result.returncode == 0

# Usage example
client = VectorBotClient(docs_dir='/path/to/docs', model='llama3.1')

if client.health_check():
    client.ingest()
    answer = client.query("What are the key points?", k=6, show_sources=True)
    print(answer)
```

### REST API Wrapper

```python
# api-wrapper.py
from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_documents():
    data = request.get_json()
    question = data.get('question')
    k = data.get('k', 4)
    show_sources = data.get('show_sources', False)
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    
    cmd = ['vector-bot', 'query', question, '--k', str(k)]
    if show_sources:
        cmd.append('--show-sources')
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'answer': result.stdout})
        else:
            return jsonify({'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ingest', methods=['POST'])
def ingest_documents():
    try:
        result = subprocess.run(['vector-bot', 'ingest'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'status': 'success', 'output': result.stdout})
        else:
            return jsonify({'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        result = subprocess.run(['vector-bot', 'doctor'], capture_output=True, text=True)
        return jsonify({
            'healthy': result.returncode == 0,
            'output': result.stdout
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Docker Integration

#### Dockerfile for Custom Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Install Vector Bot
RUN pip install vector-bot

# Set up directories
WORKDIR /app
RUN mkdir -p /app/docs /app/index_storage

# Copy configuration
COPY configs/docker.env /app/.env

# Environment variables
ENV RAG_ENV=docker
ENV DOCS_DIR=/app/docs
ENV INDEX_DIR=/app/index_storage

# Expose ports (if needed for API wrapper)
EXPOSE 5000

# Default command
ENTRYPOINT ["vector-bot"]
CMD ["--help"]
```

#### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_ORIGINS=*

  vector-bot:
    build: .
    depends_on:
      - ollama
    volumes:
      - ./docs:/app/docs:ro
      - vector_index:/app/index_storage
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - RAG_ENV=docker

volumes:
  ollama_data:
  vector_index:
```

### Automation with Cron/Task Scheduler

#### Unix Cron Job

```bash
# Add to crontab (crontab -e)

# Daily document ingestion at 6 AM
0 6 * * * cd /path/to/vector-bot && /usr/local/bin/vector-bot ingest

# Weekly report generation on Sundays at 9 AM
0 9 * * 0 cd /path/to/vector-bot && /usr/local/bin/vector-bot query "Generate weekly summary" --k 10 > weekly-report-$(date +\%Y-\%m-\%d).txt

# Health check every 4 hours
0 */4 * * * /usr/local/bin/vector-bot doctor || echo "Vector Bot health check failed" | mail admin@company.com
```

#### Windows Task Scheduler

```powershell
# create-scheduled-task.ps1

# Daily ingestion task
$action = New-ScheduledTaskAction -Execute "vector-bot.exe" -Argument "ingest" -WorkingDirectory "C:\VectorBot"
$trigger = New-ScheduledTaskTrigger -Daily -At "06:00"
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable

Register-ScheduledTask -TaskName "VectorBot-DailyIngest" -Action $action -Trigger $trigger -Settings $settings
```

## Advanced Configuration Patterns

### Multi-Project Configuration

```bash
#!/bin/bash
# multi-project-setup.sh

# Create project structure
mkdir -p projects/{alpha,beta,gamma}/{docs,index}

# Create project-specific configs
cat > projects/alpha/.env << EOF
DOCS_DIR=./docs
INDEX_DIR=./index
OLLAMA_CHAT_MODEL=llama3.1
SIMILARITY_TOP_K=4
EOF

cat > projects/beta/.env << EOF
DOCS_DIR=./docs
INDEX_DIR=./index
OLLAMA_CHAT_MODEL=mixtral
SIMILARITY_TOP_K=6
EOF

cat > projects/gamma/.env << EOF
DOCS_DIR=./docs
INDEX_DIR=./index
OLLAMA_CHAT_MODEL=llama3.2
SIMILARITY_TOP_K=8
EOF

# Project switching function
switch_project() {
    cd "projects/$1"
    echo "Switched to project: $1"
    vector-bot --config-info
}
```

### Dynamic Configuration

```python
# dynamic-config.py
import os
import subprocess
from datetime import datetime, time

def get_optimal_config():
    """Adjust configuration based on time of day and system load"""
    current_time = datetime.now().time()
    
    # Business hours: use faster model for quick responses
    if time(9, 0) <= current_time <= time(17, 0):
        return {
            'OLLAMA_CHAT_MODEL': 'llama3.1',
            'SIMILARITY_TOP_K': '4',
            'REQUEST_TIMEOUT': '30'
        }
    # After hours: use better model for detailed analysis
    else:
        return {
            'OLLAMA_CHAT_MODEL': 'llama3.3',
            'SIMILARITY_TOP_K': '8',
            'REQUEST_TIMEOUT': '120'
        }

def query_with_dynamic_config(question):
    config = get_optimal_config()
    
    # Set environment variables
    for key, value in config.items():
        os.environ[key] = value
    
    # Execute query
    result = subprocess.run(['vector-bot', 'query', question], 
                          capture_output=True, text=True)
    return result.stdout
```

## Performance Optimization

### Parallel Processing

```bash
#!/bin/bash
# parallel-processing.sh

# Process multiple document sets in parallel
process_project() {
    local project=$1
    echo "Processing $project..."
    
    export DOCS_DIR="./projects/$project/docs"
    export INDEX_DIR="./projects/$project/index"
    
    vector-bot ingest > "logs/$project.log" 2>&1
    echo "✓ $project complete"
}

# Create log directory
mkdir -p logs

# Process projects in parallel
for project in alpha beta gamma delta; do
    process_project "$project" &
done

# Wait for all background processes
wait
echo "All projects processed"
```

### Memory-Optimized Processing

```bash
#!/bin/bash
# memory-optimized.sh

# For systems with limited RAM
export EMBED_BATCH_SIZE=3          # Smaller batches
export SIMILARITY_TOP_K=3          # Fewer context chunks
export REQUEST_TIMEOUT=300         # Longer timeout for slower processing

# Process in smaller chunks
for chunk_dir in docs/chunk_*; do
    export DOCS_DIR="$chunk_dir"
    vector-bot ingest
done
```

### High-Performance Configuration

```bash
#!/bin/bash
# high-performance.sh

# For systems with abundant resources
export EMBED_BATCH_SIZE=20         # Larger batches
export SIMILARITY_TOP_K=12         # More context for better answers
export REQUEST_TIMEOUT=60          # Standard timeout
export OLLAMA_CHAT_MODEL=llama3.3  # Higher quality model

vector-bot ingest
```

## Monitoring and Logging

### Health Monitoring Script

```bash
#!/bin/bash
# monitor-health.sh

LOG_FILE="vector-bot-health.log"

check_health() {
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    if vector-bot doctor > /dev/null 2>&1; then
        echo "[$timestamp] HEALTHY: Vector Bot system check passed" >> "$LOG_FILE"
        return 0
    else
        echo "[$timestamp] UNHEALTHY: Vector Bot system check failed" >> "$LOG_FILE"
        
        # Try to restart Ollama
        ollama serve &
        sleep 5
        
        if vector-bot doctor > /dev/null 2>&1; then
            echo "[$timestamp] RECOVERED: System recovered after Ollama restart" >> "$LOG_FILE"
            return 0
        else
            echo "[$timestamp] CRITICAL: System still unhealthy after restart" >> "$LOG_FILE"
            return 1
        fi
    fi
}

# Run health check
check_health
```

### Usage Analytics

```bash
#!/bin/bash
# usage-analytics.sh

ANALYTICS_FILE="vector-bot-usage.log"

log_query() {
    local question="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local question_hash=$(echo "$question" | sha256sum | cut -d' ' -f1 | head -c 10)
    
    echo "[$timestamp] QUERY: $question_hash" >> "$ANALYTICS_FILE"
}

# Wrapper function for queries with logging
query_with_logging() {
    log_query "$1"
    vector-bot query "$1" "${@:2}"
}

# Usage: query_with_logging "What are the requirements?" --k 6
```

## Troubleshooting Advanced Setups

### Configuration Debugging

```bash
#!/bin/bash
# debug-config.sh

echo "=== Vector Bot Configuration Debug ==="
echo ""

echo "Environment Variables:"
env | grep -E "(RAG_|DOCS_|INDEX_|OLLAMA_|SIMILARITY_)" | sort
echo ""

echo "Configuration Info:"
vector-bot --config-info
echo ""

echo "Available Models:"
ollama list
echo ""

echo "System Health:"
vector-bot doctor --verbose
```

### Performance Profiling

```bash
#!/bin/bash
# profile-performance.sh

echo "=== Performance Profile ==="

# Time ingestion
echo "Timing ingestion..."
time vector-bot ingest

echo ""

# Time various query complexities
for k in 2 4 8 12; do
    echo "Timing query with k=$k..."
    time vector-bot query "What are the main topics?" --k $k
    echo ""
done
```

---

## Next Steps

For advanced users, consider:

- **[Configuration Guide](../admin/configuration.md)** - Deep configuration management
- **[Contributing](../../CONTRIBUTING.md)** - Development and contribution
- **[Architecture](../../ARCHITECTURE.md)** - System architecture details

**Need help with advanced features?** Check the [Troubleshooting Guide](troubleshooting.md)