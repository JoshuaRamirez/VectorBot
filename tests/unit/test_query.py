"""Unit tests for the query module."""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Any
import pytest


class TestAsk:
    """Test cases for ask function."""

    def test_Ask_WithValidQuestion_ReturnsAnswer(self, mock_console: Any) -> None:
        """Test that valid question returns proper answer."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        question = "What is the capital of France?"
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Paris is the capital of France."))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext') as mock_storage:
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask(question)

                                    # Assert
                                    assert result == "Paris is the capital of France."
                                    mock_query_engine.query.assert_called_once_with(question)

    def test_Ask_WithNoIndexDir_RaisesRuntimeError(self, mock_console: Any) -> None:
        """Test that missing index directory raises RuntimeError."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = False
                    mock_get_index_dir.return_value = mock_index_dir

                    # Act & Assert
                    from rag.query import ask
                    with pytest.raises(RuntimeError, match="not indexed"):
                        ask("test question")

    def test_Ask_WithNoDocstoreJson_RaisesRuntimeError(self, mock_console: Any) -> None:
        """Test that missing docstore.json raises RuntimeError."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    # Index dir exists but docstore.json doesn't
                    mock_docstore_path = Mock()
                    mock_docstore_path.exists.return_value = False
                    mock_index_dir.__truediv__ = Mock(return_value=mock_docstore_path)
                    mock_get_index_dir.return_value = mock_index_dir

                    # Act & Assert
                    from rag.query import ask
                    with pytest.raises(RuntimeError, match="not indexed"):
                        ask("test question")

    def test_Ask_WithCustomTopK_UsesCustomValue(self, mock_console: Any) -> None:
        """Test that custom top_k is used correctly."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        custom_top_k = 8
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    ask("test question", top_k=custom_top_k)

                                    # Assert
                                    mock_index.as_query_engine.assert_called_once_with(
                                        similarity_top_k=custom_top_k,
                                        streaming=False
                                    )

    def test_Ask_WithDefaultTopK_UsesDefaultValue(self, mock_console: Any) -> None:
        """Test that default top_k (4) is used when not specified."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    ask("test question")

                                    # Assert - default top_k is 4
                                    mock_index.as_query_engine.assert_called_once_with(
                                        similarity_top_k=4,
                                        streaming=False
                                    )

    def test_Ask_WithEmptyResponse_ReturnsNoRelevantInfo(self, mock_console: Any) -> None:
        """Test that empty response returns no relevant info message."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value=""))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask("test question")

                                    # Assert
                                    assert result == "No relevant information found in the indexed documents."

    def test_Ask_WithEmptyResponseString_ReturnsNoRelevantInfo(self, mock_console: Any) -> None:
        """Test that 'Empty Response' string returns no relevant info message."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Empty Response"))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask("test question")

                                    # Assert
                                    assert result == "No relevant information found in the indexed documents."

    def test_Ask_WithShowSources_IncludesSourceInformation(self, mock_console: Any) -> None:
        """Test that show_sources includes source information in response."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_source_node = Mock()
        mock_source_node.metadata = {"file_name": "test_document.txt"}
        mock_source_node.score = 0.85

        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        mock_response.source_nodes = [mock_source_node]

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask("test question", show_sources=True)

                                    # Assert
                                    assert "Test answer" in result
                                    assert "[dim]Sources:[/dim]" in result
                                    assert "test_document.txt" in result
                                    assert "0.850" in result

    def test_Ask_WithShowSourcesButNoSourceNodes_DoesNotIncludeSources(self, mock_console: Any) -> None:
        """Test that show_sources without source_nodes doesn't include sources."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock(spec=['__str__'])  # Specify only __str__ attribute
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        # No source_nodes attribute - using spec to ensure it doesn't exist

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask("test question", show_sources=True)

                                    # Assert
                                    assert result == "Test answer"
                                    assert "Sources:" not in result

    def test_Ask_WithVerboseFlag_PrintsLoadingMessages(self, mock_console: Any) -> None:
        """Test that verbose flag prints loading messages."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    ask("test question", verbose=True)

                                    # Assert
                                    # Should have called console.print for verbose output
                                    assert mock_console.print.call_count >= 1

    def test_Ask_WithSpecificStoreName_UsesCorrectStore(self, mock_console: Any) -> None:
        """Test that specific store_name is used correctly."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))

        with patch('rag.query.resolve_store', return_value="my-store") as mock_resolve_store:
            with patch('rag.query.get_store', return_value=mock_store) as mock_get_store:
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    ask("test question", store_name="my-store")

                                    # Assert
                                    mock_resolve_store.assert_called_once_with("my-store")
                                    mock_get_store.assert_called_once_with("my-store")

    def test_Ask_LoadsStorageContext_WithCorrectPersistDir(self, mock_console: Any) -> None:
        """Test that StorageContext is loaded with correct persist directory."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = MagicMock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_index_dir.__str__ = Mock(return_value="/custom/index")
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext') as mock_storage:
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    ask("test question")

                                    # Assert
                                    mock_storage.from_defaults.assert_called_once()
                                    # Get the actual call arguments
                                    actual_call = mock_storage.from_defaults.call_args
                                    # Check that persist_dir was passed
                                    assert 'persist_dir' in str(actual_call)

    def test_Ask_WithSourceNodeWithoutMetadata_HandlesGracefully(self, mock_console: Any) -> None:
        """Test that source node without metadata is handled gracefully."""
        # Arrange
        mock_store = {"chat_model": "llama3.1"}
        mock_global_config = {
            "ollama_base_url": "http://localhost:11434",
            "ollama_embed_model": "nomic-embed-text",
            "request_timeout": 60.0,
            "embed_batch_size": 10,
        }
        mock_source_node = Mock(spec=['score'])  # Only has score, no metadata
        mock_source_node.score = 0.85

        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        mock_response.source_nodes = [mock_source_node]

        with patch('rag.query.resolve_store', return_value="default"):
            with patch('rag.query.get_store', return_value=mock_store):
                with patch('rag.query.get_store_index_dir') as mock_get_index_dir:
                    mock_index_dir = Mock()
                    mock_index_dir.exists.return_value = True
                    mock_index_dir.__truediv__ = Mock(return_value=Mock(exists=Mock(return_value=True)))
                    mock_get_index_dir.return_value = mock_index_dir
                    with patch('rag.query.get_global_config', return_value=mock_global_config):
                        with patch('rag.query.setup_query_llm_settings'):
                            with patch('rag.query.StorageContext'):
                                with patch('rag.query.load_index_from_storage') as mock_load_index:
                                    mock_index = Mock()
                                    mock_query_engine = Mock()
                                    mock_query_engine.query.return_value = mock_response
                                    mock_index.as_query_engine.return_value = mock_query_engine
                                    mock_load_index.return_value = mock_index

                                    # Act
                                    from rag.query import ask
                                    result = ask("test question", show_sources=True)

                                    # Assert
                                    assert "Test answer" in result
                                    # Should handle gracefully without crashing


