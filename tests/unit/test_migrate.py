"""Unit tests for the migrate module.

Tests migration functionality from legacy index_storage to store-based system.
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


class TestDetectLegacyIndex:
    """Tests for detect_legacy_index function."""

    def test_DetectLegacyIndex_NoDirectory_ReturnsNone(self, tmp_path: Path) -> None:
        """Return None when no index_storage directory exists."""
        from rag.migrate import detect_legacy_index

        result = detect_legacy_index(tmp_path)

        assert result is None

    def test_DetectLegacyIndex_EmptyDirectory_ReturnsNone(self, tmp_path: Path) -> None:
        """Return None when index_storage exists but is empty (no docstore.json)."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()

        result = detect_legacy_index(tmp_path)

        assert result is None

    def test_DetectLegacyIndex_NoDocstore_ReturnsNone(self, tmp_path: Path) -> None:
        """Return None when index_storage exists but has no docstore.json."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "other_file.txt").write_text("some content")

        result = detect_legacy_index(tmp_path)

        assert result is None

    def test_DetectLegacyIndex_WithDocstore_ReturnsInfo(self, tmp_path: Path) -> None:
        """Return info dict when valid legacy index exists with docstore.json."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["index_dir"] == index_dir
        assert result["has_docstore"] is True
        assert result["file_count"] == 1
        assert result["docs_dir"] is None

    def test_DetectLegacyIndex_MultipleFiles_CountsCorrectly(
        self, tmp_path: Path
    ) -> None:
        """Correctly count multiple files in index_storage."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        (index_dir / "index.faiss").write_bytes(b"\x00\x01\x02")
        (index_dir / "metadata.json").write_text("{}")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["file_count"] == 3

    def test_DetectLegacyIndex_WithEnvDocsDir_ReturnsDocsDir(
        self, tmp_path: Path
    ) -> None:
        """Read DOCS_DIR from .env file when present."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "my_documents"
        docs_dir.mkdir()

        env_file = tmp_path / ".env"
        env_file.write_text(f"DOCS_DIR={docs_dir}")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["docs_dir"] == docs_dir

    def test_DetectLegacyIndex_EnvRelativePath_ResolvesAgainstProjectDir(
        self, tmp_path: Path
    ) -> None:
        """Resolve relative DOCS_DIR paths against project directory."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "relative_docs"
        docs_dir.mkdir()

        env_file = tmp_path / ".env"
        env_file.write_text("DOCS_DIR=relative_docs")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["docs_dir"] == docs_dir.resolve()

    def test_DetectLegacyIndex_NoEnvFile_DocsDirIsNone(self, tmp_path: Path) -> None:
        """Return None for docs_dir when no .env file exists."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["docs_dir"] is None

    def test_DetectLegacyIndex_EnvWithoutDocsDir_DocsDirIsNone(
        self, tmp_path: Path
    ) -> None:
        """Return None for docs_dir when .env exists but has no DOCS_DIR."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        env_file = tmp_path / ".env"
        env_file.write_text("OTHER_VAR=value\nANOTHER=123")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        assert result["docs_dir"] is None

    def test_DetectLegacyIndex_RelativeProjectDir_ResolvesToAbsolute(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Resolve relative project_dir to absolute path."""
        from rag.migrate import detect_legacy_index

        # Change to tmp_path so relative path works
        monkeypatch.chdir(tmp_path)

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        # Use relative path "."
        result = detect_legacy_index(Path("."))

        assert result is not None
        # index_dir should be absolute
        assert result["index_dir"].is_absolute()

    def test_DetectLegacyIndex_NoneProjectDir_UsesCwd(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Use current working directory when project_dir is None."""
        from rag.migrate import detect_legacy_index

        monkeypatch.chdir(tmp_path)

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        result = detect_legacy_index(None)

        assert result is not None
        assert result["index_dir"] == index_dir

    def test_DetectLegacyIndex_FileInsteadOfDir_ReturnsNone(
        self, tmp_path: Path
    ) -> None:
        """Return None when index_storage is a file instead of directory."""
        from rag.migrate import detect_legacy_index

        index_file = tmp_path / "index_storage"
        index_file.write_text("not a directory")

        result = detect_legacy_index(tmp_path)

        assert result is None

    def test_DetectLegacyIndex_DocstoreIsDir_ReturnsNone(self, tmp_path: Path) -> None:
        """Return None when docstore.json is a directory instead of file."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        docstore_dir = index_dir / "docstore.json"
        docstore_dir.mkdir()

        result = detect_legacy_index(tmp_path)

        assert result is None

    def test_DetectLegacyIndex_WithSubdirectories_OnlyCountsFiles(
        self, tmp_path: Path
    ) -> None:
        """Only count files, not subdirectories, in file_count."""
        from rag.migrate import detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        (index_dir / "subdir").mkdir()
        (index_dir / "subdir" / "nested.txt").write_text("nested")

        result = detect_legacy_index(tmp_path)

        assert result is not None
        # Should only count docstore.json, not the subdir
        assert result["file_count"] == 1


class TestMigrateLegacyIndex:
    """Tests for migrate_legacy_index function."""

    def test_MigrateLegacyIndex_NoLegacyIndex_RaisesValueError(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when no legacy index exists."""
        from rag.migrate import migrate_legacy_index

        with pytest.raises(ValueError, match="No legacy index found"):
            migrate_legacy_index("new-store", tmp_path)

    def test_MigrateLegacyIndex_StoreExists_RaisesValueError(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when store name already exists."""
        from rag.migrate import migrate_legacy_index

        # Create legacy index
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        with patch("rag.migrate.get_store") as mock_get_store:
            mock_get_store.return_value = {"name": "existing-store"}

            with pytest.raises(ValueError, match="already exists"):
                migrate_legacy_index("existing-store", tmp_path)

    def test_MigrateLegacyIndex_NoDocsDir_RaisesFileNotFoundError(
        self, tmp_path: Path
    ) -> None:
        """Raise FileNotFoundError when docs_dir cannot be determined."""
        from rag.migrate import migrate_legacy_index

        # Create legacy index without .env
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        with patch("rag.migrate.get_store") as mock_get_store:
            mock_get_store.return_value = None

            with pytest.raises(FileNotFoundError, match="Could not determine"):
                migrate_legacy_index("new-store", tmp_path, docs_dir=None)

    def test_MigrateLegacyIndex_Success_CreatesStore(self, tmp_path: Path) -> None:
        """Successfully create store during migration."""
        from rag.migrate import migrate_legacy_index

        # Create legacy index
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        mock_store_config = {"name": "new-store", "docs_dir": str(docs_dir)}

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ) as mock_set_default, patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = mock_store_config
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = mock_store_config

            result = migrate_legacy_index("new-store", tmp_path, docs_dir=docs_dir)

            mock_create_store.assert_called_once_with("new-store", [docs_dir])
            mock_set_default.assert_called_once_with("new-store")
            assert result == mock_store_config

    def test_MigrateLegacyIndex_CopiesFiles(self, tmp_path: Path) -> None:
        """Copy all files from legacy index to new store index."""
        from rag.migrate import migrate_legacy_index

        # Create legacy index with multiple files
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text('{"docs": []}')
        (index_dir / "index.faiss").write_bytes(b"\x00\x01\x02\x03")
        (index_dir / "metadata.json").write_text('{"version": 1}')

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_store_index"
        new_index_dir.mkdir()

        mock_store_config = {"name": "test-store", "docs_dir": str(docs_dir)}

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = mock_store_config
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = mock_store_config

            migrate_legacy_index("test-store", tmp_path, docs_dir=docs_dir)

            # Verify files were copied
            assert (new_index_dir / "docstore.json").exists()
            assert (new_index_dir / "index.faiss").exists()
            assert (new_index_dir / "metadata.json").exists()

            # Verify content is correct
            assert (new_index_dir / "docstore.json").read_text() == '{"docs": []}'
            assert (new_index_dir / "index.faiss").read_bytes() == b"\x00\x01\x02\x03"

    def test_MigrateLegacyIndex_CopiesSubdirectories(self, tmp_path: Path) -> None:
        """Copy subdirectories from legacy index to new store."""
        from rag.migrate import migrate_legacy_index

        # Create legacy index with subdirectory
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        subdir = index_dir / "embeddings"
        subdir.mkdir()
        (subdir / "vectors.bin").write_bytes(b"\xff\xfe")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_store_index"
        new_index_dir.mkdir()

        mock_store_config = {"name": "test-store"}

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = mock_store_config
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = mock_store_config

            migrate_legacy_index("test-store", tmp_path, docs_dir=docs_dir)

            # Verify subdirectory was copied
            assert (new_index_dir / "embeddings").exists()
            assert (new_index_dir / "embeddings").is_dir()
            assert (new_index_dir / "embeddings" / "vectors.bin").exists()
            assert (
                new_index_dir / "embeddings" / "vectors.bin"
            ).read_bytes() == b"\xff\xfe"

    def test_MigrateLegacyIndex_SetsAsDefaultStore(self, tmp_path: Path) -> None:
        """Set migrated store as default."""
        from rag.migrate import migrate_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ) as mock_set_default, patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "migrated-store"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "migrated-store"}

            migrate_legacy_index("migrated-store", tmp_path, docs_dir=docs_dir)

            mock_set_default.assert_called_once_with("migrated-store")

    def test_MigrateLegacyIndex_UpdatesStoreWithMigrationInfo(
        self, tmp_path: Path
    ) -> None:
        """Update store config with migration metadata."""
        from rag.migrate import migrate_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        (index_dir / "extra.txt").write_text("extra")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        mock_datetime = datetime(2024, 6, 15, 10, 30, 0)

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store, patch(
            "rag.migrate.datetime"
        ) as mock_dt:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "test-store"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "test-store"}
            mock_dt.now.return_value = mock_datetime

            migrate_legacy_index("test-store", tmp_path, docs_dir=docs_dir)

            mock_update_store.assert_called_once()
            call_kwargs = mock_update_store.call_args[1]
            assert call_kwargs["migrated_from"] == str(index_dir)
            assert call_kwargs["migrated_at"] == mock_datetime.isoformat()
            assert call_kwargs["chunk_count"] == 2  # docstore.json + extra.txt

    def test_MigrateLegacyIndex_ReadsDocsDirFromEnv(self, tmp_path: Path) -> None:
        """Use docs_dir from .env when not explicitly provided."""
        from rag.migrate import migrate_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "env_docs"
        docs_dir.mkdir()

        env_file = tmp_path / ".env"
        env_file.write_text(f"DOCS_DIR={docs_dir}")

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "test-store"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "test-store"}

            migrate_legacy_index("test-store", tmp_path, docs_dir=None)

            # Verify create_store was called with docs_dir from .env
            mock_create_store.assert_called_once()
            call_args = mock_create_store.call_args[0]
            assert call_args[1] == [docs_dir]

    def test_MigrateLegacyIndex_ExplicitDocsDirOverridesEnv(
        self, tmp_path: Path
    ) -> None:
        """Explicit docs_dir parameter overrides .env value."""
        from rag.migrate import migrate_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        env_docs = tmp_path / "env_docs"
        env_docs.mkdir()
        explicit_docs = tmp_path / "explicit_docs"
        explicit_docs.mkdir()

        env_file = tmp_path / ".env"
        env_file.write_text(f"DOCS_DIR={env_docs}")

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "test-store"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "test-store"}

            migrate_legacy_index("test-store", tmp_path, docs_dir=explicit_docs)

            mock_create_store.assert_called_once()
            call_args = mock_create_store.call_args[0]
            assert call_args[1] == [explicit_docs]

    def test_MigrateLegacyIndex_RelativeDocsDir_ResolvesToAbsolute(
        self, tmp_path: Path
    ) -> None:
        """Resolve relative docs_dir to absolute path."""
        from rag.migrate import migrate_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        new_index_dir = tmp_path / "new_index"
        new_index_dir.mkdir()

        # Use relative path
        relative_docs = Path("docs")

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "test-store"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "test-store"}

            migrate_legacy_index("test-store", tmp_path, docs_dir=relative_docs)

            mock_create_store.assert_called_once()
            call_args = mock_create_store.call_args[0]
            # Should be resolved to absolute
            assert call_args[1][0].is_absolute()


