"""Unit tests for the config module."""

import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest


class TestGetExecutableDir:
    """Test cases for get_executable_dir function."""

    def test_GetExecutableDir_WhenNotFrozen_ReturnsCorrectPath(self):
        """Test executable directory detection when running as script."""
        # Arrange
        with patch('sys.frozen', False, create=True):
            with patch('rag.config.Path') as mock_path:
                mock_file_path = Mock()
                mock_parent_chain = Mock()
                mock_file_path.parent.parent.parent = mock_parent_chain
                mock_path.return_value = mock_file_path
                
                # Act
                from rag.config import get_executable_dir
                result = get_executable_dir()
                
                # Assert
                assert result == mock_parent_chain

    def test_GetExecutableDir_WhenFrozen_ReturnsExecutableParent(self):
        """Test executable directory detection when running as executable."""
        # Arrange
        with patch('sys.frozen', True, create=True):
            with patch('sys.executable', '/path/to/executable'):
                with patch('rag.config.Path') as mock_path:
                    mock_executable_path = Mock()
                    mock_parent = Mock()
                    mock_executable_path.parent = mock_parent
                    mock_path.return_value = mock_executable_path
                    
                    # Act
                    from rag.config import get_executable_dir
                    result = get_executable_dir()
                    
                    # Assert
                    mock_path.assert_called_with('/path/to/executable')
                    assert result == mock_parent


class TestLoadEnvironmentConfig:
    """Test cases for load_environment_config function."""

    def test_LoadEnvironmentConfig_WithSpecificEnvName_LoadsCorrectFile(self, clean_environment):
        """Test loading specific environment configuration."""
        # Arrange
        with patch('rag.config.get_executable_dir') as mock_get_dir:
            mock_get_dir.return_value = Path('/test')
            with patch('rag.config.load_dotenv') as mock_load_dotenv:
                with patch.object(Path, 'exists', return_value=True):
                    
                    # Act
                    from rag.config import load_environment_config
                    load_environment_config('production')
                    
                    # Assert
                    mock_load_dotenv.assert_called_once()
                    call_args = mock_load_dotenv.call_args[0]
                    assert 'production.env' in str(call_args[0])

    def test_LoadEnvironmentConfig_WithRagEnvVariable_LoadsEnvSpecificFile(self, clean_environment):
        """Test loading configuration based on RAG_ENV variable."""
        # Arrange
        os.environ['RAG_ENV'] = 'docker'
        with patch('rag.config.get_executable_dir') as mock_get_dir:
            mock_get_dir.return_value = Path('/test')
            with patch('rag.config.load_dotenv') as mock_load_dotenv:
                with patch.object(Path, 'exists', return_value=True):
                    
                    # Act
                    from rag.config import load_environment_config
                    load_environment_config()
                    
                    # Assert
                    mock_load_dotenv.assert_called_once()
                    call_args = mock_load_dotenv.call_args[0]
                    assert 'docker.env' in str(call_args[0])

    def test_LoadEnvironmentConfig_NoEnvFileExists_CallsLoadDotenvWithOverrideFalse(self, clean_environment):
        """Test that load_dotenv is called with override=False."""
        # Arrange
        with patch('rag.config.get_executable_dir') as mock_get_dir:
            mock_get_dir.return_value = Path('/test')
            with patch('rag.config.load_dotenv') as mock_load_dotenv:
                with patch.object(Path, 'exists', return_value=True):
                    
                    # Act
                    from rag.config import load_environment_config
                    load_environment_config('test')
                    
                    # Assert
                    mock_load_dotenv.assert_called_once()
                    _, kwargs = mock_load_dotenv.call_args
                    assert kwargs['override'] is False


class TestValidateConfig:
    """Test cases for validate_config function."""

    def test_ValidateConfig_WithValidConfig_ReturnsTrue(self, mock_console):
        """Test validation of valid configuration."""
        # Arrange
        config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "SIMILARITY_TOP_K": 4
        }
        with patch.object(Path, 'mkdir'):
            
            # Act
            from rag.config import validate_config
            result = validate_config(config)
            
            # Assert
            assert result is True

    def test_ValidateConfig_WithInvalidUrl_ReturnsFalse(self, mock_console):
        """Test validation fails with invalid URL."""
        # Arrange
        config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "invalid-url",
            "SIMILARITY_TOP_K": 4
        }
        with patch.object(Path, 'mkdir'):
            
            # Act
            from rag.config import validate_config
            result = validate_config(config)
            
            # Assert
            assert result is False

    def test_ValidateConfig_WithInvalidSimilarityTopK_ReturnsFalse(self, mock_console):
        """Test validation fails with invalid SIMILARITY_TOP_K."""
        # Arrange
        config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "SIMILARITY_TOP_K": "invalid"
        }
        with patch.object(Path, 'mkdir'):
            
            # Act
            from rag.config import validate_config
            result = validate_config(config)
            
            # Assert
            assert result is False

    def test_ValidateConfig_WithDirectoryCreationFailure_ReturnsFalse(self, mock_console):
        """Test validation fails when directory creation fails."""
        # Arrange
        config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "SIMILARITY_TOP_K": 4
        }
        with patch.object(Path, 'mkdir', side_effect=PermissionError("Access denied")):
            
            # Act
            from rag.config import validate_config
            result = validate_config(config)
            
            # Assert
            assert result is False