class TestQuery:
    """Test cases for query function."""

    def test_Query_WithValidQuestion_PrintsAnswer(self, mock_console: Any) -> None:
        """Test that query prints the answer from ask function."""
        # Arrange
        question = "What is AI?"
        expected_answer = "AI is artificial intelligence."

        with patch('rag.query.ask', return_value=expected_answer) as mock_ask:

            # Act
            from rag.query import query
            query(question)

            # Assert
            # New signature: ask(question, store_name, show_sources, top_k, verbose)
            mock_ask.assert_called_once_with(question, None, False, 4, False)
            mock_console.print.assert_called_once()
            call_args = mock_console.print.call_args[0][0]
            assert expected_answer in call_args

    def test_Query_WithAllParameters_PassesToAsk(self, mock_console: Any) -> None:
        """Test that all parameters are passed correctly to ask function."""
        # Arrange
        question = "Test question"
        store_name = "my-store"
        show_sources = True
        top_k = 5
        verbose = True

        with patch('rag.query.ask', return_value="Test answer") as mock_ask:

            # Act
            from rag.query import query
            query(question, store_name, show_sources, top_k, verbose)

            # Assert
            mock_ask.assert_called_once_with(
                question, store_name, show_sources, top_k, verbose
            )

    def test_Query_WithException_PrintsErrorAndReraises(self, mock_console: Any) -> None:
        """Test that exceptions are printed and re-raised."""
        # Arrange
        question = "Test question"
        error_message = "Index not found"

        with patch('rag.query.ask', side_effect=RuntimeError(error_message)) as mock_ask:

            # Act & Assert
            from rag.query import query
            with pytest.raises(RuntimeError, match=error_message):
                query(question)

            # Should print error message
            mock_console.print.assert_called_once()
            call_args = mock_console.print.call_args[0][0]
            assert error_message in call_args

    def test_Query_WithDefaultParameters_UsesCorrectDefaults(self, mock_console: Any) -> None:
        """Test that default parameters are used correctly."""
        # Arrange
        question = "Default test"

        with patch('rag.query.ask', return_value="Default answer") as mock_ask:

            # Act
            from rag.query import query
            query(question)

            # Assert
            # New signature: ask(question, store_name, show_sources, top_k, verbose)
            # Defaults: store_name=None, show_sources=False, top_k=4, verbose=False
            mock_ask.assert_called_once_with(question, None, False, 4, False)
