# Contributing to Local Ollama RAG

Thank you for your interest in contributing to Local Ollama RAG! This document provides guidelines and information for contributors.

## Code of Conduct

This project adheres to a code of conduct that promotes respectful, inclusive collaboration. By participating, you agree to uphold these standards.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Ollama installed and running locally
- Git for version control

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/local-ollama-rag-poc.git
   cd local-ollama-rag-poc
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run the smoke test to verify setup:**
   ```bash
   python scripts/rag_smoke.py
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes following our coding standards:**
   - Keep the local-first architecture intact
   - Ensure no external network dependencies are introduced
   - Follow existing code style and patterns
   - Add appropriate tests for new functionality

3. **Test your changes:**
   ```bash
   # Run all tests
   pytest tests/ -v
   
   # Run linting
   ruff check src/ tests/
   
   # Run type checking
   mypy src/
   
   # Run smoke test
   python scripts/rag_smoke.py
   ```

4. **Build and test the package:**
   ```bash
   python -m build
   pip install dist/*.whl
   rag --help
   ```

### Code Standards

- **Python Style:** Follow PEP 8, enforced by ruff
- **Type Hints:** Use type hints for all functions and methods
- **Docstrings:** Document public functions with clear docstrings
- **Error Handling:** Include appropriate error handling and user-friendly messages
- **Local-First:** Maintain offline operation - no external API calls

### Testing Requirements

All contributions must maintain or improve our testing standards:

- **Code Coverage**: Maintain minimum 95% coverage (currently at 99%)
- **Unit Tests Required**: All new functionality must have unit tests
- **Test Naming**: Follow pattern `test_ClassName_MethodName_ExpectedOutcome`
- **AAA Pattern**: All tests must follow Arrange-Act-Assert pattern
- **Single Assertion**: Each test should verify exactly one behavior
- **Full Mocking**: Tests must run completely offline with no external dependencies
- **Fast Execution**: Unit tests should complete in < 1 second each

Before submitting:
```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=rag --cov-report=term-missing

# Verify coverage is >= 95%
# All tests should pass (currently 135 passing tests)
```

## Pull Request Process

1. **Ensure your PR description includes:**
   - Clear description of changes made
   - Reasoning for the changes
   - Any breaking changes
   - Testing performed

2. **PR Requirements:**
   - All CI checks must pass
   - Code coverage should not decrease significantly
   - Documentation updated if needed
   - Changelog entry added (for user-facing changes)

3. **Review Process:**
   - PRs require at least one approval
   - Address reviewer feedback promptly
   - Maintain a clean commit history

## Reporting Issues

### Bug Reports

Use the bug report template and include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Ollama version)
- Relevant log output

### Feature Requests

Use the feature request template and include:
- Problem the feature would solve
- Proposed solution
- Alignment with project goals (local-first, minimal dependencies)
- Willingness to implement

## Development Guidelines

### Architecture Principles

1. **Local-First:** All functionality must work offline
2. **Minimal Dependencies:** Prefer standard library or well-established packages
3. **User-Friendly:** Clear error messages and helpful CLI interface
4. **Performance:** Efficient indexing and querying operations
5. **Configurability:** Environment-based configuration without breaking simplicity

### Adding New Features

Before implementing major features:
1. Open an issue to discuss the approach
2. Ensure alignment with project goals
3. Consider impact on local-first architecture
4. Plan for testing and documentation

### Dependencies

- New dependencies require strong justification
- Prefer packages already in the ecosystem (LlamaIndex, etc.)
- Avoid packages with many transitive dependencies
- Test that new dependencies work across platforms

## Release Process

Releases are automated via GitHub Actions:
1. Version bumps trigger builds and PyPI publishing
2. Executables are built for all platforms
3. GitHub releases are created automatically

For contributors: Focus on features and fixes - maintainers handle releases.

## Getting Help

- **Questions:** Open a discussion on GitHub
- **Issues:** Use the issue tracker
- **Community:** Engage respectfully in discussions and reviews

## Recognition

Contributors are recognized in:
- Release notes for significant contributions
- README acknowledgments
- Git commit history

Thank you for contributing to making local RAG more accessible and powerful!

---

*This contributing guide is a living document and may be updated as the project evolves.*