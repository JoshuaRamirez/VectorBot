"""Unit tests for the ingest module."""

from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest


class TestSetupLlmSettings:
    """Test cases for setup_llm_settings function."""

    def test_SetupLlmSettings_WithValidConfig_ConfiguresSettings(self, mock_console):
        """Test LLM settings configuration with valid config."""
        # Arrange
        config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": "llama3",
            "OLLAMA_EMBED_MODEL": "nomic-embed-text",
            "REQUEST_TIMEOUT": 60.0,
            "EMBED_BATCH_SIZE": 10
        }
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models') as mock_list:
                mock_list.return_value = ["llama3", "nomic-embed-text"]
                with patch('rag.ingest.choose_chat_model') as mock_choose:
                    mock_choose.return_value = "llama3"
                    with patch('rag.ingest.ensure_embed_model') as mock_ensure:
                        mock_ensure.return_value = (True, "Model available")
                        with patch('rag.ingest.Settings') as mock_settings:
                            with patch('rag.ingest.Ollama') as mock_ollama:
                                with patch('rag.ingest.OllamaEmbedding') as mock_embedding:
                                    
                                    # Act
                                    from rag.ingest import setup_llm_settings
                                    setup_llm_settings(config)
                                    
                                    # Assert
                                    mock_ollama.assert_called_once()
                                    mock_embedding.assert_called_once()

    def test_SetupLlmSettings_WithServerDown_RaisesRuntimeError(self, mock_console):
        """Test that RuntimeError is raised when server is down."""
        # Arrange
        config = {"OLLAMA_BASE_URL": "http://localhost:11434"}
        
        with patch('rag.ingest.check_server', return_value=False):
            
            # Act & Assert
            from rag.ingest import setup_llm_settings
            with pytest.raises(RuntimeError, match="Ollama server not running"):
                setup_llm_settings(config)

    def test_SetupLlmSettings_WithNoModels_RaisesRuntimeError(self, mock_console):
        """Test that RuntimeError is raised when no models are available."""
        # Arrange
        config = {"OLLAMA_BASE_URL": "http://localhost:11434"}
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models', return_value=[]):
                
                # Act & Assert
                from rag.ingest import setup_llm_settings
                with pytest.raises(RuntimeError, match="No models installed"):
                    setup_llm_settings(config)

    def test_SetupLlmSettings_WithNoChatModel_RaisesRuntimeError(self, mock_console):
        """Test that RuntimeError is raised when no suitable chat model found."""
        # Arrange
        config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": "missing-model"
        }
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models') as mock_list:
                mock_list.return_value = ["some-model"]
                with patch('rag.ingest.choose_chat_model', return_value=None):
                    
                    # Act & Assert
                    from rag.ingest import setup_llm_settings
                    with pytest.raises(RuntimeError, match="No suitable chat model found"):
                        setup_llm_settings(config)

    def test_SetupLlmSettings_WithMissingEmbedModel_RaisesRuntimeError(self, mock_console):
        """Test that RuntimeError is raised when embed model is missing."""
        # Arrange
        config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "missing-embed"
        }
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models') as mock_list:
                mock_list.return_value = ["llama3"]
                with patch('rag.ingest.choose_chat_model') as mock_choose:
                    mock_choose.return_value = "llama3"
                    with patch('rag.ingest.ensure_embed_model') as mock_ensure:
                        mock_ensure.return_value = (False, "Model not found")
                        
                        # Act & Assert
                        from rag.ingest import setup_llm_settings
                        with pytest.raises(RuntimeError, match="Model not found"):
                            setup_llm_settings(config)

    def test_SetupLlmSettings_ConfiguresOllamaLlm_WithCorrectParameters(self, mock_console):
        """Test that Ollama LLM is configured with correct parameters."""
        # Arrange
        config = {
            "OLLAMA_BASE_URL": "http://test:8080",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "test-embed",
            "REQUEST_TIMEOUT": 120.0,
            "EMBED_BATCH_SIZE": 5
        }
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models') as mock_list:
                mock_list.return_value = ["llama3", "test-embed"]
                with patch('rag.ingest.choose_chat_model') as mock_choose:
                    mock_choose.return_value = "llama3"
                    with patch('rag.ingest.ensure_embed_model') as mock_ensure:
                        mock_ensure.return_value = (True, "OK")
                        with patch('rag.ingest.Settings') as mock_settings:
                            with patch('rag.ingest.Ollama') as mock_ollama:
                                with patch('rag.ingest.OllamaEmbedding') as mock_embedding:
                                    
                                    # Act
                                    from rag.ingest import setup_llm_settings
                                    setup_llm_settings(config)
                                    
                                    # Assert
                                    mock_ollama.assert_called_once_with(
                                        model="llama3",
                                        base_url="http://test:8080",
                                        temperature=0,
                                        request_timeout=120.0
                                    )

    def test_SetupLlmSettings_ConfiguresOllamaEmbedding_WithCorrectParameters(self, mock_console):
        """Test that Ollama embedding is configured with correct parameters."""
        # Arrange
        config = {
            "OLLAMA_BASE_URL": "http://test:8080",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "custom-embed",
            "REQUEST_TIMEOUT": 90.0,
            "EMBED_BATCH_SIZE": 15
        }
        
        with patch('rag.ingest.check_server', return_value=True):
            with patch('rag.ingest.list_local_models') as mock_list:
                mock_list.return_value = ["llama3", "custom-embed"]
                with patch('rag.ingest.choose_chat_model') as mock_choose:
                    mock_choose.return_value = "llama3"
                    with patch('rag.ingest.ensure_embed_model') as mock_ensure:
                        mock_ensure.return_value = (True, "OK")
                        with patch('rag.ingest.Settings') as mock_settings:
                            with patch('rag.ingest.Ollama'):
                                with patch('rag.ingest.OllamaEmbedding') as mock_embedding:
                                    
                                    # Act
                                    from rag.ingest import setup_llm_settings
                                    setup_llm_settings(config)
                                    
                                    # Assert
                                    mock_embedding.assert_called_once_with(
                                        model_name="custom-embed",
                                        base_url="http://test:8080",
                                        embed_batch_size=15
                                    )


