# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-10

### Added
- Multi-store support for managing multiple independent document indexes
- Multi-directory support: stores can index from multiple document directories
- CLI commands `vector-bot` and `rag` with subcommands: `doctor`, `ingest`, `query`, `store`, `migrate`
- Store management: `store new`, `store list`, `store info`, `store delete`, `store rename`, `store default`, `store reindex`
- Migration support from legacy `index_storage/` directory to new store-based system
- Backwards compatibility for existing store configurations
- Fully local RAG pipeline using LlamaIndex with Ollama
- Offline operation after initial setup
- Vector embeddings with configurable Ollama models
- Rich CLI output with progress indicators
- Comprehensive test suite (324 tests, 99% coverage)
- GitHub Actions CI/CD with automated PyPI publishing
