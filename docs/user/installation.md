---
title: Installation Guide
description: Complete installation guide for Vector Bot including all methods and troubleshooting
audience: user
level: beginner
keywords: [installation, install, setup, npm, pip, executable, ollama, requirements]
related_docs: [getting-started.md, basic-configuration.md, troubleshooting.md, ../reference/faq.md]
---

# Installation Guide

This guide covers all methods to install Vector Bot and its prerequisites. Choose the method that works best for your setup.

## Prerequisites

Before installing Vector Bot, you need:

### 1. Operating System Support

Vector Bot runs on:
- **Windows** 10/11 (x64)
- **macOS** 10.14+ (Intel and Apple Silicon)
- **Linux** (x64) - Ubuntu 18.04+, CentOS 7+, or equivalent

### 2. Ollama Installation

Vector Bot requires Ollama for AI models. Install it first:

#### Install Ollama

**Option A: Download from Website (Recommended)**
1. Visit [ollama.ai](https://ollama.ai)
2. Download the installer for your operating system
3. Run the installer and follow instructions

**Option B: Command Line Installation**

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows (PowerShell):**
```powershell
iwr -useb https://ollama.ai/install.ps1 | iex
```

#### Verify Ollama Installation

```bash
# Check Ollama version
ollama --version

# Start Ollama server (if not already running)
ollama serve
```

**Expected output:**
```
ollama version is 0.1.32
```

#### Install Required AI Models

```bash
# Install a chat model (choose one)
ollama pull llama3.1        # Recommended: Good balance of speed and quality
ollama pull llama3.2        # Alternative: Latest model
ollama pull mistral         # Alternative: Fast model

# Install embedding model (required)
ollama pull nomic-embed-text
```

**Verify models are installed:**
```bash
ollama list
```

**Expected output:**
```
NAME                    ID              SIZE    MODIFIED
llama3.1:latest         42182f0b3b60    4.7GB   2 weeks ago
nomic-embed-text:latest 0a109f422b47    274MB   2 weeks ago
```

## Vector Bot Installation Methods

Choose one of these installation methods:

## Method 1: npm Package (Recommended)

Best for most users. Works on all platforms and includes automatic updates.

### Install Node.js (if needed)

If you don't have Node.js:
1. Visit [nodejs.org](https://nodejs.org)
2. Download and install the LTS version
3. Verify installation:

```bash
node --version
npm --version
```

### Install Vector Bot

```bash
# Install globally (recommended)
npm install -g @joshuaramirez/vector-bot

# Verify installation
vector-bot --version
```

### Alternative: Run without installing

```bash
# Run directly without installation
npx @joshuaramirez/vector-bot --help
npx @joshuaramirez/vector-bot doctor
```

### Updating

```bash
# Update to latest version
npm update -g @joshuaramirez/vector-bot
```

## Method 2: Python Package (pip)

Best for Python developers or when npm is not available.

### Install Python (if needed)

Vector Bot requires Python 3.10 or later:

**Check current version:**
```bash
python --version
# or
python3 --version
```

**If you need to install Python:**
- **Windows**: Download from [python.org](https://python.org)
- **macOS**: `brew install python` (with Homebrew) or download from python.org
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian) or equivalent

### Install Vector Bot

```bash
# Install from PyPI
pip install vector-bot

# Verify installation
vector-bot --version
```

### Updating

```bash
# Update to latest version
pip install --upgrade vector-bot
```

## Method 3: Standalone Executable

Best for users who want a single file with no dependencies.

### Download Executable

1. Go to [GitHub Releases](https://github.com/joshuaramirez/vector-bot/releases/latest)
2. Download the appropriate file for your system:
   - **Windows**: `vector-bot.exe`
   - **macOS**: `vector-bot-macos`
   - **Linux**: `vector-bot-linux`

### Setup Executable

**Windows:**
```powershell
# Place in a permanent location
mkdir C:\Tools
move vector-bot.exe C:\Tools\

# Add to PATH (optional - makes it easier to use)
$env:PATH += ";C:\Tools"

# Test
C:\Tools\vector-bot.exe --version
```

**macOS/Linux:**
```bash
# Make executable
chmod +x vector-bot-macos  # or vector-bot-linux

# Place in a standard location (optional)
sudo mv vector-bot-macos /usr/local/bin/vector-bot

# Test
vector-bot --version
```

### Updating Executables

Download the new version from GitHub releases and replace the old file.

## Method 4: From Source Code

Best for developers who want to contribute or modify the code.

### Prerequisites for Source Installation

- **Python 3.10+**
- **Git**
- **Make** (optional, for convenience)

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/joshuaramirez/vector-bot.git
cd vector-bot

# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"

# Verify installation
vector-bot --version
```

### Development Commands

```bash
# Run tests
pytest tests/ -v

# Code quality checks
ruff check src/
mypy src/

# Build executable
python build_executable.py
```

## Installation Verification

After installing Vector Bot with any method, verify everything works:

### 1. Check Installation

```bash
# Check Vector Bot version
vector-bot --version

# Should output something like:
# Vector Bot v1.0.0
```

### 2. Run System Check

```bash
# Check all components
vector-bot doctor
```

**Expected output:**
```
✓ Ollama server is running at http://localhost:11434
✓ Chat model available: llama3.1
✓ Embedding model available: nomic-embed-text
✓ Configuration is valid
```

### 3. Test Basic Functionality

```bash
# Create test setup
mkdir test-docs
echo "This is a test document about Vector Bot installation." > test-docs/test.txt

# Index the test document
vector-bot ingest

# Ask a test question
vector-bot query "What is this document about?"
```

**Expected response:**
The AI should provide an answer about Vector Bot installation based on your test document.

## Platform-Specific Notes

### Windows

**PowerShell Execution Policy:**
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Path Issues:**
If `vector-bot` command isn't found:
- For npm install: Restart terminal after installation
- For executable: Add installation directory to PATH
- For pip: Ensure Python Scripts directory is in PATH

**Windows Defender:**
If Windows Defender blocks the executable:
1. Add an exclusion for the vector-bot.exe file
2. Or right-click → Properties → Unblock

### macOS

**Permission Issues:**
If you get "developer cannot be verified" error:
1. System Preferences → Security & Privacy → General
2. Click "Allow Anyway" next to the blocked app message

**Homebrew Users:**
```bash
# Alternative Ollama installation
brew install ollama

# Start Ollama service
brew services start ollama
```

**Apple Silicon (M1/M2):**
- All installation methods work on Apple Silicon
- Ollama includes optimized models for Apple Silicon
- Performance may be better than Intel Macs

### Linux

**Package Manager Dependencies:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install curl python3 python3-pip nodejs npm

# CentOS/RHEL/Fedora
sudo yum install curl python3 python3-pip nodejs npm

# Or with dnf
sudo dnf install curl python3 python3-pip nodejs npm
```

**Permissions:**
If you get permission errors:
```bash
# For executable installation
sudo chmod +x vector-bot-linux
sudo mv vector-bot-linux /usr/local/bin/vector-bot

# For pip installation
pip install --user vector-bot
```

## Environment Setup

### Creating Working Directory

```bash
# Create a dedicated directory for Vector Bot work
mkdir ~/vector-bot-workspace
cd ~/vector-bot-workspace

# Create documents directory
mkdir docs

# Optional: Create environment file
cp .env.example .env  # if installing from source
```

### Basic Configuration

Create a `.env` file for custom settings:

```bash
# Create basic configuration file
cat > .env << EOF
# Documents directory
DOCS_DIR=./docs

# Index storage location
INDEX_DIR=./index_storage

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_CHAT_MODEL=llama3.1
OLLAMA_EMBED_MODEL=nomic-embed-text

# Query settings
SIMILARITY_TOP_K=4
EOF
```

## Troubleshooting Installation

### Common Issues

#### Issue: "Command not found: vector-bot"

**For npm installation:**
```bash
# Check if installed globally
npm list -g @joshuaramirez/vector-bot

# Reinstall if needed
npm install -g @joshuaramirez/vector-bot

# Check npm global bin directory
npm config get prefix
```

**For pip installation:**
```bash
# Check if installed
pip show vector-bot

# Check if Python scripts directory is in PATH
python -m site --user-base
```

**For executable:**
- Ensure file is executable (`chmod +x` on Unix)
- Use full path to executable if PATH isn't set

#### Issue: "Ollama connection failed"

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start Ollama
ollama serve

# Check if on different port
ps aux | grep ollama  # Unix
tasklist | findstr ollama  # Windows
```

#### Issue: "No models found"

```bash
# List installed models
ollama list

# Install required models
ollama pull llama3.1
ollama pull nomic-embed-text

# Verify models are available
ollama list
```

#### Issue: Python version conflicts

```bash
# Check Python version
python --version

# Use specific Python version if needed
python3.10 -m pip install vector-bot

# Or use virtual environment
python -m venv vector-bot-env
source vector-bot-env/bin/activate  # Unix
vector-bot-env\Scripts\activate     # Windows
pip install vector-bot
```

### Getting Help

If you're still having issues:

1. **Run diagnosis:** `vector-bot doctor --verbose`
2. **Check logs:** Look for error messages in terminal output
3. **Verify requirements:** Ensure all prerequisites are met
4. **Check documentation:**
   - [Troubleshooting Guide](troubleshooting.md)
   - [FAQ](../reference/faq.md)
   - [Configuration Guide](basic-configuration.md)

## Multiple Installation Methods

You can have multiple installation methods on the same system:

```bash
# Example: npm and pip installations
vector-bot --version          # npm version
python -m rag.cli --version   # pip version (if installed in development mode)
```

To avoid conflicts, use only one method for regular use.

## Uninstalling

### npm Installation
```bash
npm uninstall -g @joshuaramirez/vector-bot
```

### pip Installation
```bash
pip uninstall vector-bot
```

### Executable Installation
```bash
# Simply delete the executable file
rm /usr/local/bin/vector-bot  # Unix
del C:\Tools\vector-bot.exe   # Windows
```

### Source Installation
```bash
cd vector-bot-source-directory
pip uninstall vector-bot
```

## Next Steps

After successful installation:

1. **[Getting Started](getting-started.md)** - Quick start guide
2. **[Basic Configuration](basic-configuration.md)** - Customize your setup
3. **[Basic Usage](basic-usage.md)** - Learn the essential commands

---

**Installation complete!** You're now ready to start using Vector Bot for document querying and analysis.