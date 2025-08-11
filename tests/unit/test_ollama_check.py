"""Unit tests for the ollama_check module."""

import json
import subprocess
from unittest.mock import Mock, patch
import requests


class TestCheckServer:
    """Test cases for check_server function."""

    def test_CheckServer_WithSuccessfulResponse_ReturnsTrue(self):
        """Test server check returns True for successful response."""
        # Arrange
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Act
            from rag.ollama_check import check_server
            result = check_server("http://localhost:11434")
            
            # Assert
            assert result is True
            mock_get.assert_called_once_with("http://localhost:11434/api/tags", timeout=3)

    def test_CheckServer_WithConnectionError_ReturnsFalse(self):
        """Test server check returns False for connection error."""
        # Arrange
        with patch('requests.get', side_effect=requests.ConnectionError()):
            
            # Act
            from rag.ollama_check import check_server
            result = check_server("http://localhost:11434")
            
            # Assert
            assert result is False

    def test_CheckServer_WithTimeout_ReturnsFalse(self):
        """Test server check returns False for timeout."""
        # Arrange
        with patch('requests.get', side_effect=requests.Timeout()):
            
            # Act
            from rag.ollama_check import check_server
            result = check_server("http://localhost:11434")
            
            # Assert
            assert result is False

    def test_CheckServer_WithNon200Status_ReturnsFalse(self):
        """Test server check returns False for non-200 status code."""
        # Arrange
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_get.return_value = mock_response
            
            # Act
            from rag.ollama_check import check_server
            result = check_server("http://localhost:11434")
            
            # Assert
            assert result is False

    def test_CheckServer_WithCustomBaseUrl_UsesCorrectUrl(self):
        """Test server check uses custom base URL correctly."""
        # Arrange
        custom_url = "http://custom-host:8080"
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response
            
            # Act
            from rag.ollama_check import check_server
            check_server(custom_url)
            
            # Assert
            mock_get.assert_called_once_with(f"{custom_url}/api/tags", timeout=3)


class TestListLocalModels:
    """Test cases for list_local_models function."""

    def test_ListLocalModels_WithSuccessfulApiCall_ReturnsModelList(self):
        """Test listing models via API returns correct model list."""
        # Arrange
        models_data = {
            "models": [
                {"name": "llama3.1:latest"},
                {"name": "nomic-embed-text:latest"}
            ]
        }
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = models_data
            mock_get.return_value = mock_response
            
            # Act
            from rag.ollama_check import list_local_models
            result = list_local_models()
            
            # Assert
            expected = ["llama3.1:latest", "nomic-embed-text:latest"]
            assert result == expected

    def test_ListLocalModels_WithApiFailure_FallsBackToCli(self):
        """Test that API failure triggers CLI fallback."""
        # Arrange
        cli_output = "NAME\t\t\tID\t\t\tSIZE\tMODIFIED\nllama3:latest\t\tabc123\t\t7GB\t2 days ago\n"
        
        with patch('requests.get', side_effect=requests.ConnectionError()):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = cli_output
                mock_run.return_value = mock_result
                
                # Act
                from rag.ollama_check import list_local_models
                result = list_local_models()
                
                # Assert
                assert result == ["llama3"]
                mock_run.assert_called_once()

    def test_ListLocalModels_WithEmptyApiResponse_ReturnsEmptyList(self):
        """Test that empty API response returns empty list."""
        # Arrange
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"models": []}
            mock_get.return_value = mock_response
            
            # Act
            from rag.ollama_check import list_local_models
            result = list_local_models()
            
            # Assert
            assert result == []

    def test_ListLocalModels_WithJsonDecodeError_FallsBackToCli(self):
        """Test that JSON decode error triggers CLI fallback."""
        # Arrange
        cli_output = "NAME\t\t\tID\t\t\tSIZE\tMODIFIED\nmistral:latest\t\tdef456\t\t4GB\t1 day ago\n"
        
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("error", "doc", 0)
            mock_get.return_value = mock_response
            
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = cli_output
                mock_run.return_value = mock_result
                
                # Act
                from rag.ollama_check import list_local_models
                result = list_local_models()
                
                # Assert
                assert result == ["mistral"]

    def test_ListLocalModels_WithCliTimeout_ReturnsEmptyList(self):
        """Test that CLI timeout returns empty list."""
        # Arrange
        with patch('requests.get', side_effect=requests.ConnectionError()):
            with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("ollama", 5)):
                
                # Act
                from rag.ollama_check import list_local_models
                result = list_local_models()
                
                # Assert
                assert result == []

    def test_ListLocalModels_WithCliFileNotFound_ReturnsEmptyList(self):
        """Test that CLI not found returns empty list."""
        # Arrange
        with patch('requests.get', side_effect=requests.ConnectionError()):
            with patch('subprocess.run', side_effect=FileNotFoundError()):
                
                # Act
                from rag.ollama_check import list_local_models
                result = list_local_models()
                
                # Assert
                assert result == []

    def test_ListLocalModels_RemovesTagSuffixes_Correctly(self):
        """Test that tag suffixes are removed from model names."""
        # Arrange
        cli_output = "NAME\t\t\tID\t\t\tSIZE\tMODIFIED\nllama3.1:8b\t\tabc123\t\t5GB\t1 day ago\ngemma:2b\t\tdef456\t\t2GB\t3 days ago\n"
        
        with patch('requests.get', side_effect=requests.ConnectionError()):
            with patch('subprocess.run') as mock_run:
                mock_result = Mock()
                mock_result.returncode = 0
                mock_result.stdout = cli_output
                mock_run.return_value = mock_result
                
                # Act
                from rag.ollama_check import list_local_models
                result = list_local_models()
                
                # Assert
                assert result == ["llama3.1", "gemma"]


