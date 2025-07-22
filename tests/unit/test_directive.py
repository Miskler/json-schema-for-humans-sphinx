"""
Tests for schema directive.
"""

from unittest.mock import Mock

from jsoncrack_for_sphinx.core.directive import SchemaDirective


class TestSchemaDirective:
    """Test the schema directive."""

    def test_schema_directive_creation(self, mock_sphinx_app):
        """Test creating a schema directive."""
        # Create mock environment
        mock_env = Mock()
        mock_env.config = Mock()
        mock_env.config.json_schema_dir = "/test/schemas"

        # Create mock state with env
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = mock_env

        directive = SchemaDirective(
            name="schema",
            arguments=["User.create"],
            options={"title": "Test Schema"},
            content=[],
            lineno=1,
            content_offset=0,
            block_text="",
            state=mock_state,
            state_machine=Mock(),
        )

        assert directive.arguments == ["User.create"]
        assert directive.options == {"title": "Test Schema"}
        assert directive.env.config.json_schema_dir == "/test/schemas"

    def test_find_schema_file_found(self, schema_dir):
        """Test finding an existing schema file."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()

        directive = SchemaDirective(
            name="schema",
            arguments=["User.create"],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text="",
            state=mock_state,
            state_machine=Mock(),
        )

        result = directive._find_schema_file("User.create", str(schema_dir))

        assert result is not None
        assert result.name == "User.create.schema.json"

    def test_find_schema_file_not_found(self, schema_dir):
        """Test finding a non-existent schema file."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()

        directive = SchemaDirective(
            name="schema",
            arguments=["NonExistent.method"],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text="",
            state=mock_state,
            state_machine=Mock(),
        )

        result = directive._find_schema_file("NonExistent.method", str(schema_dir))
        assert result is None

    def test_find_schema_file_no_schema_dir(self):
        """Test finding schema file when no schema directory is configured."""
        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = Mock()

        directive = SchemaDirective(
            name="schema",
            arguments=["User.create"],
            options={},
            content=[],
            lineno=1,
            content_offset=0,
            block_text="",
            state=mock_state,
            state_machine=Mock(),
        )

        result = directive._find_schema_file("User.create", None)
        assert result is None

    def test_generate_schema_html_with_options(self, schema_dir):
        """Test generating schema HTML with directive options."""
        mock_env = Mock()
        mock_config = Mock()
        mock_config.jsoncrack_default_options = {}
        mock_env.config = mock_config

        mock_state = Mock()
        mock_state.document = Mock()
        mock_state.document.settings = Mock()
        mock_state.document.settings.env = mock_env

        directive = SchemaDirective(
            name="schema",
            arguments=["User.create"],
            options={
                "title": "Custom Title",
                "description": "Custom description",
                "render_mode": "onload",
                "direction": "LEFT",
                "height": "600",
            },
            content=[],
            lineno=1,
            content_offset=0,
            block_text="",
            state=mock_state,
            state_machine=Mock(),
        )

        schema_path = schema_dir / "User.create.schema.json"
        html_content = directive._generate_schema_html(schema_path)

        assert "Custom Title" in html_content
        assert "Custom description" in html_content
        assert "jsoncrack-container" in html_content
        assert 'data-render-mode="onload"' in html_content
        assert 'data-direction="LEFT"' in html_content
        assert 'data-height="600"' in html_content
