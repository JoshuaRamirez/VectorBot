# Makefile for Local Ollama RAG

.PHONY: help doctor ingest query smoke test install dev-install clean

help:
	@echo "Available commands:"
	@echo "  make install      - Install the package"
	@echo "  make dev-install  - Install with dev dependencies"
	@echo "  make doctor       - Check Ollama health and models"
	@echo "  make ingest       - Ingest documents and build index"
	@echo "  make query Q='...' - Query the index"
	@echo "  make smoke        - Run smoke test"
	@echo "  make test         - Run unit tests"
	@echo "  make clean        - Clean generated files"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

doctor:
	python -m rag.cli doctor

ingest:
	python -m rag.cli ingest

query:
	@if [ -z "$(Q)" ]; then \
		echo "Usage: make query Q='your question here'"; \
		exit 1; \
	fi
	python -m rag.cli query "$(Q)"

smoke:
	python scripts/rag_smoke.py

test:
	pytest tests/ -v

clean:
	rm -rf index_storage/
	rm -rf __pycache__/
	rm -rf src/rag/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete