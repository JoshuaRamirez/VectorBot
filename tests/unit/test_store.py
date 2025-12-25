"""Unit tests for the store management module."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import patch, MagicMock

import pytest

from rag.store import (
    get_stores_home,
    get_global_config,
    save_global_config,
    list_stores,
    get_store,
    create_store,
    update_store,
    delete_store,
    rename_store,
    get_store_index_dir,
    get_default_store,
    set_default_store,
    resolve_store,
    STORE_NAME_PATTERN,
)


@pytest.fixture
def mock_stores_home(tmp_path: Path) -> Any:
    """Mock get_stores_home to use temp directory."""
    with patch("rag.store.get_stores_home", return_value=tmp_path):
        yield tmp_path


@pytest.fixture
def mock_console() -> Any:
    """Mock the console for output suppression."""
    with patch("rag.store.console") as mock:
        yield mock


class TestGetStoresHome:
    """Test cases for get_stores_home function."""

    def test_GetStoresHome_WhenDirectoryNotExists_CreatesDirectory(
        self, tmp_path: Path
    ) -> None:
        """Test that get_stores_home creates the directory if it doesn't exist."""
        # Arrange
        test_home = tmp_path / ".vector-bot"

        with patch("rag.store.Path.home", return_value=tmp_path):
            # Act
            result = get_stores_home()

            # Assert
            assert result == test_home
            assert result.exists()
            assert result.is_dir()

    def test_GetStoresHome_WhenDirectoryExists_ReturnsExistingDirectory(
        self, tmp_path: Path
    ) -> None:
        """Test that get_stores_home returns existing directory."""
        # Arrange
        test_home = tmp_path / ".vector-bot"
        test_home.mkdir(parents=True, exist_ok=True)

        with patch("rag.store.Path.home", return_value=tmp_path):
            # Act
            result = get_stores_home()

            # Assert
            assert result == test_home
            assert result.exists()


