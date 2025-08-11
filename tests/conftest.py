"""Test configuration and shared fixtures for the RAG application tests."""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import MagicMock, Mock

import pytest

# Add src to Python path for test imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Provide a mock configuration dictionary for testing."""
    return {
        "DOCS_DIR": Path("/test/docs"),
        "INDEX_DIR": Path("/test/index"),
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "OLLAMA_CHAT_MODEL": "llama3.1",
        "OLLAMA_EMBED_MODEL": "nomic-embed-text",
        "SIMILARITY_TOP_K": 4,
        "LOG_LEVEL": "INFO",
        "ENABLE_VERBOSE_OUTPUT": False,
        "REQUEST_TIMEOUT": 60.0,
        "EMBED_BATCH_SIZE": 10,
    }


@pytest.fixture
def mock_models_list() -> List[str]:
    """Provide a mock list of available Ollama models."""
    return [
        "llama3.1:latest",
        "llama3:latest",
        "nomic-embed-text:latest",
        "mistral:latest",
    ]


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for HTTP calls."""
    from unittest.mock import patch
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "models": [
            {"name": "llama3.1:latest"},
            {"name": "nomic-embed-text:latest"},
            {"name": "mistral:latest"},
        ]
    }
    
    with patch("requests.get", return_value=mock_response) as mock:
        yield mock


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for CLI command execution."""
    from unittest.mock import patch
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "NAME            \tID              \tSIZE  \tMODIFIED    \nllama3.1:latest \t1234567890abcdef\t7.3GB \t2 days ago\n"
    
    with patch("subprocess.run", return_value=mock_result) as mock:
        yield mock


@pytest.fixture
def mock_path_exists():
    """Mock Path.exists() method."""
    from unittest.mock import patch
    with patch.object(Path, "exists", return_value=True) as mock:
        yield mock


@pytest.fixture
def mock_path_mkdir():
    """Mock Path.mkdir() method."""
    from unittest.mock import patch
    with patch.object(Path, "mkdir") as mock:
        yield mock


@pytest.fixture
def mock_load_dotenv():
    """Mock dotenv loading."""
    from unittest.mock import patch
    with patch("rag.config.load_dotenv") as mock:
        yield mock


@pytest.fixture
def mock_console():
    """Mock Rich console for output testing."""
    from unittest.mock import patch, MagicMock
    
    # Create mocks for all modules that use console
    mocks = {}
    
    # Patch console in all modules that use it
    with patch("rag.config.console") as config_mock:
        with patch("rag.query.console") as query_mock:
            with patch("rag.cli.console") as cli_mock:
                with patch("rag.ollama_check.console") as ollama_mock:
                    with patch("rag.ingest.console") as ingest_mock:
                        # Make them all the same mock for consistency
                        mock = MagicMock()
                        config_mock.print = mock.print
                        query_mock.print = mock.print
                        cli_mock.print = mock.print
                        ollama_mock.print = mock.print
                        ingest_mock.print = mock.print
                        
                        yield mock


@pytest.fixture
def mock_llama_index_settings():
    """Mock LlamaIndex Settings object."""
    from unittest.mock import patch
    with patch("llama_index.core.Settings") as mock:
        mock.llm = MagicMock()
        mock.embed_model = MagicMock()
        yield mock


@pytest.fixture
def mock_ollama_llm():
    """Mock Ollama LLM class."""
    from unittest.mock import patch
    with patch("llama_index.llms.ollama.Ollama") as mock:
        yield mock


@pytest.fixture
def mock_ollama_embedding():
    """Mock Ollama embedding class."""
    from unittest.mock import patch
    with patch("llama_index.embeddings.ollama.OllamaEmbedding") as mock:
        yield mock


@pytest.fixture
def mock_simple_directory_reader():
    """Mock SimpleDirectoryReader for document loading."""
    from unittest.mock import patch
    mock_reader = Mock()
    mock_documents = [
        Mock(text="Sample document 1", metadata={"file_name": "doc1.txt"}),
        Mock(text="Sample document 2", metadata={"file_name": "doc2.txt"}),
    ]
    mock_reader.load_data.return_value = mock_documents
    
    with patch("llama_index.core.SimpleDirectoryReader", return_value=mock_reader) as mock:
        yield mock


@pytest.fixture
def mock_vector_store_index():
    """Mock VectorStoreIndex for indexing operations."""
    from unittest.mock import patch
    mock_index = Mock()
    mock_storage_context = Mock()
    mock_index.storage_context = mock_storage_context
    mock_query_engine = Mock()
    mock_index.as_query_engine.return_value = mock_query_engine
    
    with patch("llama_index.core.VectorStoreIndex") as mock_class:
        mock_class.from_documents.return_value = mock_index
        yield mock_class, mock_index, mock_query_engine


@pytest.fixture
def mock_storage_context():
    """Mock StorageContext for index persistence."""
    from unittest.mock import patch
    mock_context = Mock()
    with patch("llama_index.core.StorageContext") as mock_class:
        mock_class.from_defaults.return_value = mock_context
        yield mock_class, mock_context


@pytest.fixture
def mock_load_index_from_storage():
    """Mock load_index_from_storage function."""
    from unittest.mock import patch
    mock_index = Mock()
    with patch("llama_index.core.load_index_from_storage", return_value=mock_index) as mock:
        yield mock, mock_index


@pytest.fixture
def clean_environment():
    """Clean environment variables before and after test."""
    # Store original values
    original_env = {}
    test_vars = [
        "DOCS_DIR", "INDEX_DIR", "OLLAMA_BASE_URL", "OLLAMA_CHAT_MODEL",
        "OLLAMA_EMBED_MODEL", "SIMILARITY_TOP_K", "LOG_LEVEL",
        "ENABLE_VERBOSE_OUTPUT", "REQUEST_TIMEOUT", "EMBED_BATCH_SIZE",
        "RAG_ENV", "RAG_VERBOSE"
    ]
    
    for var in test_vars:
        if var in os.environ:
            original_env[var] = os.environ[var]
            del os.environ[var]
    
    yield
    
    # Restore original values
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]
        if var in original_env:
            os.environ[var] = original_env[var]


@pytest.fixture
def temp_files(tmp_path):
    """Create temporary files for testing file operations."""
    # Create test directories
    docs_dir = tmp_path / "docs"
    index_dir = tmp_path / "index"
    docs_dir.mkdir()
    index_dir.mkdir()
    
    # Create test files
    test_files = {
        "doc1.txt": "This is the first test document.",
        "doc2.md": "# Test Document\nThis is a markdown document.",
        "doc3.pdf": "PDF content placeholder",
    }
    
    for filename, content in test_files.items():
        (docs_dir / filename).write_text(content)
    
    return {
        "docs_dir": docs_dir,
        "index_dir": index_dir,
        "files": test_files,
    }


class MockQueryResponse:
    """Mock query response object for testing."""
    
    def __init__(self, text: str = "Mock response", source_nodes: List = None):
        self.text = text
        self.source_nodes = source_nodes or []
    
    def __str__(self):
        return self.text


@pytest.fixture
def mock_query_response():
    """Provide a mock query response."""
    mock_node = Mock()
    mock_node.metadata = {"file_name": "test.txt"}
    mock_node.score = 0.85
    
    return MockQueryResponse(
        text="This is a mock response",
        source_nodes=[mock_node]
    )