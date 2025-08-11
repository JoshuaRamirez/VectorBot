"""Unit tests for the version module."""

import pytest


class TestVersion:
    """Test cases for version module functionality."""

    def test_Version_ImportVersion_ReturnsStringValue(self):
        """Test that version can be imported and is a string."""
        # Arrange & Act
        from rag.version import __version__
        
        # Assert
        assert isinstance(__version__, str)

    def test_Version_ImportVersion_ReturnsNonEmptyString(self):
        """Test that version string is not empty."""
        # Arrange & Act
        from rag.version import __version__
        
        # Assert
        assert len(__version__) > 0

    def test_Version_ImportVersion_ReturnsValidSemanticVersion(self):
        """Test that version follows semantic versioning pattern."""
        # Arrange & Act
        from rag.version import __version__
        
        # Assert
        version_parts = __version__.split(".")
        assert len(version_parts) >= 2  # At least major.minor
        for part in version_parts:
            # Each part should be numeric (ignoring pre-release suffixes)
            numeric_part = part.split("-")[0].split("+")[0]
            assert numeric_part.isdigit()

    def test_Version_ImportVersion_MatchesExpectedValue(self):
        """Test that version matches expected value from project."""
        # Arrange & Act
        from rag.version import __version__
        
        # Assert
        assert __version__ == "1.0.0"

    def test_Version_ModuleDocstring_ExistsAndIsString(self):
        """Test that module has a docstring."""
        # Arrange & Act
        import rag.version as version_module
        
        # Assert
        assert hasattr(version_module, "__doc__")
        assert isinstance(version_module.__doc__, str)
        assert len(version_module.__doc__) > 0