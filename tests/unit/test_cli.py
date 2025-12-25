"""Unit tests for the cli module."""

import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Any
import pytest


class TestMain:
    """Test cases for main function."""

    def test_Main_WithVersionFlag_ExitsWithZero(self, mock_console: Any) -> None:
        """Test that --version flag exits with code 0."""
        # Arrange
        argv = ["--version"]

        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)

        assert exc_info.value.code == 0

    def test_Main_WithHelpFlag_ExitsWithZero(self, mock_console: Any) -> None:
        """Test that --help flag exits with code 0."""
        # Arrange
        argv = ["--help"]

        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)

        assert exc_info.value.code == 0

    def test_Main_WithNoCommand_ReturnsOne(self, mock_console: Any) -> None:
        """Test that no command returns exit code 1."""
        # Arrange
        argv: list[str] = []

        # Act
        from rag.cli import main
        result = main(argv)

        # Assert
        assert result == 1

    def test_Main_WithDoctorCommand_CallsDoctorFunction(self, mock_console: Any) -> None:
        """Test that doctor command calls doctor function and lists stores."""
        # Arrange
        argv = ["doctor"]

        with patch('rag.cli.run_doctor') as mock_doctor:
            with patch('rag.cli.list_stores', return_value=[]):
                with patch('rag.cli.get_default_store', return_value=None):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_doctor.assert_called_once_with(verbose=False)

    def test_Main_WithDoctorVerbose_CallsDoctorWithVerbose(self, mock_console: Any) -> None:
        """Test that doctor --verbose calls doctor with verbose=True."""
        # Arrange
        argv = ["doctor", "--verbose"]

        with patch('rag.cli.run_doctor') as mock_doctor:
            with patch('rag.cli.list_stores', return_value=[]):
                with patch('rag.cli.get_default_store', return_value=None):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_doctor.assert_called_once_with(verbose=True)

    def test_Main_WithIngestCommand_CallsIngestFunction(self, mock_console: Any) -> None:
        """Test that ingest command calls ingest function."""
        # Arrange
        argv = ["ingest"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.ingest', return_value={"chunk_count": 10}) as mock_ingest:
                with patch('rag.cli.update_store'):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_ingest.assert_called_once_with(
                        store_name="test-store",
                        verbose=False,
                        force=False,
                    )

    def test_Main_WithIngestVerbose_CallsIngestWithVerbose(self, mock_console: Any) -> None:
        """Test that ingest --verbose calls ingest with verbose=True."""
        # Arrange
        argv = ["ingest", "--verbose"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.ingest', return_value={"chunk_count": 10}) as mock_ingest:
                with patch('rag.cli.update_store'):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_ingest.assert_called_once_with(
                        store_name="test-store",
                        verbose=True,
                        force=False,
                    )

    def test_Main_WithQueryCommand_CallsQueryFunction(self, mock_console: Any) -> None:
        """Test that query command calls query function."""
        # Arrange
        argv = ["query", "What is AI?"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                mock_query.assert_called_once_with(
                    question="What is AI?",
                    store_name="test-store",
                    show_sources=False,
                    top_k=4,
                    verbose=False,
                )

    def test_Main_WithQueryAllOptions_CallsQueryWithAllOptions(self, mock_console: Any) -> None:
        """Test that query with all options calls query with correct parameters."""
        # Arrange
        argv = ["query", "Test question", "--k", "5", "--show-sources", "--verbose"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                mock_query.assert_called_once_with(
                    question="Test question",
                    store_name="test-store",
                    show_sources=True,
                    top_k=5,
                    verbose=True,
                )

    def test_Main_WithStoreFlag_PassesToCommands(self, mock_console: Any) -> None:
        """Test that -s/--store flag is passed to commands."""
        # Arrange
        store_name = "my-store"

        # Test ingest command with --store
        with patch('rag.cli.resolve_store', return_value=store_name) as mock_resolve:
            with patch('rag.cli.ingest', return_value={"chunk_count": 10}):
                with patch('rag.cli.update_store'):
                    from rag.cli import main
                    main(["--store", store_name, "ingest"])
                    mock_resolve.assert_called_once_with(store_name)

        # Test query command with -s
        with patch('rag.cli.resolve_store', return_value=store_name) as mock_resolve:
            with patch('rag.cli.query'):
                main(["-s", store_name, "query", "test"])
                mock_resolve.assert_called_once_with(store_name)

    def test_Main_WithKeyboardInterrupt_ReturnsInterruptCode(self, mock_console: Any) -> None:
        """Test that KeyboardInterrupt returns code 130."""
        # Arrange
        argv = ["doctor"]

        with patch('rag.cli.run_doctor', side_effect=KeyboardInterrupt()):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 130
            mock_console.print.assert_called_once_with("\n[yellow]Interrupted by user[/yellow]")

    def test_Main_WithGeneralException_ReturnsOne(self, mock_console: Any) -> None:
        """Test that general exception returns code 1."""
        # Arrange
        argv = ["doctor"]
        error_message = "Something went wrong"

        with patch('rag.cli.run_doctor', side_effect=RuntimeError(error_message)):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1
            mock_console.print.assert_called_once_with(f"[red]Error: {error_message}[/red]")

    def test_Main_WithNoneArgv_UsesSystemArgv(self, mock_console: Any) -> None:
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

    def test_Main_WithInvalidKValue_ShowsError(self, mock_console: Any) -> None:
        """Test that invalid --k value shows appropriate error."""
        # Arrange
        argv = ["query", "test", "--k", "invalid"]

        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)

        # ArgumentParser exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

    def test_Main_WithMissingQueryQuestion_ShowsError(self, mock_console: Any) -> None:
        """Test that missing question for query command shows error."""
        # Arrange
        argv = ["query"]  # Missing required question argument

        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)

        # ArgumentParser exits with code 2 for missing required arguments
        assert exc_info.value.code == 2

    def test_Main_WithValidIntegerK_ParsesCorrectly(self, mock_console: Any) -> None:
        """Test that valid integer --k value is parsed correctly."""
        # Arrange
        argv = ["query", "test question", "--k", "10"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                _, kwargs = mock_query.call_args
                assert kwargs['top_k'] == 10

    def test_Main_WithUnknownCommand_ShowsError(self, mock_console: Any) -> None:
        """Test that unknown command shows error."""
        # Arrange
        argv = ["unknown-command"]

        # Act & Assert
        from rag.cli import main
        with pytest.raises(SystemExit) as exc_info:
            main(argv)

        # ArgumentParser exits with code 2 for invalid subcommands
        assert exc_info.value.code == 2

    def test_Main_WithUnknownFlag_ShowsError(self, mock_console: Any) -> None:
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

    def test_Main_WithEmptyStringArguments_HandlesGracefully(self, mock_console: Any) -> None:
        """Test that empty string arguments are handled gracefully."""
        # Arrange
        argv = ["query", ""]  # Empty question string

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                mock_query.assert_called_once()
                call_args = mock_query.call_args
                assert call_args[1]['question'] == ""

    def test_Main_WithZeroKValue_PassesCorrectly(self, mock_console: Any) -> None:
        """Test that zero --k value is passed correctly."""
        # Arrange
        argv = ["query", "test", "--k", "0"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                _, kwargs = mock_query.call_args
                assert kwargs['top_k'] == 0

    def test_Main_WithNegativeKValue_PassesCorrectly(self, mock_console: Any) -> None:
        """Test that negative --k value is passed correctly."""
        # Arrange
        argv = ["query", "test", "--k", "-1"]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                _, kwargs = mock_query.call_args
                assert kwargs['top_k'] == -1

    def test_Main_WithLongQuestion_HandlesCorrectly(self, mock_console: Any) -> None:
        """Test that very long questions are handled correctly."""
        # Arrange
        long_question = "What is " + "very " * 1000 + "long question?"
        argv = ["query", long_question]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                _, kwargs = mock_query.call_args
                assert kwargs['question'] == long_question

    def test_Main_WithSpecialCharactersInQuestion_HandlesCorrectly(self, mock_console: Any) -> None:
        """Test that special characters in questions are handled correctly."""
        # Arrange
        special_question = "What about symbols: !@#$%^&*()[]{}|\\:;\"'<>?,./"
        argv = ["query", special_question]

        with patch('rag.cli.resolve_store', return_value="test-store"):
            with patch('rag.cli.query') as mock_query:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                _, kwargs = mock_query.call_args
                assert kwargs['question'] == special_question

    def test_Main_WithIngestStoreResolveError_ReturnsOne(self, mock_console: Any) -> None:
        """Test that ingest returns 1 when store resolution fails."""
        # Arrange
        argv = ["ingest"]

        with patch('rag.cli.resolve_store', side_effect=ValueError("No stores exist")):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_Main_WithQueryStoreResolveError_ReturnsOne(self, mock_console: Any) -> None:
        """Test that query returns 1 when store resolution fails."""
        # Arrange
        argv = ["query", "test"]

        with patch('rag.cli.resolve_store', side_effect=ValueError("Store 'foo' does not exist")):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1


class TestStoreCommands:
    """Test cases for store subcommands."""

    def test_StoreNew_WithDocsArg_CreatesStore(self, mock_console: Any) -> None:
        """Test that store new creates a store with docs argument."""
        # Arrange
        argv = ["store", "new", "my-store", "--docs", "/path/to/docs"]

        with patch('rag.cli.create_store') as mock_create:
            with patch('rag.cli.list_stores', return_value=[{"name": "my-store"}]):
                with patch('rag.cli.set_default_store'):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_create.assert_called_once_with("my-store", Path("/path/to/docs"))

    def test_StoreNew_WithExistingStore_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store new returns 1 when store already exists."""
        # Arrange
        argv = ["store", "new", "existing-store", "--docs", "/path"]

        with patch('rag.cli.create_store', side_effect=ValueError("Store 'existing-store' already exists.")):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_StoreList_ShowsTable(self, mock_console: Any) -> None:
        """Test that store list shows stores in a table."""
        # Arrange
        argv = ["store", "list"]

        mock_stores = [
            {"name": "store1", "docs_dir": "/docs1", "last_indexed": None, "chunk_count": 0},
            {"name": "store2", "docs_dir": "/docs2", "last_indexed": "2024-01-01T00:00:00", "chunk_count": 100},
        ]

        with patch('rag.cli.list_stores', return_value=mock_stores):
            with patch('rag.cli.get_default_store', return_value="store1"):
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0

    def test_StoreList_EmptyStores_ShowsMessage(self, mock_console: Any) -> None:
        """Test that store list with no stores shows appropriate message."""
        # Arrange
        argv = ["store", "list"]

        with patch('rag.cli.list_stores', return_value=[]):
            with patch('rag.cli.get_default_store', return_value=None):
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0

    def test_StoreInfo_ShowsStoreDetails(self, mock_console: Any) -> None:
        """Test that store info shows store details."""
        # Arrange
        argv = ["store", "info", "my-store"]

        mock_store = {
            "name": "my-store",
            "docs_dir": "/path/to/docs",
            "last_indexed": "2024-01-01T00:00:00",
            "chunk_count": 50,
        }

        with patch('rag.cli.get_store', return_value=mock_store):
            with patch('rag.cli.get_default_store', return_value="my-store"):
                with patch('rag.cli.get_store_index_dir', return_value=Path("/index")):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0

    def test_StoreInfo_NonExistentStore_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store info returns 1 for non-existent store."""
        # Arrange
        argv = ["store", "info", "nonexistent"]

        with patch('rag.cli.get_store', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_StoreDefault_SetsDefaultStore(self, mock_console: Any) -> None:
        """Test that store default sets the default store."""
        # Arrange
        argv = ["store", "default", "my-store"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.set_default_store') as mock_set:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                mock_set.assert_called_once_with("my-store")

    def test_StoreDefault_NonExistentStore_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store default returns 1 for non-existent store."""
        # Arrange
        argv = ["store", "default", "nonexistent"]

        with patch('rag.cli.get_store', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_StoreReindex_RebuildsIndex(self, mock_console: Any) -> None:
        """Test that store reindex rebuilds the index."""
        # Arrange
        argv = ["store", "reindex", "my-store"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.ingest', return_value={"chunk_count": 50}) as mock_ingest:
                with patch('rag.cli.update_store'):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_ingest.assert_called_once_with(
                        store_name="my-store",
                        verbose=True,
                        force=True,
                    )

    def test_StoreReindex_UsesDefaultIfNoName(self, mock_console: Any) -> None:
        """Test that store reindex uses default store when no name provided."""
        # Arrange
        argv = ["store", "reindex"]

        with patch('rag.cli.get_default_store', return_value="default-store"):
            with patch('rag.cli.get_store', return_value={"name": "default-store"}):
                with patch('rag.cli.ingest', return_value={"chunk_count": 50}) as mock_ingest:
                    with patch('rag.cli.update_store'):
                        # Act
                        from rag.cli import main
                        result = main(argv)

                        # Assert
                        assert result == 0
                        mock_ingest.assert_called_once_with(
                            store_name="default-store",
                            verbose=True,
                            force=True,
                        )

    def test_StoreReindex_NoDefaultNoName_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store reindex returns 1 when no name and no default."""
        # Arrange
        argv = ["store", "reindex"]

        with patch('rag.cli.get_default_store', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_StoreRename_RenamesStore(self, mock_console: Any) -> None:
        """Test that store rename renames a store."""
        # Arrange
        argv = ["store", "rename", "old-name", "new-name"]

        with patch('rag.cli.rename_store') as mock_rename:
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 0
            mock_rename.assert_called_once_with("old-name", "new-name")

    def test_StoreRename_Error_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store rename returns 1 on error."""
        # Arrange
        argv = ["store", "rename", "nonexistent", "new-name"]

        with patch('rag.cli.rename_store', side_effect=ValueError("Store 'nonexistent' does not exist.")):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_StoreDelete_WithForce_DeletesStore(self, mock_console: Any) -> None:
        """Test that store delete with --force deletes without confirmation."""
        # Arrange
        argv = ["store", "delete", "my-store", "--force"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.delete_store') as mock_delete:
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 0
                mock_delete.assert_called_once_with("my-store")

    def test_StoreDelete_NonExistentStore_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store delete returns 1 for non-existent store."""
        # Arrange
        argv = ["store", "delete", "nonexistent", "--force"]

        with patch('rag.cli.get_store', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1


class TestMigrateCommand:
    """Test cases for the migrate command."""

    def test_Migrate_NoLegacyIndex_ReturnsOne(self, mock_console: Any) -> None:
        """Test that migrate returns 1 when no legacy index exists."""
        # Arrange
        argv = ["migrate"]

        with patch('rag.cli.detect_legacy_index', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1

    def test_Migrate_WithName_MigratesSuccessfully(self, mock_console: Any) -> None:
        """Test that migrate with --name migrates successfully."""
        # Arrange
        argv = ["migrate", "--name", "migrated-store", "--docs", "/docs"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,
            "file_count": 10,
        }

        store_config = {
            "name": "migrated-store",
            "docs_dir": "/docs",
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.migrate_legacy_index', return_value=store_config):
                with patch('rag.cli.get_store_index_dir', return_value=Path("/new/index")):
                    with patch('rag.cli.cleanup_legacy_index'):
                        with patch.object(MagicMock(), 'input', return_value='n'):
                            # Need to mock console.input
                            with patch('rag.cli.console') as mock_cli_console:
                                mock_cli_console.input.return_value = 'n'
                                mock_cli_console.print = mock_console.print

                                # Act
                                from rag.cli import main
                                result = main(argv)

                                # Assert
                                assert result == 0
