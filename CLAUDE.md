# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This project implements a fully local Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex with Ollama. It provides offline question-answering capabilities by indexing local documents without any external network calls.

## Architecture

- **LLM Backend**: Ollama (reuses already-installed local chat models)
- **Embedding**: Local embedding model via Ollama (installed if needed)
- **Indexing**: LlamaIndex for document indexing and retrieval
- **Storage**: Optional persistent storage for the document index
- **Configuration**: Environment-based model selection

## Key Features

- Fully offline operation - no external API calls
- Minimal dependencies for clean, reproducible setup
- Reuses existing Ollama models when available
- Environment variable configuration for model selection
- Optional persistent storage for document indices
- Smoke-test script for validation

## Development Guidelines

When implementing features:
- Ensure all operations remain local (no external network dependencies)
- Use environment variables for model configuration
- Keep dependencies minimal
- Include proper error handling for missing Ollama models
- Test with the smoke-test script to verify grounded question-answering from local files