class TestCleanupLegacyIndex:
    """Tests for cleanup_legacy_index function."""

    def test_CleanupLegacyIndex_NoLegacyIndex_RaisesValueError(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when no legacy index exists."""
        from rag.migrate import cleanup_legacy_index

        with pytest.raises(ValueError, match="No legacy index found"):
            cleanup_legacy_index(tmp_path)

    def test_CleanupLegacyIndex_BackupTrue_RenamesDirectory(
        self, tmp_path: Path
    ) -> None:
        """Rename directory to backup when backup=True."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        (index_dir / "data.txt").write_text("important data")

        mock_datetime = datetime(2024, 6, 15, 14, 30, 45)

        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = mock_datetime
            mock_dt.strftime = datetime.strftime

            result = cleanup_legacy_index(tmp_path, backup=True)

        expected_backup = tmp_path / "index_storage.bak.20240615_143045"
        assert result == expected_backup
        assert expected_backup.exists()
        assert not index_dir.exists()
        # Verify content was preserved
        assert (expected_backup / "docstore.json").exists()
        assert (expected_backup / "data.txt").read_text() == "important data"

    def test_CleanupLegacyIndex_BackupFalse_DeletesDirectory(
        self, tmp_path: Path
    ) -> None:
        """Delete directory completely when backup=False."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        (index_dir / "data.txt").write_text("data to delete")

        result = cleanup_legacy_index(tmp_path, backup=False)

        assert result is None
        assert not index_dir.exists()
        # Verify no backup was created
        backup_dirs = list(tmp_path.glob("index_storage.bak.*"))
        assert len(backup_dirs) == 0

    def test_CleanupLegacyIndex_BackupDefault_UsesBackupTrue(
        self, tmp_path: Path
    ) -> None:
        """Default behavior should be backup=True."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
            mock_dt.strftime = datetime.strftime

            result = cleanup_legacy_index(tmp_path)

        # Should return backup path (backup=True is default)
        assert result is not None
        assert result.exists()
        assert not index_dir.exists()

    def test_CleanupLegacyIndex_BackupTimestampFormat(self, tmp_path: Path) -> None:
        """Verify backup timestamp format is YYYYMMDD_HHMMSS."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 12, 31, 23, 59, 59)
            mock_dt.strftime = datetime.strftime

            result = cleanup_legacy_index(tmp_path, backup=True)

        assert result is not None
        assert result.name == "index_storage.bak.20241231_235959"

    def test_CleanupLegacyIndex_PreservesDirectoryContents(
        self, tmp_path: Path
    ) -> None:
        """Verify all files and subdirectories are preserved in backup."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text('{"docs": [1,2,3]}')
        (index_dir / "index.bin").write_bytes(b"\x00\x01\x02\x03")
        subdir = index_dir / "nested"
        subdir.mkdir()
        (subdir / "deep.txt").write_text("nested content")

        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 6, 1, 0, 0, 0)
            mock_dt.strftime = datetime.strftime

            result = cleanup_legacy_index(tmp_path, backup=True)

        assert result is not None
        assert (result / "docstore.json").read_text() == '{"docs": [1,2,3]}'
        assert (result / "index.bin").read_bytes() == b"\x00\x01\x02\x03"
        assert (result / "nested" / "deep.txt").read_text() == "nested content"

    def test_CleanupLegacyIndex_NoneProjectDir_UsesCwd(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Use current working directory when project_dir is None."""
        from rag.migrate import cleanup_legacy_index

        monkeypatch.chdir(tmp_path)

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 1, 1, 0, 0, 0)
            mock_dt.strftime = datetime.strftime

            result = cleanup_legacy_index(None, backup=True)

        assert result is not None
        assert not index_dir.exists()

    def test_CleanupLegacyIndex_DeleteRecursively(self, tmp_path: Path) -> None:
        """Delete should remove nested directories."""
        from rag.migrate import cleanup_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")
        deep = index_dir / "a" / "b" / "c"
        deep.mkdir(parents=True)
        (deep / "deep_file.txt").write_text("deep")

        cleanup_legacy_index(tmp_path, backup=False)

        assert not index_dir.exists()
        assert not (tmp_path / "a").exists()


class TestMigrateModuleConstants:
    """Tests for module-level constants."""

    def test_LegacyIndexDir_HasCorrectValue(self) -> None:
        """Verify LEGACY_INDEX_DIR constant."""
        from rag.migrate import LEGACY_INDEX_DIR

        assert LEGACY_INDEX_DIR == "index_storage"

    def test_LegacyDocstoreFile_HasCorrectValue(self) -> None:
        """Verify LEGACY_DOCSTORE_FILE constant."""
        from rag.migrate import LEGACY_DOCSTORE_FILE

        assert LEGACY_DOCSTORE_FILE == "docstore.json"

    def test_LegacyEnvDocsKey_HasCorrectValue(self) -> None:
        """Verify LEGACY_ENV_DOCS_KEY constant."""
        from rag.migrate import LEGACY_ENV_DOCS_KEY

        assert LEGACY_ENV_DOCS_KEY == "DOCS_DIR"


class TestMigrateIntegration:
    """Integration-style tests for migrate module workflows."""

    def test_FullMigrationWorkflow_DetectMigrateCleanup(self, tmp_path: Path) -> None:
        """Test complete workflow: detect -> migrate -> cleanup."""
        from rag.migrate import (
            cleanup_legacy_index,
            detect_legacy_index,
            migrate_legacy_index,
        )

        # Setup legacy index
        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text('{"documents": []}')
        (index_dir / "vectors.faiss").write_bytes(b"\x00" * 100)

        docs_dir = tmp_path / "documents"
        docs_dir.mkdir()

        env_file = tmp_path / ".env"
        env_file.write_text(f"DOCS_DIR={docs_dir}")

        # Step 1: Detect
        legacy_info = detect_legacy_index(tmp_path)
        assert legacy_info is not None
        assert legacy_info["has_docstore"] is True
        assert legacy_info["docs_dir"] == docs_dir
        assert legacy_info["file_count"] == 2

        # Step 2: Migrate (with mocks for store functions)
        new_index_dir = tmp_path / "new_store_index"
        new_index_dir.mkdir()

        with patch("rag.migrate.get_store") as mock_get_store, patch(
            "rag.migrate.create_store"
        ) as mock_create_store, patch(
            "rag.migrate.get_store_index_dir"
        ) as mock_get_index_dir, patch(
            "rag.migrate.set_default_store"
        ), patch(
            "rag.store.update_store"
        ) as mock_update_store:
            mock_get_store.return_value = None
            mock_create_store.return_value = {"name": "my-docs"}
            mock_get_index_dir.return_value = new_index_dir
            mock_update_store.return_value = {"name": "my-docs"}

            migrate_legacy_index("my-docs", tmp_path)

        # Verify files were copied
        assert (new_index_dir / "docstore.json").exists()
        assert (new_index_dir / "vectors.faiss").exists()

        # Step 3: Cleanup
        with patch("rag.migrate.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2024, 6, 15, 12, 0, 0)
            mock_dt.strftime = datetime.strftime

            backup_path = cleanup_legacy_index(tmp_path, backup=True)

        # Original should be gone, backup should exist
        assert not index_dir.exists()
        assert backup_path is not None
        assert backup_path.exists()
        assert (backup_path / "docstore.json").exists()

    def test_DetectAfterCleanup_ReturnsNone(self, tmp_path: Path) -> None:
        """After cleanup, detect should return None."""
        from rag.migrate import cleanup_legacy_index, detect_legacy_index

        index_dir = tmp_path / "index_storage"
        index_dir.mkdir()
        (index_dir / "docstore.json").write_text("{}")

        # Verify detected before cleanup
        assert detect_legacy_index(tmp_path) is not None

        # Cleanup
        cleanup_legacy_index(tmp_path, backup=False)

        # Should no longer detect
        assert detect_legacy_index(tmp_path) is None