class TestChooseChatModel:
    """Test cases for choose_chat_model function."""

    def test_ChooseChatModel_WithEnvModelAvailable_ReturnsEnvModel(self):
        """Test that environment model is returned when available."""
        # Arrange
        env_model = "custom-model"
        available = ["llama3", "custom-model", "mistral"]
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model(env_model, available)
        
        # Assert
        assert result == "custom-model"

    def test_ChooseChatModel_WithEnvModelUnavailable_ReturnsPreferredModel(self):
        """Test that preferred model is returned when env model unavailable."""
        # Arrange
        env_model = "unavailable-model"
        available = ["mistral", "qwen", "gemma"]
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model(env_model, available)
        
        # Assert
        assert result == "mistral"

    def test_ChooseChatModel_WithNoEnvModel_ReturnsPreferredModel(self):
        """Test that preferred model is returned when no env model specified."""
        # Arrange
        available = ["some-model", "llama3.2", "other-model"]
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model(None, available)
        
        # Assert
        assert result == "llama3.2"

    def test_ChooseChatModel_WithEmptyAvailable_ReturnsNone(self):
        """Test that None is returned when no models available."""
        # Arrange
        available = []
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model("any-model", available)
        
        # Assert
        assert result is None

    def test_ChooseChatModel_WithNoPreferredModels_ReturnsFirstAvailable(self):
        """Test that first available model is returned when no preferred matches."""
        # Arrange
        available = ["unknown-model-1", "unknown-model-2"]
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model(None, available)
        
        # Assert
        assert result == "unknown-model-1"

    def test_ChooseChatModel_PreferenceOrder_FollowsExpectedPriority(self):
        """Test that model preference order is followed correctly."""
        # Arrange
        available = ["gemma", "mistral", "llama3.3"]
        
        # Act
        from rag.ollama_check import choose_chat_model
        result = choose_chat_model(None, available)
        
        # Assert
        # llama3.3 should be chosen over mistral and gemma
        assert result == "llama3.3"


class TestEnsureEmbedModel:
    """Test cases for ensure_embed_model function."""

    def test_EnsureEmbedModel_WithExactMatch_ReturnsTrue(self):
        """Test that exact model match returns True."""
        # Arrange
        model_name = "nomic-embed-text"
        
        with patch('rag.ollama_check.list_local_models') as mock_list:
            mock_list.return_value = ["llama3", "nomic-embed-text", "mistral"]
            
            # Act
            from rag.ollama_check import ensure_embed_model
            success, message = ensure_embed_model("http://localhost:11434", model_name)
            
            # Assert
            assert success is True
            assert "available" in message

    def test_EnsureEmbedModel_WithPartialMatch_ReturnsTrue(self):
        """Test that partial model match returns True."""
        # Arrange
        model_name = "nomic-embed"
        
        with patch('rag.ollama_check.list_local_models') as mock_list:
            mock_list.return_value = ["llama3", "nomic-embed-text:latest", "mistral"]
            
            # Act
            from rag.ollama_check import ensure_embed_model
            success, message = ensure_embed_model("http://localhost:11434", model_name)
            
            # Assert
            assert success is True
            assert "available" in message

    def test_EnsureEmbedModel_WithNoMatch_ReturnsFalse(self):
        """Test that no model match returns False."""
        # Arrange
        model_name = "missing-model"
        
        with patch('rag.ollama_check.list_local_models') as mock_list:
            mock_list.return_value = ["llama3", "mistral"]
            
            # Act
            from rag.ollama_check import ensure_embed_model
            success, message = ensure_embed_model("http://localhost:11434", model_name)
            
            # Assert
            assert success is False
            assert "not found" in message
            assert "ollama pull" in message

    def test_EnsureEmbedModel_CallsListLocalModels_WithCorrectBaseUrl(self):
        """Test that list_local_models is called with correct base URL."""
        # Arrange
        base_url = "http://custom:8080"
        model_name = "test-model"
        
        with patch('rag.ollama_check.list_local_models') as mock_list:
            mock_list.return_value = []
            
            # Act
            from rag.ollama_check import ensure_embed_model
            ensure_embed_model(base_url, model_name)
            
            # Assert
            mock_list.assert_called_once_with(base_url)


