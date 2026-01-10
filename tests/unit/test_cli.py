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

    def test_Doctor_WithStores_ShowsStoresWithDefaultMarker(self, mock_console: Any) -> None:
        """Test that doctor lists stores with * marker for default store."""
        # Arrange
        argv = ["doctor"]

        mock_stores = [
            {"name": "store1"},
            {"name": "store2"},
            {"name": "default-store"},
        ]

        with patch('rag.cli.run_doctor') as mock_doctor:
            with patch('rag.cli.list_stores', return_value=mock_stores):
                with patch('rag.cli.get_default_store', return_value="default-store"):
                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_doctor.assert_called_once_with(verbose=False)
                    # Check that stores are printed with the default marker
                    mock_console.print.assert_any_call("  - store1")
                    mock_console.print.assert_any_call("  - store2")
                    mock_console.print.assert_any_call("  - default-store *")

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
                    mock_create.assert_called_once_with("my-store", [Path("/path/to/docs")])

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

    def test_StoreNew_WithoutDocsArg_PromptsAndSucceeds(self, mock_console: Any) -> None:
        """Test that store new prompts for docs path when not provided."""
        # Arrange
        argv = ["store", "new", "my-store"]

        with patch('rag.cli.create_store') as mock_create:
            with patch('rag.cli.list_stores', return_value=[{"name": "my-store"}]):
                with patch('rag.cli.set_default_store'):
                    with patch('rag.cli.console') as mock_cli_console:
                        # Mock input to return a path
                        mock_cli_console.input.return_value = "/path/to/docs"
                        mock_cli_console.print = mock_console.print

                        # Act
                        from rag.cli import main
                        result = main(argv)

                        # Assert
                        assert result == 0
                        mock_create.assert_called_once_with("my-store", [Path("/path/to/docs")])

    def test_StoreNew_WithEmptyDocsInput_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store new returns 1 when user inputs empty docs path."""
        # Arrange
        argv = ["store", "new", "my-store"]

        with patch('rag.cli.console') as mock_cli_console:
            # Mock input to return empty string
            mock_cli_console.input.return_value = ""
            mock_cli_console.print = mock_console.print

            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1
            mock_cli_console.print.assert_any_call("[red]Error: Documents path is required.[/red]")

    def test_StoreDelete_WithoutForce_UserConfirms_Deletes(self, mock_console: Any) -> None:
        """Test that store delete prompts and deletes when user confirms."""
        # Arrange
        argv = ["store", "delete", "my-store"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.delete_store') as mock_delete:
                with patch('rag.cli.console') as mock_cli_console:
                    # Mock input to return 'y' for confirmation
                    mock_cli_console.input.return_value = 'y'
                    mock_cli_console.print = mock_console.print

                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_delete.assert_called_once_with("my-store")

    def test_StoreDelete_WithoutForce_UserCancels_NoDelete(self, mock_console: Any) -> None:
        """Test that store delete cancels when user declines confirmation."""
        # Arrange
        argv = ["store", "delete", "my-store"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.delete_store') as mock_delete:
                with patch('rag.cli.console') as mock_cli_console:
                    # Mock input to return 'n' for cancellation
                    mock_cli_console.input.return_value = 'n'
                    mock_cli_console.print = mock_console.print

                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 0
                    mock_delete.assert_not_called()
                    mock_cli_console.print.assert_any_call("[dim]Cancelled.[/dim]")

    def test_StoreReindex_ExplicitNonexistentStore_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store reindex returns 1 when explicit store doesn't exist."""
        # Arrange
        argv = ["store", "reindex", "nonexistent-store"]

        with patch('rag.cli.get_store', return_value=None):
            # Act
            from rag.cli import main
            result = main(argv)

            # Assert
            assert result == 1
            mock_console.print.assert_any_call("[red]Error: Store 'nonexistent-store' not found.[/red]")

    def test_StoreList_WithInvalidDatetime_HandlesGracefully(self, mock_console: Any) -> None:
        """Test that store list handles invalid last_indexed datetime gracefully."""
        # Arrange
        argv = ["store", "list"]

        # Store with invalid datetime that cannot be parsed by datetime.fromisoformat
        mock_stores = [
            {
                "name": "store-with-bad-date",
                "docs_dir": "/docs",
                "last_indexed": "not-a-valid-datetime",  # This will cause ValueError
                "chunk_count": 50,
            },
            {
                "name": "store-with-none-date",
                "docs_dir": "/docs2",
                "last_indexed": None,  # This could cause TypeError if passed to fromisoformat
                "chunk_count": 100,
            },
        ]

        with patch('rag.cli.list_stores', return_value=mock_stores):
            with patch('rag.cli.get_default_store', return_value="store-with-bad-date"):
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                # Should return 0 and not raise exception
                assert result == 0

    def test_StoreDelete_DeleteRaisesValueError_ReturnsOne(self, mock_console: Any) -> None:
        """Test that store delete returns 1 when delete_store raises ValueError."""
        # Arrange
        argv = ["store", "delete", "my-store", "--force"]

        with patch('rag.cli.get_store', return_value={"name": "my-store"}):
            with patch('rag.cli.delete_store', side_effect=ValueError("Cannot delete: store is in use")):
                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 1
                mock_console.print.assert_any_call("[red]Error: Cannot delete: store is in use[/red]")


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

    def test_Migrate_WithoutName_PromptsAndSucceeds(self, mock_console: Any) -> None:
        """Test that migrate without --name prompts for store name and succeeds."""
        # Arrange
        argv = ["migrate", "--docs", "/docs"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,
            "file_count": 10,
        }

        store_config = {
            "name": "my-store",
            "docs_dir": "/docs",
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.migrate_legacy_index', return_value=store_config):
                with patch('rag.cli.get_store_index_dir', return_value=Path("/new/index")):
                    with patch('rag.cli.cleanup_legacy_index'):
                        with patch('rag.cli.console') as mock_cli_console:
                            # First input for store name, second for cleanup prompt
                            mock_cli_console.input.side_effect = ['my-store', 'n']
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0
                            # Verify input was called for store name
                            assert mock_cli_console.input.call_count == 2

    def test_Migrate_CleanupPromptAccepted_CleansUp(self, mock_console: Any) -> None:
        """Test that migrate cleans up legacy index when user confirms."""
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
                    with patch('rag.cli.cleanup_legacy_index', return_value=Path("/backup/path")) as mock_cleanup:
                        with patch('rag.cli.console') as mock_cli_console:
                            # User accepts cleanup prompt
                            mock_cli_console.input.return_value = 'y'
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0
                            mock_cleanup.assert_called_once_with(backup=True)

    def test_Migrate_CleanupPromptDeclined_LeavesInPlace(self, mock_console: Any) -> None:
        """Test that migrate leaves legacy index in place when user declines."""
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
                    with patch('rag.cli.cleanup_legacy_index') as mock_cleanup:
                        with patch('rag.cli.console') as mock_cli_console:
                            # User declines cleanup prompt
                            mock_cli_console.input.return_value = 'n'
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0
                            mock_cleanup.assert_not_called()
                            # Verify "left in place" message was printed
                            mock_cli_console.print.assert_any_call("[dim]Legacy index_storage/ left in place.[/dim]")

    def test_Migrate_MigrationRaisesFileNotFoundError_ReturnsOne(self, mock_console: Any) -> None:
        """Test that migrate returns 1 when migrate_legacy_index raises FileNotFoundError."""
        # Arrange
        argv = ["migrate", "--name", "migrated-store", "--docs", "/docs"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,
            "file_count": 10,
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.migrate_legacy_index', side_effect=FileNotFoundError("Legacy index not found")):
                with patch('rag.cli.console') as mock_cli_console:
                    mock_cli_console.print = mock_console.print

                    # Act
                    from rag.cli import main
                    result = main(argv)

                    # Assert
                    assert result == 1
                    mock_cli_console.print.assert_any_call("[red]Error: Legacy index not found[/red]")

    def test_Migrate_CleanupRaisesValueError_ShowsWarning(self, mock_console: Any) -> None:
        """Test that migrate shows warning when cleanup_legacy_index raises ValueError."""
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
                    with patch('rag.cli.cleanup_legacy_index', side_effect=ValueError("Cleanup failed")):
                        with patch('rag.cli.console') as mock_cli_console:
                            # User accepts cleanup prompt
                            mock_cli_console.input.return_value = 'y'
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0  # Should still return 0
                            mock_cli_console.print.assert_any_call("[yellow]Warning: Could not clean up: Cleanup failed[/yellow]")

    def test_Migrate_WithEmptyNameInput_ReturnsOne(self, mock_console: Any) -> None:
        """Test that migrate returns 1 when user inputs empty store name."""
        # Arrange
        argv = ["migrate", "--docs", "/docs"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,
            "file_count": 10,
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.console') as mock_cli_console:
                # User inputs empty string for store name
                mock_cli_console.input.return_value = ""
                mock_cli_console.print = mock_console.print

                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 1
                mock_cli_console.print.assert_any_call("[red]Error: Store name is required.[/red]")

    def test_Migrate_WithoutDocsAndLegacyHasNone_PromptsAndSucceeds(self, mock_console: Any) -> None:
        """Test that migrate prompts for docs directory when legacy has none and --docs not provided."""
        # Arrange
        argv = ["migrate", "--name", "migrated-store"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,  # No docs_dir in legacy
            "file_count": 10,
        }

        store_config = {
            "name": "migrated-store",
            "docs_dir": "/user/provided/docs",
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.migrate_legacy_index', return_value=store_config) as mock_migrate:
                with patch('rag.cli.get_store_index_dir', return_value=Path("/new/index")):
                    with patch('rag.cli.cleanup_legacy_index'):
                        with patch('rag.cli.console') as mock_cli_console:
                            # First input for docs path, second for cleanup prompt
                            mock_cli_console.input.side_effect = ['/user/provided/docs', 'n']
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0
                            # Verify docs_dir was passed to migrate
                            call_kwargs = mock_migrate.call_args[1]
                            assert call_kwargs['docs_dir'] == Path('/user/provided/docs')

    def test_Migrate_WithEmptyDocsInput_ReturnsOne(self, mock_console: Any) -> None:
        """Test that migrate returns 1 when user inputs empty docs directory."""
        # Arrange
        argv = ["migrate", "--name", "migrated-store"]

        legacy_info = {
            "index_dir": Path("/legacy/index"),
            "docs_dir": None,  # No docs_dir in legacy
            "file_count": 10,
        }

        with patch('rag.cli.detect_legacy_index', return_value=legacy_info):
            with patch('rag.cli.console') as mock_cli_console:
                # User inputs empty string for docs path
                mock_cli_console.input.return_value = ""
                mock_cli_console.print = mock_console.print

                # Act
                from rag.cli import main
                result = main(argv)

                # Assert
                assert result == 1
                mock_cli_console.print.assert_any_call("[red]Error: Documents directory is required.[/red]")

    def test_Migrate_WithNoBackup_DeletesLegacyIndex(self, mock_console: Any) -> None:
        """Test that migrate with --no-backup calls cleanup with backup=False."""
        # Arrange
        argv = ["migrate", "--name", "migrated-store", "--docs", "/docs", "--no-backup"]

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
                    with patch('rag.cli.cleanup_legacy_index', return_value=None) as mock_cleanup:
                        with patch('rag.cli.console') as mock_cli_console:
                            # User confirms deletion (requires 'y' with --no-backup)
                            mock_cli_console.input.return_value = 'y'
                            mock_cli_console.print = mock_console.print

                            # Act
                            from rag.cli import main
                            result = main(argv)

                            # Assert
                            assert result == 0
                            # Verify cleanup was called with backup=False
                            mock_cleanup.assert_called_once_with(backup=False)
                            # Verify the deletion message was printed (since backup_path is None)
                            mock_cli_console.print.assert_any_call("[green]Legacy index deleted.[/green]")
