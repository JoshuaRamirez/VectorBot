# Changelog

All notable changes to the Local Ollama RAG project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive GitHub Actions CI/CD pipeline
  - Multi-platform testing (Ubuntu, Windows, macOS)
  - Python version matrix (3.10, 3.11, 3.12)
  - Automated security scanning with CodeQL, Bandit, and Safety
  - Automated PyPI publishing on release
  - Multi-platform executable builds
- Professional unit testing suite
  - 135 passing tests (115 unit + 20 integration) with 99% code coverage
  - Complete mocking of external dependencies
  - Tests run completely offline
  - Professional test structure following AAA pattern
- DevOps infrastructure
  - GitHub Actions workflows for CI/CD
  - Dependabot configuration for dependency updates
  - Pre-commit hooks support
  - Security policy (SECURITY.md)
  - Contributing guidelines (CONTRIBUTING.md)
  - MIT License
- Documentation improvements
  - Comprehensive testing documentation (TESTING.md)
  - Enhanced README with badges and test statistics
  - Improved deployment guide with CI/CD information

### Fixed
- All 21 failing unit tests now passing
- Windows/Unix path compatibility issues in tests
- Mock console output handling across all modules
- Configuration loading in test environments
- Complex Path.exists() mocking issue in CLI config test

### Changed
- Enhanced pyproject.toml with complete publishing metadata
- Improved test fixture architecture for better reusability
- Updated all documentation to reflect current project state

## [1.0.0] - 2025-01-01

### Initial Release
- Fully local RAG pipeline using LlamaIndex with Ollama
- Offline question-answering capabilities
- Document indexing support (PDF, Markdown, text, JSON, CSV)
- Multi-environment configuration (development, production, Docker)
- Executable distribution with PyInstaller
- Command-line interface with doctor, ingest, and query commands
- Persistent storage for document indices
- Comprehensive documentation suite

### Features
- 100% local operation - no external API calls
- Minimal dependencies for clean setup
- Environment-based configuration
- Automatic model detection and selection
- Rich console output with progress indicators
- Error handling and user-friendly messages

### Supported Platforms
- Windows
- macOS
- Linux

### Requirements
- Python 3.10+
- Ollama installed and running
- At least one Ollama chat model installed

---

[Unreleased]: https://github.com/yourusername/local-ollama-rag-poc/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/local-ollama-rag-poc/releases/tag/v1.0.0