class TestDoctor:
    """Test cases for doctor function."""

    def test_Doctor_WithHealthyServer_CompletesSuccessfully(self, mock_console):
        """Test that doctor completes successfully with healthy server."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "nomic-embed-text"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=True):
                with patch('rag.ollama_check.list_local_models') as mock_list:
                    mock_list.return_value = ["llama3.1", "nomic-embed-text"]
                    with patch('rag.ollama_check.choose_chat_model') as mock_choose:
                        mock_choose.return_value = "llama3.1"
                        with patch('rag.ollama_check.ensure_embed_model') as mock_ensure:
                            mock_ensure.return_value = (True, "OK")
                            
                            # Act
                            from rag.ollama_check import doctor
                            doctor(verbose=False, env_name=None)
                            
                            # Assert
                            mock_load_config.assert_called_once_with(None)

    def test_Doctor_WithServerDown_ExitsWithError(self, mock_console):
        """Test that doctor exits when server is down."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "nomic-embed-text"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=False):
                with patch('sys.exit') as mock_exit:
                    
                    # Act
                    from rag.ollama_check import doctor
                    doctor()
                    
                    # Assert
                    mock_exit.assert_called_with(1)

    def test_Doctor_WithNoModels_ExitsWithError(self, mock_console):
        """Test that doctor exits when no models are installed."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "nomic-embed-text"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=True):
                with patch('rag.ollama_check.list_local_models', return_value=[]):
                    with patch('sys.exit') as mock_exit:
                        
                        # Act
                        from rag.ollama_check import doctor
                        doctor()
                        
                        # Assert
                        mock_exit.assert_called_with(1)

    def test_Doctor_WithNoChatModel_ExitsWithError(self, mock_console):
        """Test that doctor exits when no suitable chat model found."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "nomic-embed-text"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=True):
                with patch('rag.ollama_check.list_local_models') as mock_list:
                    mock_list.return_value = ["some-model"]
                    with patch('rag.ollama_check.choose_chat_model', return_value=None):
                        with patch('sys.exit') as mock_exit:
                            
                            # Act
                            from rag.ollama_check import doctor
                            doctor()
                            
                            # Assert
                            mock_exit.assert_called_with(1)

    def test_Doctor_WithSpecificEnvName_PassesToLoadConfig(self, mock_console):
        """Test that specific env name is passed to load_config."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": "llama3",
            "OLLAMA_EMBED_MODEL": "nomic-embed-text"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=True):
                with patch('rag.ollama_check.list_local_models') as mock_list:
                    mock_list.return_value = ["llama3", "nomic-embed-text"]
                    with patch('rag.ollama_check.choose_chat_model') as mock_choose:
                        mock_choose.return_value = "llama3"
                        with patch('rag.ollama_check.ensure_embed_model') as mock_ensure:
                            mock_ensure.return_value = (True, "OK")
                            
                            # Act
                            from rag.ollama_check import doctor
                            doctor(env_name="production")
                            
                            # Assert
                            mock_load_config.assert_called_once_with("production")

    def test_Doctor_WithMissingEmbedModel_ShowsWarning(self, mock_console):
        """Test that doctor shows warning for missing embed model."""
        # Arrange
        mock_config = {
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": None,
            "OLLAMA_EMBED_MODEL": "missing-embed-model"
        }
        
        with patch('rag.config.load_config') as mock_load_config:
            mock_load_config.return_value = mock_config
            with patch('rag.ollama_check.check_server', return_value=True):
                with patch('rag.ollama_check.list_local_models') as mock_list:
                    mock_list.return_value = ["llama3.1"]
                    with patch('rag.ollama_check.choose_chat_model') as mock_choose:
                        mock_choose.return_value = "llama3.1"
                        with patch('rag.ollama_check.ensure_embed_model') as mock_ensure:
                            mock_ensure.return_value = (False, "Model not found")
                            
                            # Act
                            from rag.ollama_check import doctor
                            doctor()
                            
                            # Assert
                            # Should show warning but not exit
                            mock_console.print.assert_called()