class TestLoadDocuments:
    """Test cases for load_documents function."""

    def test_LoadDocuments_WithNonexistentDir_CreatesDirectoryAndReturnsEmpty(self, mock_console):
        """Test that nonexistent directory is created and empty list returned."""
        # Arrange
        docs_dir = Path("/test/docs")
        
        with patch.object(Path, 'exists', return_value=False):
            with patch.object(Path, 'mkdir') as mock_mkdir:
                
                # Act
                from rag.ingest import load_documents
                result = load_documents(docs_dir)
                
                # Assert
                mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
                assert result == []

    def test_LoadDocuments_WithNoFiles_ReturnsEmptyList(self, mock_console):
        """Test that empty directory returns empty list."""
        # Arrange
        docs_dir = Path("/test/docs")
        
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'glob', return_value=[]):
                
                # Act
                from rag.ingest import load_documents
                result = load_documents(docs_dir)
                
                # Assert
                assert result == []

    def test_LoadDocuments_WithValidFiles_LoadsDocuments(self, mock_console):
        """Test that valid files are loaded correctly."""
        # Arrange
        docs_dir = Path("/test/docs")
        mock_file1 = Mock(spec=Path)
        mock_file1.stat.return_value.st_size = 1024  # 1KB
        mock_file2 = Mock(spec=Path)
        mock_file2.stat.return_value.st_size = 2048  # 2KB
        
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'glob') as mock_glob:
                mock_glob.side_effect = [
                    [mock_file1],  # *.txt files
                    [],  # **/*.txt files
                    [mock_file2],  # *.md files
                    [],  # **/*.md files
                    [],  # other extensions
                    [],
                    [],
                    [],
                    [],
                    []
                ]
                with patch('rag.ingest.SimpleDirectoryReader') as mock_reader:
                    mock_reader_instance = Mock()
                    mock_documents = [Mock(), Mock()]
                    mock_reader_instance.load_data.return_value = mock_documents
                    mock_reader.return_value = mock_reader_instance
                    
                    # Act
                    from rag.ingest import load_documents
                    result = load_documents(docs_dir)
                    
                    # Assert
                    assert result == mock_documents
                    mock_reader.assert_called_once()

    def test_LoadDocuments_WithLargeFiles_SkipsLargeFiles(self, mock_console):
        """Test that files larger than 20MB are skipped."""
        # Arrange
        docs_dir = Path("/test/docs")
        mock_small_file = Mock(spec=Path)
        mock_small_file.stat.return_value.st_size = 1024 * 1024  # 1MB
        mock_small_file.name = "small.txt"
        mock_large_file = Mock(spec=Path)
        mock_large_file.stat.return_value.st_size = 25 * 1024 * 1024  # 25MB
        mock_large_file.name = "large.txt"
        
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'glob') as mock_glob:
                mock_glob.side_effect = [
                    [mock_small_file, mock_large_file],  # *.txt files
                    [],  # **/*.txt files
                    [],  # other extensions
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []
                ]
                with patch('rag.ingest.SimpleDirectoryReader') as mock_reader:
                    mock_reader_instance = Mock()
                    mock_documents = [Mock()]
                    mock_reader_instance.load_data.return_value = mock_documents
                    mock_reader.return_value = mock_reader_instance
                    
                    # Act
                    from rag.ingest import load_documents
                    result = load_documents(docs_dir)
                    
                    # Assert
                    assert result == mock_documents
                    # Should print warning about large file
                    mock_console.print.assert_called()

    def test_LoadDocuments_WithOnlyLargeFiles_ReturnsEmptyList(self, mock_console):
        """Test that only large files results in empty list."""
        # Arrange
        docs_dir = Path("/test/docs")
        mock_large_file = Mock(spec=Path)
        mock_large_file.stat.return_value.st_size = 25 * 1024 * 1024  # 25MB
        mock_large_file.name = "large.txt"
        
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'glob') as mock_glob:
                mock_glob.side_effect = [
                    [mock_large_file],  # *.txt files
                    [],  # other calls return empty
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []
                ]
                
                # Act
                from rag.ingest import load_documents
                result = load_documents(docs_dir)
                
                # Assert
                assert result == []

    def test_LoadDocuments_ConfiguresSimpleDirectoryReader_WithCorrectParameters(self, mock_console):
        """Test that SimpleDirectoryReader is configured with correct parameters."""
        # Arrange
        docs_dir = Path("/test/docs")
        mock_file = Mock(spec=Path)
        mock_file.stat.return_value.st_size = 1024
        
        with patch.object(Path, 'exists', return_value=True):
            with patch.object(Path, 'glob') as mock_glob:
                mock_glob.side_effect = [
                    [mock_file],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    [],
                    []
                ]
                with patch('rag.ingest.SimpleDirectoryReader') as mock_reader:
                    mock_reader_instance = Mock()
                    mock_reader_instance.load_data.return_value = []
                    mock_reader.return_value = mock_reader_instance
                    
                    # Act
                    from rag.ingest import load_documents
                    load_documents(docs_dir)
                    
                    # Assert
                    mock_reader.assert_called_once_with(
                        input_dir=str(docs_dir),
                        recursive=True,
                        exclude_hidden=True,
                        required_exts=[".txt", ".md", ".pdf", ".json", ".csv"]
                    )