class TestGlobalConfig:
    """Test cases for global config functions."""

    def test_GetGlobalConfig_WhenNoConfigExists_ReturnsDefaults(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_global_config returns defaults when no config file exists."""
        # Arrange - no config file created

        # Act
        config = get_global_config()

        # Assert
        assert config["default_store"] is None
        assert config["ollama_base_url"] == "http://localhost:11434"
        assert config["ollama_embed_model"] == "nomic-embed-text"

    def test_GetGlobalConfig_WhenConfigExists_ReturnsConfigValues(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_global_config reads existing config file."""
        # Arrange
        config_path = mock_stores_home / "config.json"
        existing_config = {
            "default_store": "my-store",
            "ollama_base_url": "http://custom:8080",
        }
        config_path.write_text(json.dumps(existing_config))

        # Act
        config = get_global_config()

        # Assert
        assert config["default_store"] == "my-store"
        assert config["ollama_base_url"] == "http://custom:8080"
        # Should merge with defaults for missing keys
        assert config["ollama_embed_model"] == "nomic-embed-text"

    def test_GetGlobalConfig_WhenConfigIsInvalid_ReturnsDefaults(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_global_config returns defaults when config is invalid JSON."""
        # Arrange
        config_path = mock_stores_home / "config.json"
        config_path.write_text("invalid json {{{")

        # Act
        config = get_global_config()

        # Assert
        assert config["default_store"] is None
        assert config["ollama_base_url"] == "http://localhost:11434"

    def test_SaveGlobalConfig_WritesConfigFile(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that save_global_config writes config to file."""
        # Arrange
        config = {
            "default_store": "test-store",
            "ollama_base_url": "http://localhost:11434",
        }

        # Act
        save_global_config(config)

        # Assert
        config_path = mock_stores_home / "config.json"
        assert config_path.exists()
        saved_config = json.loads(config_path.read_text())
        assert saved_config["default_store"] == "test-store"

    def test_SaveGlobalConfig_OverwritesExistingConfig(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that save_global_config overwrites existing config."""
        # Arrange
        config_path = mock_stores_home / "config.json"
        old_config = {"default_store": "old-store"}
        config_path.write_text(json.dumps(old_config))

        new_config = {"default_store": "new-store"}

        # Act
        save_global_config(new_config)

        # Assert
        saved_config = json.loads(config_path.read_text())
        assert saved_config["default_store"] == "new-store"


class TestListStores:
    """Test cases for list_stores function."""

    def test_ListStores_WhenNoStores_ReturnsEmptyList(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that list_stores returns empty list when no stores exist."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act
        stores = list_stores()

        # Assert
        assert stores == []

    def test_ListStores_WithOneStore_ReturnsOneStore(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that list_stores returns one store when one exists."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        store_dir = stores_dir / "my-store"
        store_dir.mkdir(parents=True, exist_ok=True)

        store_config = {
            "name": "my-store",
            "docs_dir": "/path/to/docs",
            "last_indexed": None,
            "chunk_count": 0,
        }
        (store_dir / "store.json").write_text(json.dumps(store_config))

        # Act
        stores = list_stores()

        # Assert
        assert len(stores) == 1
        assert stores[0]["name"] == "my-store"
        assert stores[0]["docs_dir"] == "/path/to/docs"

    def test_ListStores_WithMultipleStores_ReturnsAllStores(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that list_stores returns all stores when multiple exist."""
        # Arrange
        stores_dir = mock_stores_home / "stores"

        for store_name in ["store-a", "store-b", "store-c"]:
            store_dir = stores_dir / store_name
            store_dir.mkdir(parents=True, exist_ok=True)
            store_config = {
                "name": store_name,
                "docs_dir": f"/path/to/{store_name}",
                "last_indexed": None,
                "chunk_count": 0,
            }
            (store_dir / "store.json").write_text(json.dumps(store_config))

        # Act
        stores = list_stores()

        # Assert
        assert len(stores) == 3
        store_names = [s["name"] for s in stores]
        assert "store-a" in store_names
        assert "store-b" in store_names
        assert "store-c" in store_names

    def test_ListStores_SkipsDirectoriesWithoutStoreConfig(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that list_stores skips directories without store.json."""
        # Arrange
        stores_dir = mock_stores_home / "stores"

        # Valid store with config
        valid_store = stores_dir / "valid-store"
        valid_store.mkdir(parents=True, exist_ok=True)
        (valid_store / "store.json").write_text(json.dumps({"name": "valid-store"}))

        # Invalid directory without config
        invalid_store = stores_dir / "invalid-store"
        invalid_store.mkdir(parents=True, exist_ok=True)

        # Act
        stores = list_stores()

        # Assert
        assert len(stores) == 1
        assert stores[0]["name"] == "valid-store"

    def test_ListStores_SkipsInvalidJsonConfigs(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that list_stores skips stores with invalid JSON configs."""
        # Arrange
        stores_dir = mock_stores_home / "stores"

        # Valid store
        valid_store = stores_dir / "valid-store"
        valid_store.mkdir(parents=True, exist_ok=True)
        (valid_store / "store.json").write_text(json.dumps({"name": "valid-store"}))

        # Store with invalid JSON
        invalid_json_store = stores_dir / "invalid-json"
        invalid_json_store.mkdir(parents=True, exist_ok=True)
        (invalid_json_store / "store.json").write_text("not valid json {{{")

        # Act
        stores = list_stores()

        # Assert
        assert len(stores) == 1
        assert stores[0]["name"] == "valid-store"


class TestGetStore:
    """Test cases for get_store function."""

    def test_GetStore_WhenStoreExists_ReturnsStoreConfig(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store returns config when store exists."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        store_dir = stores_dir / "my-store"
        store_dir.mkdir(parents=True, exist_ok=True)

        store_config = {
            "name": "my-store",
            "docs_dir": "/path/to/docs",
            "created": "2024-01-01T00:00:00Z",
            "last_indexed": None,
            "chunk_count": 0,
        }
        (store_dir / "store.json").write_text(json.dumps(store_config))

        # Act
        result = get_store("my-store")

        # Assert
        assert result is not None
        assert result["name"] == "my-store"
        assert result["docs_dir"] == "/path/to/docs"

    def test_GetStore_WhenStoreNotExists_ReturnsNone(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store returns None when store doesn't exist."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act
        result = get_store("nonexistent-store")

        # Assert
        assert result is None

    def test_GetStore_WithInvalidName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store raises ValueError for invalid store names."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Invalid store name"):
            get_store("invalid name with spaces")

    def test_GetStore_WhenConfigIsInvalid_ReturnsNone(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store returns None for invalid JSON config."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        store_dir = stores_dir / "broken-store"
        store_dir.mkdir(parents=True, exist_ok=True)
        (store_dir / "store.json").write_text("invalid json")

        # Act
        result = get_store("broken-store")

        # Assert
        assert result is None


class TestCreateStore:
    """Test cases for create_store function."""

    def test_CreateStore_WithValidName_CreatesStoreDirectory(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that create_store creates store directory structure."""
        # Arrange
        docs_dir = Path("/path/to/docs")

        # Act
        result = create_store("new-store", docs_dir)

        # Assert
        store_dir = mock_stores_home / "stores" / "new-store"
        assert store_dir.exists()
        assert (store_dir / "index").exists()
        assert (store_dir / "store.json").exists()
        assert result["name"] == "new-store"

    def test_CreateStore_WithChatModel_IncludesInConfig(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that create_store includes chat_model in config."""
        # Arrange
        docs_dir = Path("/path/to/docs")

        # Act
        result = create_store("my-store", docs_dir, chat_model="llama3.1")

        # Assert
        assert result["chat_model"] == "llama3.1"

    def test_CreateStore_WithDuplicateName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that create_store raises ValueError for duplicate names."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("existing-store", docs_dir)

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            create_store("existing-store", docs_dir)

    @pytest.mark.parametrize(
        "invalid_name",
        [
            "",  # Empty name
            "a" * 51,  # Too long (max 50)
            "has spaces",  # Contains spaces
            "has/slash",  # Contains slash
            "has\\backslash",  # Contains backslash
            "has@symbol",  # Contains special character
            "has.dot",  # Contains dot
        ],
    )
    def test_CreateStore_WithInvalidName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any, invalid_name: str
    ) -> None:
        """Test that create_store raises ValueError for invalid names."""
        # Arrange
        docs_dir = Path("/path/to/docs")

        # Act & Assert
        with pytest.raises(ValueError):
            create_store(invalid_name, docs_dir)

    @pytest.mark.parametrize(
        "valid_name",
        [
            "store",
            "my-store",
            "my_store",
            "Store123",
            "a",
            "a" * 50,  # Maximum length
        ],
    )
    def test_CreateStore_WithValidName_Succeeds(
        self, mock_stores_home: Path, mock_console: Any, valid_name: str
    ) -> None:
        """Test that create_store accepts valid store names."""
        # Arrange
        docs_dir = Path("/path/to/docs")

        # Act
        result = create_store(valid_name, docs_dir)

        # Assert
        assert result["name"] == valid_name

    def test_CreateStore_WithRelativePath_ConvertsToAbsolute(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that create_store converts relative paths to absolute."""
        # Arrange
        relative_path = Path("./docs")

        # Act
        result = create_store("my-store", relative_path)

        # Assert
        # The docs_dir should be an absolute path
        assert Path(result["docs_dir"]).is_absolute()


class TestUpdateStore:
    """Test cases for update_store function."""

    def test_UpdateStore_WithExistingStore_UpdatesFields(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that update_store updates store fields."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)

        # Act
        result = update_store(
            "my-store",
            last_indexed="2024-01-01T00:00:00Z",
            chunk_count=100,
        )

        # Assert
        assert result["last_indexed"] == "2024-01-01T00:00:00Z"
        assert result["chunk_count"] == 100

    def test_UpdateStore_WithNonexistentStore_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that update_store raises ValueError for nonexistent store."""
        # Arrange - no store created

        # Act & Assert
        with pytest.raises(ValueError, match="does not exist"):
            update_store("nonexistent", last_indexed="2024-01-01T00:00:00Z")

    def test_UpdateStore_PreservesExistingFields(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that update_store preserves fields not being updated."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir, chat_model="llama3.1")

        # Act
        result = update_store("my-store", chunk_count=50)

        # Assert
        assert result["chat_model"] == "llama3.1"
        assert result["chunk_count"] == 50

    def test_UpdateStore_WithDocsDir_ConvertsToAbsolutePath(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that update_store converts docs_dir to absolute path."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)

        # Act
        result = update_store("my-store", docs_dir="./new/docs")

        # Assert
        assert Path(result["docs_dir"]).is_absolute()


class TestDeleteStore:
    """Test cases for delete_store function."""

    def test_DeleteStore_WhenStoreExists_DeletesStore(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that delete_store removes store directory."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)
        store_dir = mock_stores_home / "stores" / "my-store"
        assert store_dir.exists()

        # Act
        result = delete_store("my-store")

        # Assert
        assert result is True
        assert not store_dir.exists()

    def test_DeleteStore_WhenStoreNotExists_ReturnsFalse(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that delete_store returns False for nonexistent store."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act
        result = delete_store("nonexistent")

        # Assert
        assert result is False

    def test_DeleteStore_WhenIsDefaultStore_ClearsDefault(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that delete_store clears default when deleting default store."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)
        set_default_store("my-store")
        assert get_default_store() == "my-store"

        # Act
        delete_store("my-store")

        # Assert
        assert get_default_store() is None

    def test_DeleteStore_WithInvalidName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that delete_store raises ValueError for invalid names."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            delete_store("invalid name")


class TestRenameStore:
    """Test cases for rename_store function."""

    def test_RenameStore_WithValidNames_RenamesStore(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that rename_store renames the store directory."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("old-name", docs_dir)

        old_dir = mock_stores_home / "stores" / "old-name"
        assert old_dir.exists()

        # Act
        result = rename_store("old-name", "new-name")

        # Assert
        new_dir = mock_stores_home / "stores" / "new-name"
        assert not old_dir.exists()
        assert new_dir.exists()
        assert result["name"] == "new-name"

    def test_RenameStore_WhenOldNameNotExists_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that rename_store raises ValueError for nonexistent store."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act & Assert
        with pytest.raises(ValueError, match="does not exist"):
            rename_store("nonexistent", "new-name")

    def test_RenameStore_WhenNewNameExists_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that rename_store raises ValueError when new name already exists."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("store-a", docs_dir)
        create_store("store-b", docs_dir)

        # Act & Assert
        with pytest.raises(ValueError, match="already exists"):
            rename_store("store-a", "store-b")

    def test_RenameStore_WhenIsDefaultStore_UpdatesDefault(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that rename_store updates default store reference."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("old-name", docs_dir)
        set_default_store("old-name")
        assert get_default_store() == "old-name"

        # Act
        rename_store("old-name", "new-name")

        # Assert
        assert get_default_store() == "new-name"

    def test_RenameStore_WithInvalidNewName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that rename_store validates new name."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("valid-name", docs_dir)

        # Act & Assert
        with pytest.raises(ValueError):
            rename_store("valid-name", "invalid name with spaces")


class TestGetStoreIndexDir:
    """Test cases for get_store_index_dir function."""

    def test_GetStoreIndexDir_ReturnsCorrectPath(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store_index_dir returns correct path."""
        # Arrange & Act
        result = get_store_index_dir("my-store")

        # Assert
        expected = mock_stores_home / "stores" / "my-store" / "index"
        assert result == expected

    def test_GetStoreIndexDir_WithInvalidName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_store_index_dir validates store name."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError):
            get_store_index_dir("invalid name")


class TestGetDefaultStore:
    """Test cases for get_default_store function."""

    def test_GetDefaultStore_WhenDefaultSet_ReturnsStoreName(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_default_store returns store name when set."""
        # Arrange
        config = {"default_store": "my-store"}
        config_path = mock_stores_home / "config.json"
        config_path.write_text(json.dumps(config))

        # Act
        result = get_default_store()

        # Assert
        assert result == "my-store"

    def test_GetDefaultStore_WhenNoDefaultSet_ReturnsNone(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that get_default_store returns None when no default set."""
        # Arrange - no config file

        # Act
        result = get_default_store()

        # Assert
        assert result is None


class TestSetDefaultStore:
    """Test cases for set_default_store function."""

    def test_SetDefaultStore_WithExistingStore_SetsDefault(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that set_default_store sets the default store."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)

        # Act
        set_default_store("my-store")

        # Assert
        assert get_default_store() == "my-store"

    def test_SetDefaultStore_WithNonexistentStore_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that set_default_store raises ValueError for nonexistent store."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act & Assert
        with pytest.raises(ValueError, match="does not exist"):
            set_default_store("nonexistent")

    def test_SetDefaultStore_ChangesExistingDefault(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that set_default_store changes existing default."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("store-a", docs_dir)
        create_store("store-b", docs_dir)
        set_default_store("store-a")
        assert get_default_store() == "store-a"

        # Act
        set_default_store("store-b")

        # Assert
        assert get_default_store() == "store-b"


class TestResolveStore:
    """Test cases for resolve_store function."""

    def test_ResolveStore_WithExplicitName_ReturnsName(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store returns explicit name when provided."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)

        # Act
        result = resolve_store("my-store")

        # Assert
        assert result == "my-store"

    def test_ResolveStore_WithExplicitNonexistentName_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store raises ValueError for nonexistent explicit name."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act & Assert
        with pytest.raises(ValueError, match="does not exist"):
            resolve_store("nonexistent")

    def test_ResolveStore_WithNoNameAndDefaultSet_ReturnsDefault(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store returns default store when no name provided."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("default-store", docs_dir)
        set_default_store("default-store")

        # Act
        result = resolve_store(None)

        # Assert
        assert result == "default-store"

    def test_ResolveStore_WithNoNameAndSingleStore_ReturnsSingleStore(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store returns single store when only one exists."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("only-store", docs_dir)
        # No default set

        # Act
        result = resolve_store(None)

        # Assert
        assert result == "only-store"

    def test_ResolveStore_WithNoNameAndMultipleStores_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store raises ValueError with multiple stores and no default."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("store-a", docs_dir)
        create_store("store-b", docs_dir)
        # No default set

        # Act & Assert
        with pytest.raises(ValueError, match="Multiple stores exist"):
            resolve_store(None)

    def test_ResolveStore_WithNoNameAndNoStores_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store raises ValueError when no stores exist."""
        # Arrange
        stores_dir = mock_stores_home / "stores"
        stores_dir.mkdir(parents=True, exist_ok=True)

        # Act & Assert
        with pytest.raises(ValueError, match="No stores exist"):
            resolve_store(None)

    def test_ResolveStore_WithDefaultStoreDeleted_RaisesValueError(
        self, mock_stores_home: Path, mock_console: Any
    ) -> None:
        """Test that resolve_store raises ValueError when default store was deleted."""
        # Arrange
        docs_dir = Path("/path/to/docs")
        create_store("my-store", docs_dir)
        set_default_store("my-store")

        # Manually delete the store directory (simulating external deletion)
        import shutil
        store_dir = mock_stores_home / "stores" / "my-store"
        shutil.rmtree(store_dir)

        # Act & Assert
        with pytest.raises(ValueError, match="no longer exists"):
            resolve_store(None)


class TestStoreNamePattern:
    """Test cases for STORE_NAME_PATTERN regex."""

    @pytest.mark.parametrize(
        "valid_name",
        [
            "a",
            "store",
            "my-store",
            "my_store",
            "MyStore",
            "store123",
            "123store",
            "Store-With-Dashes",
            "Store_With_Underscores",
            "a1b2c3",
            "A" * 50,  # Maximum length
        ],
    )
    def test_StoreNamePattern_WithValidNames_Matches(self, valid_name: str) -> None:
        """Test that STORE_NAME_PATTERN matches valid names."""
        # Act & Assert
        assert STORE_NAME_PATTERN.match(valid_name) is not None

    @pytest.mark.parametrize(
        "invalid_name",
        [
            "",  # Empty
            "a" * 51,  # Too long
            "has spaces",
            "has.dot",
            "has/slash",
            "has\\backslash",
            "has@symbol",
            "has#hash",
            "has$dollar",
            "has%percent",
            "has&ampersand",
            "has*asterisk",
            "has(paren",
            "has)paren",
            "has+plus",
            "has=equals",
        ],
    )
    def test_StoreNamePattern_WithInvalidNames_DoesNotMatch(
        self, invalid_name: str
    ) -> None:
        """Test that STORE_NAME_PATTERN does not match invalid names."""
        # Act & Assert
        assert STORE_NAME_PATTERN.match(invalid_name) is None
