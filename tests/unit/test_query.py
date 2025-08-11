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
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        question = "What is the capital of France?"
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Paris is the capital of France."))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
        mock_config = {
            "INDEX_DIR": Path("/nonexistent/index"),
            "SIMILARITY_TOP_K": 4
        }
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch.object(Path, 'exists', return_value=False):
                
                # Act & Assert
                from rag.query import ask
                with pytest.raises(RuntimeError, match="No index found"):
                    ask("test question")

    def test_Ask_WithNoDocstoreJson_RaisesRuntimeError(self, mock_console: Any) -> None:
        """Test that missing docstore.json raises RuntimeError."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch.object(Path, 'exists', autospec=True) as mock_exists:
                # INDEX_DIR exists but docstore.json doesn't
                # Path.exists() is called as a bound method, so self is the Path instance
                def exists_side_effect(path_self: Any) -> bool:
                    path_str = str(path_self).replace('\\', '/')
                    # Only the index dir exists, not docstore.json
                    return path_str == "/test/index" or path_str.endswith("/test/index")
                mock_exists.side_effect = exists_side_effect
                
                # Act & Assert
                from rag.query import ask
                with pytest.raises(RuntimeError, match="No index found"):
                    ask("test question")

    def test_Ask_WithCustomSimilarityTopK_UsesCustomValue(self, mock_console: Any) -> None:
        """Test that custom similarity_top_k is used correctly."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        custom_top_k = 8
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
                    with patch('rag.query.StorageContext'):
                        with patch('rag.query.load_index_from_storage') as mock_load_index:
                            mock_index = Mock()
                            mock_query_engine = Mock()
                            mock_query_engine.query.return_value = mock_response
                            mock_index.as_query_engine.return_value = mock_query_engine
                            mock_load_index.return_value = mock_index
                            
                            # Act
                            from rag.query import ask
                            ask("test question", similarity_top_k=custom_top_k)
                            
                            # Assert
                            mock_index.as_query_engine.assert_called_once_with(
                                similarity_top_k=custom_top_k,
                                streaming=False
                            )

    def test_Ask_WithDefaultSimilarityTopK_UsesConfigValue(self, mock_console: Any) -> None:
        """Test that default similarity_top_k uses config value."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 6
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
                            
                            # Assert
                            mock_index.as_query_engine.assert_called_once_with(
                                similarity_top_k=6,
                                streaming=False
                            )

    def test_Ask_WithEmptyResponse_ReturnsNoRelevantInfo(self, mock_console: Any) -> None:
        """Test that empty response returns no relevant info message."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value=""))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Empty Response"))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_source_node = Mock()
        mock_source_node.metadata = {"file_name": "test_document.txt"}
        mock_source_node.score = 0.85
        
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        mock_response.source_nodes = [mock_source_node]
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock(spec=['__str__'])  # Specify only __str__ attribute
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        # No source_nodes attribute - using spec to ensure it doesn't exist
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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

    def test_Ask_WithSpecificEnvName_PassesToLoadConfig(self, mock_console: Any) -> None:
        """Test that specific env name is passed to load_config."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        
        with patch('rag.query.load_config', return_value=mock_config) as mock_load_config:
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
                    with patch('rag.query.StorageContext'):
                        with patch('rag.query.load_index_from_storage') as mock_load_index:
                            mock_index = Mock()
                            mock_query_engine = Mock()
                            mock_query_engine.query.return_value = mock_response
                            mock_index.as_query_engine.return_value = mock_query_engine
                            mock_load_index.return_value = mock_index
                            
                            # Act
                            from rag.query import ask
                            ask("test question", env_name="production")
                            
                            # Assert
                            mock_load_config.assert_called_once_with("production")

    def test_Ask_LoadsStorageContext_WithCorrectPersistDir(self, mock_console: Any) -> None:
        """Test that StorageContext is loaded with correct persist directory."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/custom/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
                            # Check that it was called with the string version of the path
                            mock_storage.from_defaults.assert_called_once()
                            # Get the actual call arguments
                            actual_call = mock_storage.from_defaults.call_args
                            # Check that persist_dir was passed and contains expected path
                            assert 'persist_dir' in str(actual_call)
                            assert 'custom' in str(actual_call)
                            assert 'index' in str(actual_call)

    def test_Ask_WithSourceNodeWithoutMetadata_HandlesGracefully(self, mock_console: Any) -> None:
        """Test that source node without metadata is handled gracefully."""
        # Arrange
        mock_config = {
            "INDEX_DIR": Path("/test/index"),
            "SIMILARITY_TOP_K": 4
        }
        mock_source_node = Mock()
        mock_source_node.score = 0.85  # Add score as a float
        # No metadata attribute
        
        mock_response = Mock()
        mock_response.configure_mock(__str__=Mock(return_value="Test answer"))
        mock_response.source_nodes = [mock_source_node]
        
        with patch('rag.query.load_config', return_value=mock_config):
            with patch('rag.query.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
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
            mock_ask.assert_called_once_with(question, None, False, False, None)
            mock_console.print.assert_called_once()
            call_args = mock_console.print.call_args[0][0]
            assert expected_answer in call_args

    def test_Query_WithAllParameters_PassesToAsk(self, mock_console: Any) -> None:
        """Test that all parameters are passed correctly to ask function."""
        # Arrange
        question = "Test question"
        similarity_top_k = 5
        show_sources = True
        verbose = True
        env_name = "production"
        
        with patch('rag.query.ask', return_value="Test answer") as mock_ask:
            
            # Act
            from rag.query import query
            query(question, similarity_top_k, show_sources, verbose, env_name)
            
            # Assert
            mock_ask.assert_called_once_with(
                question, similarity_top_k, show_sources, verbose, env_name
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
            mock_ask.assert_called_once_with(question, None, False, False, None)