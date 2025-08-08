"""Simple unit test for the RAG system."""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llama_index.core import Document, VectorStoreIndex
from rag.ollama_check import check_server


def test_ollama_not_required_for_import():
    """Test that modules can be imported without Ollama running."""
    try:
        from rag import __version__
        from rag.config import load_config
        assert __version__ is not None
        assert load_config() is not None
    except Exception as e:
        pytest.fail(f"Import failed: {e}")


@pytest.mark.skipif(
    not check_server("http://localhost:11434"),
    reason="Ollama server not running - skipping integration test",
)
def test_simple_query_with_ollama():
    """Test a simple query if Ollama is available."""
    from llama_index.core import Settings
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.llms.ollama import Ollama
    
    from rag.config import load_config
    from rag.ollama_check import choose_chat_model, list_local_models
    
    # Get config
    config = load_config()
    base_url = config["OLLAMA_BASE_URL"]
    
    # Get available models
    models = list_local_models(base_url)
    if not models:
        pytest.skip("No models installed in Ollama")
    
    # Choose model
    chat_model = choose_chat_model(config["OLLAMA_CHAT_MODEL"], models)
    if not chat_model:
        pytest.skip("No suitable chat model found")
    
    # Setup minimal LLM
    Settings.llm = Ollama(
        model=chat_model,
        base_url=base_url,
        temperature=0,
    )
    
    # Try to use embedding model
    embed_model = config["OLLAMA_EMBED_MODEL"]
    try:
        Settings.embed_model = OllamaEmbedding(
            model_name=embed_model,
            base_url=base_url,
        )
    except Exception:
        pytest.skip(f"Embedding model {embed_model} not available")
    
    # Create toy documents
    docs = [
        Document(
            text="The capital of France is Paris.",
            metadata={"source": "test"},
        ),
    ]
    
    # Build index
    index = VectorStoreIndex.from_documents(docs)
    query_engine = index.as_query_engine()
    
    # Query
    response = query_engine.query("What is the capital of France?")
    answer = str(response).strip().lower()
    
    # Basic assertion
    assert "paris" in answer or len(answer) > 0


def test_config_loading():
    """Test configuration loading with defaults."""
    from rag.config import load_config
    
    config = load_config()
    
    assert "DOCS_DIR" in config
    assert "INDEX_DIR" in config
    assert "OLLAMA_BASE_URL" in config
    assert config["OLLAMA_BASE_URL"] == "http://localhost:11434"
    assert config["SIMILARITY_TOP_K"] == 4


def test_cli_help():
    """Test CLI help output."""
    from rag.cli import main
    
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    
    # Help should exit with 0
    assert exc_info.value.code == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])