class TestLoadConfig:
    """Test cases for load_config function."""

    def test_LoadConfig_WithDefaults_ReturnsExpectedStructure(self, clean_environment):
        """Test loading configuration with default values."""
        # Arrange
        with patch('rag.config.load_environment_config'):
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_get_dir.return_value = Path('/test')
                with patch('rag.config.validate_config', return_value=True):
                    
                    # Act
                    from rag.config import load_config
                    config = load_config()
                    
                    # Assert
                    assert "DOCS_DIR" in config
                    assert "INDEX_DIR" in config
                    assert "OLLAMA_BASE_URL" in config
                    assert config["OLLAMA_BASE_URL"] == "http://localhost:11434"
                    assert config["SIMILARITY_TOP_K"] == 4

    def test_LoadConfig_WithEnvironmentVariables_ReturnsOverriddenValues(self, clean_environment):
        """Test loading configuration with environment variable overrides."""
        # Arrange
        os.environ["SIMILARITY_TOP_K"] = "8"
        os.environ["OLLAMA_BASE_URL"] = "http://custom:11434"
        
        with patch('rag.config.load_environment_config'):
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_get_dir.return_value = Path('/test')
                with patch('rag.config.validate_config', return_value=True):
                    
                    # Act
                    from rag.config import load_config
                    config = load_config()
                    
                    # Assert
                    assert config["SIMILARITY_TOP_K"] == 8
                    assert config["OLLAMA_BASE_URL"] == "http://custom:11434"

    def test_LoadConfig_WithValidationFailure_RaisesValueError(self, clean_environment):
        """Test that load_config raises ValueError when validation fails."""
        # Arrange
        with patch('rag.config.load_environment_config'):
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_get_dir.return_value = Path('/test')
                with patch('rag.config.validate_config', return_value=False):
                    
                    # Act & Assert
                    from rag.config import load_config
                    with pytest.raises(ValueError, match="Configuration validation failed"):
                        load_config()

    def test_LoadConfig_WithSpecificEnvName_CallsLoadEnvironmentConfig(self, clean_environment):
        """Test that specific environment name is passed to load_environment_config."""
        # Arrange
        with patch('rag.config.load_environment_config') as mock_load_env:
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_get_dir.return_value = Path('/test')
                with patch('rag.config.validate_config', return_value=True):
                    with patch('rag.config.resolve_store', return_value=None):

                        # Act
                        from rag.config import load_config
                        load_config('production')

                        # Assert
                        mock_load_env.assert_called_once_with('production')

    def test_LoadConfig_WithStoreName_CallsLoadStoreConfig(self, clean_environment):
        """Test that store_name triggers store-based config loading."""
        # Arrange
        mock_store = Mock()
        mock_store.name = 'test_store'
        mock_store.docs_dir = '/test/docs'
        mock_store.chat_model = 'llama3.1'
        mock_store.description = 'Test store'

        with patch('rag.config.load_environment_config'):
            with patch('rag.config.resolve_store', return_value=mock_store):
                with patch('rag.config.get_store_index_dir', return_value=Path('/test/index')):
                    with patch('rag.config.get_global_config', return_value={}):
                        with patch('rag.config.validate_config', return_value=True):

                            # Act
                            from rag.config import load_config
                            config = load_config(store_name='test_store')

                            # Assert
                            assert config["DOCS_DIR"] == Path('/test/docs')
                            assert config["_store_name"] == 'test_store'

    def test_LoadConfig_WithNonExistentStore_RaisesValueError(self, clean_environment):
        """Test that load_config raises ValueError when store doesn't exist."""
        # Arrange
        with patch('rag.config.load_environment_config'):
            with patch('rag.config.resolve_store', return_value=None):

                # Act & Assert
                from rag.config import load_config
                with pytest.raises(ValueError, match="Store 'nonexistent' not found"):
                    load_config(store_name='nonexistent')


