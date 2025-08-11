# Test Suite Documentation

This directory contains comprehensive unit and integration tests for the Local Ollama RAG project.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and test configuration
├── __init__.py             # Test package initialization
├── README.md               # This documentation
├── unit/                   # Unit tests (fast, isolated, mocked)
│   ├── __init__.py
│   ├── test_version.py     # Tests for version module
│   ├── test_config.py      # Tests for config module
│   ├── test_ollama_check.py # Tests for ollama_check module
│   ├── test_ingest.py      # Tests for ingest module
│   ├── test_query.py       # Tests for query module
│   └── test_cli.py         # Tests for cli module
└── integration/            # Integration tests (may require external services)
    ├── __init__.py
    └── test_integration.py  # Full system integration tests
```

## Test Philosophy

### Unit Tests
- Follow the AAA (Arrange-Act-Assert) pattern
- Test exactly one unit of functionality per test
- Use extensive mocking to isolate the system under test
- Fast execution (< 1 second per test)
- No external dependencies (network, filesystem, databases)
- Named using the pattern: `ClassName_MethodName_ExpectedOutcome`

### Integration Tests
- Test interactions between components
- May require external services (Ollama server)
- Test real file system operations where appropriate
- Longer execution time acceptable
- Use `@pytest.mark.skipif` for conditional execution

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Only Unit Tests
```bash
pytest tests/unit/
```

### Run Only Integration Tests
```bash
pytest tests/integration/
```

### Run Specific Test File
```bash
pytest tests/unit/test_config.py
```

### Run Specific Test Method
```bash
pytest tests/unit/test_config.py::TestLoadConfig::test_LoadConfig_WithDefaults_ReturnsExpectedStructure
```

### Run with Verbose Output
```bash
pytest -v
```

### Run with Coverage Report
```bash
pytest --cov=rag --cov-report=html
```

## Test Naming Convention

All tests follow the naming pattern: `ClassName_MethodName_ExpectedOutcome`

Examples:
- `test_LoadConfig_WithDefaults_ReturnsExpectedStructure`
- `test_CheckServer_WithSuccessfulResponse_ReturnsTrue`
- `test_Ask_WithValidQuestion_ReturnsAnswer`

This naming convention makes it immediately clear:
1. What class/module is being tested
2. What method/function is being tested
3. What the expected behavior is

## Test Categories

### Unit Tests by Module

#### `test_version.py`
- Tests version string accessibility
- Tests version format validation
- Tests module documentation

#### `test_config.py`
- Tests configuration loading and validation
- Tests environment variable handling
- Tests path resolution
- Tests error conditions

#### `test_ollama_check.py`
- Tests server connectivity checks
- Tests model listing and selection
- Tests health check functionality
- All HTTP requests are mocked

#### `test_ingest.py`
- Tests document loading and indexing
- Tests LLM settings configuration
- Tests error handling
- All LlamaIndex components are mocked

#### `test_query.py`
- Tests query processing and response handling
- Tests source citation functionality
- Tests error conditions
- All dependencies are mocked

#### `test_cli.py`
- Tests command-line argument parsing
- Tests command execution routing
- Tests error handling and exit codes
- All function calls are mocked

### Integration Tests

#### `test_integration.py`
- Tests that require actual Ollama server
- Tests real configuration file loading
- Tests CLI functionality end-to-end
- Uses conditional skipping for missing dependencies

## Fixtures and Test Utilities

The `conftest.py` file provides shared fixtures:

- `mock_config`: Standard configuration dictionary
- `mock_models_list`: List of available Ollama models
- `mock_requests_get`: Mock HTTP requests
- `mock_subprocess_run`: Mock CLI command execution
- `clean_environment`: Clean environment variables
- `temp_files`: Temporary file creation
- Various LlamaIndex component mocks

## Mocking Strategy

### External Dependencies
- HTTP requests (`requests.get`)
- Subprocess calls (`subprocess.run`)
- File system operations (`Path.exists`, `Path.mkdir`)
- LlamaIndex components (`Settings`, `VectorStoreIndex`, etc.)

### Configuration
- Environment variables are cleaned between tests
- Path resolution is mocked for consistent behavior
- Configuration validation is isolated

### Console Output
- Rich console output is mocked for testing
- Error messages and verbose output are captured

## Best Practices

1. **One Assertion Per Test**: Each test should verify exactly one behavior
2. **Descriptive Names**: Test names clearly describe the scenario and expectation
3. **Arrange-Act-Assert**: Clear separation of test setup, execution, and verification
4. **Mock External Dependencies**: Unit tests should not depend on external services
5. **Test Error Conditions**: Include tests for failure scenarios
6. **Clean Test Environment**: Each test runs in isolation

## Continuous Integration

These tests are designed to run in CI environments:

- Unit tests run without any external dependencies
- Integration tests are skipped when dependencies are unavailable
- All tests use deterministic mocking for reproducible results
- No network calls in unit tests
- No file system modifications outside temp directories

## Adding New Tests

When adding new functionality:

1. Add unit tests for each public method/function
2. Follow the established naming convention
3. Use appropriate fixtures from `conftest.py`
4. Mock all external dependencies
5. Test both success and failure scenarios
6. Update this documentation if adding new test categories

## Performance Expectations

- Unit tests: < 1 second each
- Integration tests: < 30 seconds each
- Full test suite: < 5 minutes

If tests are slower, consider:
- Adding more mocking
- Reducing test data size
- Splitting complex tests into smaller units