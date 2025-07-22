"""Tests for autodoc settings in configuration."""

from jsoncrack_for_sphinx.config import JsonCrackConfig


class TestAutodocSettings:
    """Test autodoc configuration settings."""

    def test_default_autodoc_settings(self):
        """Test default autodoc settings."""
        config = JsonCrackConfig()
        assert config.disable_autodoc is False
        assert config.autodoc_ignore == []

    def test_custom_autodoc_settings(self):
        """Test custom autodoc settings."""
        config = JsonCrackConfig(
            disable_autodoc=True, autodoc_ignore=["mymodule.test", "examples."]
        )
        assert config.disable_autodoc is True
        assert config.autodoc_ignore == ["mymodule.test", "examples."]

    def test_autodoc_ignore_empty_list(self):
        """Test that empty list is handled correctly."""
        config = JsonCrackConfig(autodoc_ignore=[])
        assert config.autodoc_ignore == []

    def test_autodoc_ignore_with_none(self):
        """Test that None is converted to empty list."""
        config = JsonCrackConfig(autodoc_ignore=None)
        assert config.autodoc_ignore == []

    def test_repr_includes_autodoc_settings(self):
        """Test that repr includes autodoc settings."""
        config = JsonCrackConfig(disable_autodoc=True, autodoc_ignore=["test"])
        repr_str = repr(config)
        assert "disable_autodoc=True" in repr_str
        assert "autodoc_ignore=['test']" in repr_str