class TestGetConfigValue:
    """Test cases for get_config_value function."""

    def test_GetConfigValue_WithExistingKey_ReturnsValue(self, clean_environment):
        """Test getting an existing configuration value."""
        # Arrange
        with patch('rag.config.load_config') as mock_load_config:
            mock_config = {"TEST_KEY": "test_value"}
            mock_load_config.return_value = mock_config
            
            # Act
            from rag.config import get_config_value
            result = get_config_value("TEST_KEY")
            
            # Assert
            assert result == "test_value"

    def test_GetConfigValue_WithMissingKey_ReturnsDefault(self, clean_environment):
        """Test getting a missing configuration value returns default."""
        # Arrange
        with patch('rag.config.load_config') as mock_load_config:
            mock_config = {}
            mock_load_config.return_value = mock_config
            
            # Act
            from rag.config import get_config_value
            result = get_config_value("MISSING_KEY", "default_value")
            
            # Assert
            assert result == "default_value"

    def test_GetConfigValue_WithEnvName_PassesToLoadConfig(self, clean_environment):
        """Test that env_name is passed to load_config."""
        # Arrange
        with patch('rag.config.load_config') as mock_load_config:
            mock_config = {"TEST_KEY": "test_value"}
            mock_load_config.return_value = mock_config

            # Act
            from rag.config import get_config_value
            get_config_value("TEST_KEY", env_name="production")

            # Assert
            # load_config now takes (env_name, store_name) - store_name defaults to None
            mock_load_config.assert_called_once_with("production", None)

    def test_GetConfigValue_WithStoreName_PassesToLoadConfig(self, clean_environment):
        """Test that store_name is passed to load_config."""
        # Arrange
        with patch('rag.config.load_config') as mock_load_config:
            mock_config = {"TEST_KEY": "store_value"}
            mock_load_config.return_value = mock_config

            # Act
            from rag.config import get_config_value
            result = get_config_value("TEST_KEY", store_name="my_store")

            # Assert
            mock_load_config.assert_called_once_with(None, "my_store")
            assert result == "store_value"

    def test_GetConfigValue_WithBothEnvAndStoreName_PassesBothToLoadConfig(self, clean_environment):
        """Test that both env_name and store_name are passed to load_config."""
        # Arrange
        with patch('rag.config.load_config') as mock_load_config:
            mock_config = {"TEST_KEY": "combined_value"}
            mock_load_config.return_value = mock_config

            # Act
            from rag.config import get_config_value
            result = get_config_value("TEST_KEY", env_name="prod", store_name="my_store")

            # Assert
            mock_load_config.assert_called_once_with("prod", "my_store")
            assert result == "combined_value"


class TestResolvePath:
    """Test cases for path resolution functionality."""

    def test_LoadConfig_ResolvesRelativePaths_Correctly(self, clean_environment):
        """Test that relative paths are resolved correctly."""
        # Arrange
        os.environ["DOCS_DIR"] = "./test_docs"
        os.environ["INDEX_DIR"] = "./test_index"
        
        with patch('rag.config.load_environment_config'):
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_executable_dir = Path('/project_root')
                mock_get_dir.return_value = mock_executable_dir
                with patch('rag.config.validate_config', return_value=True):
                    
                    # Act
                    from rag.config import load_config
                    config = load_config()
                    
                    # Assert
                    expected_docs = (mock_executable_dir / "test_docs").resolve()
                    expected_index = (mock_executable_dir / "test_index").resolve()
                    assert config["DOCS_DIR"] == expected_docs
                    assert config["INDEX_DIR"] == expected_index

    def test_LoadConfig_KeepsAbsolutePaths_Unchanged(self, clean_environment):
        """Test that absolute paths are kept unchanged."""
        # Arrange - use platform-appropriate absolute paths
        import sys
        if sys.platform == 'win32':
            abs_docs = "C:\\absolute\\docs"
            abs_index = "C:\\absolute\\index"
        else:
            abs_docs = "/absolute/docs"
            abs_index = "/absolute/index"

        os.environ["DOCS_DIR"] = abs_docs
        os.environ["INDEX_DIR"] = abs_index

        with patch('rag.config.load_environment_config'):
            with patch('rag.config.get_executable_dir') as mock_get_dir:
                mock_get_dir.return_value = Path('/project_root')
                with patch('rag.config.validate_config', return_value=True):
                    with patch('rag.config.resolve_store', return_value=None):

                        # Act
                        from rag.config import load_config
                        config = load_config()

                        # Assert - paths should remain absolute (not relative to project_root)
                        assert config["DOCS_DIR"] == Path(abs_docs)
                        assert config["INDEX_DIR"] == Path(abs_index)