class TestIngest:
    """Test cases for ingest function."""

    def test_Ingest_WithExistingIndex_LoadsExistingIndex(self, mock_console):
        """Test that existing index is loaded when available."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
                    with patch('rag.ingest.StorageContext') as mock_storage:
                        with patch('rag.ingest.load_index_from_storage') as mock_load:
                            mock_index = Mock()
                            mock_load.return_value = mock_index
                            
                            # Act
                            from rag.ingest import ingest
                            ingest()
                            
                            # Assert
                            mock_storage.from_defaults.assert_called_once()
                            mock_load.assert_called_once()

    def test_Ingest_WithCorruptedExistingIndex_CreatesNewIndex(self, mock_console):
        """Test that corrupted existing index triggers new index creation."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
                    with patch('rag.ingest.StorageContext'):
                        with patch('rag.ingest.load_index_from_storage', side_effect=Exception("Corrupted")):
                            with patch('rag.ingest.load_documents') as mock_load_docs:
                                mock_load_docs.return_value = [Mock(), Mock()]
                                with patch('rag.ingest.VectorStoreIndex') as mock_index_class:
                                    mock_index = Mock()
                                    mock_storage_context = Mock()
                                    mock_index.storage_context = mock_storage_context
                                    mock_index_class.from_documents.return_value = mock_index
                                    with patch.object(Path, 'mkdir'):
                                        
                                        # Act
                                        from rag.ingest import ingest
                                        ingest()
                                        
                                        # Assert
                                        mock_index_class.from_documents.assert_called_once()

    def test_Ingest_WithNoExistingIndex_CreatesNewIndex(self, mock_console):
        """Test that new index is created when none exists."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=False):
                    with patch('rag.ingest.load_documents') as mock_load_docs:
                        mock_documents = [Mock(), Mock()]
                        mock_load_docs.return_value = mock_documents
                        with patch('rag.ingest.VectorStoreIndex') as mock_index_class:
                            mock_index = Mock()
                            mock_storage_context = Mock()
                            mock_index.storage_context = mock_storage_context
                            mock_index_class.from_documents.return_value = mock_index
                            with patch.object(Path, 'mkdir'):
                                
                                # Act
                                from rag.ingest import ingest
                                ingest()
                                
                                # Assert
                                mock_index_class.from_documents.assert_called_once_with(
                                    mock_documents,
                                    show_progress=False
                                )

    def test_Ingest_WithNoDocuments_RaisesRuntimeError(self, mock_console):
        """Test that RuntimeError is raised when no documents found."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=False):
                    with patch('rag.ingest.load_documents', return_value=[]):
                        
                        # Act & Assert
                        from rag.ingest import ingest
                        with pytest.raises(RuntimeError, match="No documents found"):
                            ingest()

    def test_Ingest_WithVerboseFlag_PassesToVectorStoreIndex(self, mock_console):
        """Test that verbose flag is passed to VectorStoreIndex."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=False):
                    with patch('rag.ingest.load_documents') as mock_load_docs:
                        mock_load_docs.return_value = [Mock()]
                        with patch('rag.ingest.VectorStoreIndex') as mock_index_class:
                            mock_index = Mock()
                            mock_storage_context = Mock()
                            mock_index.storage_context = mock_storage_context
                            mock_index_class.from_documents.return_value = mock_index
                            with patch.object(Path, 'mkdir'):
                                
                                # Act
                                from rag.ingest import ingest
                                ingest(verbose=True)
                                
                                # Assert
                                _, kwargs = mock_index_class.from_documents.call_args
                                assert kwargs['show_progress'] is True

    def test_Ingest_WithSpecificEnvName_PassesToLoadConfig(self, mock_console):
        """Test that specific env name is passed to load_config."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config) as mock_load_config:
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=True):
                    with patch('rag.ingest.StorageContext'):
                        with patch('rag.ingest.load_index_from_storage'):
                            
                            # Act
                            from rag.ingest import ingest
                            ingest(env_name="production")
                            
                            # Assert
                            mock_load_config.assert_called_once_with("production")

    def test_Ingest_PersistsIndex_ToCorrectDirectory(self, mock_console):
        """Test that index is persisted to correct directory."""
        # Arrange
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index")
        }
        
        with patch('rag.ingest.load_config', return_value=mock_config):
            with patch('rag.ingest.setup_llm_settings'):
                with patch.object(Path, 'exists', return_value=False):
                    with patch('rag.ingest.load_documents') as mock_load_docs:
                        mock_load_docs.return_value = [Mock()]
                        with patch('rag.ingest.VectorStoreIndex') as mock_index_class:
                            mock_index = Mock()
                            mock_storage_context = Mock()
                            mock_index.storage_context = mock_storage_context
                            mock_index_class.from_documents.return_value = mock_index
                            with patch.object(Path, 'mkdir') as mock_mkdir:
                                
                                # Act
                                from rag.ingest import ingest
                                ingest()
                                
                                # Assert
                                mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
                                mock_storage_context.persist.assert_called_once_with(
                                    persist_dir=str(mock_config["INDEX_DIR"])
                                )