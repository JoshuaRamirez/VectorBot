"""Unit tests for the cli module."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import pytest


class TestMain:
    """Test cases for main function."""

    def test_Main_WithVersionFlag_ExitsWithZero(self, mock_console):
        """Test that --version flag exits with code 0."""
        # Arrange
        argv = ["--version"]
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        assert exc_info.value.code == 0

    def test_Main_WithHelpFlag_ExitsWithZero(self, mock_console):
        """Test that --help flag exits with code 0."""
        # Arrange
        argv = ["--help"]
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        assert exc_info.value.code == 0

    def test_Main_WithNoCommand_ReturnsOne(self, mock_console):
        """Test that no command returns exit code 1."""
        # Arrange
        argv = []
        
        # Act
        from rag.cli import main
        result = main(argv)
        
        # Assert
        assert result == 1

    def test_Main_WithConfigInfoFlag_ReturnsZero(self, mock_console):
        """Test that --config-info flag returns 0."""
        # Arrange
        argv = ["--config-info"]
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "http://localhost:11434"
        }
        
        with patch('rag.config.load_config', return_value=mock_config):
            with patch('rag.config.get_executable_dir', return_value=Path("/test")):
                with patch.object(Path, 'exists', return_value=True):
                    
                    # Act
                    from rag.cli import main
                    result = main(argv)
                    
                    # Assert
                    assert result == 0

    def test_Main_WithDoctorCommand_CallsDoctorFunction(self, mock_console):
        """Test that doctor command calls doctor function."""
        # Arrange
        argv = ["doctor"]
        
        with patch('rag.cli.doctor') as mock_doctor:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_doctor.assert_called_once_with(verbose=False, env_name=None)

    def test_Main_WithDoctorVerbose_CallsDoctorWithVerbose(self, mock_console):
        """Test that doctor --verbose calls doctor with verbose=True."""
        # Arrange
        argv = ["doctor", "--verbose"]
        
        with patch('rag.cli.doctor') as mock_doctor:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_doctor.assert_called_once_with(verbose=True, env_name=None)

    def test_Main_WithIngestCommand_CallsIngestFunction(self, mock_console):
        """Test that ingest command calls ingest function."""
        # Arrange
        argv = ["ingest"]
        
        with patch('rag.cli.ingest') as mock_ingest:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_ingest.assert_called_once_with(verbose=False, env_name=None)

    def test_Main_WithIngestVerbose_CallsIngestWithVerbose(self, mock_console):
        """Test that ingest --verbose calls ingest with verbose=True."""
        # Arrange
        argv = ["ingest", "--verbose"]
        
        with patch('rag.cli.ingest') as mock_ingest:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_ingest.assert_called_once_with(verbose=True, env_name=None)

    def test_Main_WithQueryCommand_CallsQueryFunction(self, mock_console):
        """Test that query command calls query function."""
        # Arrange
        argv = ["query", "What is AI?"]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_query.assert_called_once_with(
                question="What is AI?",
                similarity_top_k=None,
                show_sources=False,
                verbose=False,
                env_name=None
            )

    def test_Main_WithQueryAllOptions_CallsQueryWithAllOptions(self, mock_console):
        """Test that query with all options calls query with correct parameters."""
        # Arrange
        argv = ["query", "Test question", "--k", "5", "--show-sources", "--verbose"]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_query.assert_called_once_with(
                question="Test question",
                similarity_top_k=5,
                show_sources=True,
                verbose=True,
                env_name=None
            )

    def test_Main_WithEnvFlag_PassesToAllCommands(self, mock_console):
        """Test that --env flag is passed to all commands."""
        # Arrange
        env_name = "production"
        
        # Test doctor command
        with patch('rag.cli.doctor') as mock_doctor:
            from rag.cli import main
            main(["--env", env_name, "doctor"])
            mock_doctor.assert_called_once_with(verbose=False, env_name=env_name)
        
        # Test ingest command
        with patch('rag.cli.ingest') as mock_ingest:
            main(["--env", env_name, "ingest"])
            mock_ingest.assert_called_once_with(verbose=False, env_name=env_name)
        
        # Test query command
        with patch('rag.cli.query') as mock_query:
            main(["--env", env_name, "query", "test"])
            mock_query.assert_called_once_with(
                question="test",
                similarity_top_k=None,
                show_sources=False,
                verbose=False,
                env_name=env_name
            )

    def test_Main_WithKeyboardInterrupt_ReturnsInterruptCode(self, mock_console):
        """Test that KeyboardInterrupt returns code 130."""
        # Arrange
        argv = ["doctor"]
        
        with patch('rag.cli.doctor', side_effect=KeyboardInterrupt()):
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 130
            mock_console.print.assert_called_once_with("\n[yellow]Interrupted by user[/yellow]")

    def test_Main_WithGeneralException_ReturnsOne(self, mock_console):
        """Test that general exception returns code 1."""
        # Arrange
        argv = ["doctor"]
        error_message = "Something went wrong"
        
        with patch('rag.cli.doctor', side_effect=RuntimeError(error_message)):
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 1
            mock_console.print.assert_called_once_with(f"[red]Error: {error_message}[/red]")

    def test_Main_WithConfigInfoAndEnv_ShowsEnvironmentSpecificConfig(self, mock_console):
        """Test that config info with environment shows environment-specific config."""
        # Arrange
        argv = ["--config-info", "--env", "production"]
        mock_config = {
            "DOCS_DIR": Path("/prod/docs"),
            "INDEX_DIR": Path("/prod/index"),
            "LOG_LEVEL": "INFO"
        }
        
        with patch('rag.config.load_config', return_value=mock_config) as mock_load_config:
            with patch('rag.config.get_executable_dir', return_value=Path("/app")):
                with patch.object(Path, 'exists', return_value=True):
                    
                    # Act
                    from rag.cli import main
                    result = main(argv)
                    
                    # Assert
                    assert result == 0
                    mock_load_config.assert_called_once_with("production")

    def test_Main_WithConfigInfo_ShowsConfigurationDetails(self, mock_console):
        """Test that config info shows configuration details correctly."""
        # Arrange
        argv = ["--config-info"]
        mock_config = {
            "DOCS_DIR": Path("/test/docs"),
            "INDEX_DIR": Path("/test/index"),
            "OLLAMA_BASE_URL": "http://localhost:11434",
            "OLLAMA_CHAT_MODEL": "llama3.1",
            "OLLAMA_EMBED_MODEL": "nomic-embed-text",
            "SIMILARITY_TOP_K": 4,
            "LOG_LEVEL": "INFO",
            "ENABLE_VERBOSE_OUTPUT": False,
            "REQUEST_TIMEOUT": 60.0,
            "EMBED_BATCH_SIZE": 10
        }
        
        with patch('rag.config.load_config', return_value=mock_config):
            with patch('rag.config.get_executable_dir', return_value=Path("/app")):
                with patch.object(Path, 'exists', return_value=True):
                    # Act
                    from rag.cli import main
                    result = main(argv)
                    
                    # Assert
                    assert result == 0
                    # Verify that console.print was called to display configuration
                    mock_console.print.assert_called()
                    # Check that at least a few calls were made (configuration output)
                    assert mock_console.print.call_count >= 3

    def test_Main_WithNoneArgv_UsesSystemArgv(self, mock_console):
        """Test that None argv uses sys.argv."""
        # Arrange
        original_argv = sys.argv
        sys.argv = ["rag", "--version"]
        
        try:
            # Act & Assert
            from rag.cli import main
            with pytest.raises(SystemExit):
                main(None)
        finally:
            sys.argv = original_argv


class TestArgumentParsing:
    """Test cases for argument parsing functionality."""

    def test_Main_WithInvalidKValue_ShowsError(self, mock_console):
        """Test that invalid --k value shows appropriate error."""
        # Arrange
        argv = ["query", "test", "--k", "invalid"]
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        # ArgumentParser exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

    def test_Main_WithMissingQueryQuestion_ShowsError(self, mock_console):
        """Test that missing question for query command shows error."""
        # Arrange
        argv = ["query"]  # Missing required question argument
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        # ArgumentParser exits with code 2 for missing required arguments
        assert exc_info.value.code == 2

    def test_Main_WithValidIntegerK_ParsesCorrectly(self, mock_console):
        """Test that valid integer --k value is parsed correctly."""
        # Arrange
        argv = ["query", "test question", "--k", "10"]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            _, kwargs = mock_query.call_args
            assert kwargs['similarity_top_k'] == 10

    def test_Main_WithUnknownCommand_ShowsError(self, mock_console):
        """Test that unknown command shows error."""
        # Arrange
        argv = ["unknown-command"]
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        # ArgumentParser exits with code 2 for invalid subcommands
        assert exc_info.value.code == 2

    def test_Main_WithUnknownFlag_ShowsError(self, mock_console):
        """Test that unknown flag shows error."""
        # Arrange
        argv = ["--unknown-flag"]
        
        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)
        
        # ArgumentParser exits with code 2 for unknown arguments
        assert exc_info.value.code == 2


class TestSpecialCases:
    """Test cases for special edge cases and error conditions."""

    def test_Main_WithBothConfigInfoAndCommand_ConfigInfoTakesPrecedence(self, mock_console):
        """Test that config-info takes precedence over commands."""
        # Arrange
        argv = ["--config-info", "doctor"]
        mock_config = {"DOCS_DIR": Path("/test")}
        
        with patch('rag.config.load_config', return_value=mock_config):
            with patch('rag.config.get_executable_dir', return_value=Path("/test")):
                with patch('rag.cli.doctor') as mock_doctor:
                    with patch.object(Path, 'exists', return_value=True):
                        
                        # Act
                        from rag.cli import main
                        result = main(argv)
                        
                        # Assert
                        assert result == 0
                        # Doctor should not be called
                        mock_doctor.assert_not_called()

    def test_Main_WithEmptyStringArguments_HandlesGracefully(self, mock_console):
        """Test that empty string arguments are handled gracefully."""
        # Arrange
        argv = ["query", ""]  # Empty question string
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            mock_query.assert_called_once()
            call_args = mock_query.call_args
            assert call_args[1]['question'] == ""

    def test_Main_WithZeroKValue_PassesCorrectly(self, mock_console):
        """Test that zero --k value is passed correctly."""
        # Arrange
        argv = ["query", "test", "--k", "0"]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            _, kwargs = mock_query.call_args
            assert kwargs['similarity_top_k'] == 0

    def test_Main_WithNegativeKValue_PassesCorrectly(self, mock_console):
        """Test that negative --k value is passed correctly."""
        # Arrange
        argv = ["query", "test", "--k", "-1"]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            _, kwargs = mock_query.call_args
            assert kwargs['similarity_top_k'] == -1

    def test_Main_WithLongQuestion_HandlesCorrectly(self, mock_console):
        """Test that very long questions are handled correctly."""
        # Arrange
        long_question = "What is " + "very " * 1000 + "long question?"
        argv = ["query", long_question]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            _, kwargs = mock_query.call_args
            assert kwargs['question'] == long_question

    def test_Main_WithSpecialCharactersInQuestion_HandlesCorrectly(self, mock_console):
        """Test that special characters in questions are handled correctly."""
        # Arrange
        special_question = "What about symbols: !@#$%^&*()[]{}|\\:;\"'<>?,./"
        argv = ["query", special_question]
        
        with patch('rag.cli.query') as mock_query:
            
            # Act
            from rag.cli import main
            result = main(argv)
            
            # Assert
            assert result == 0
            _, kwargs = mock_query.call_args
            assert kwargs['question'] == special_question