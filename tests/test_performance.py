"""
Performance and stress tests for the jsoncrack-for-sphinx extension.
"""

import json
import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from jsoncrack_for_sphinx.extension import (
    find_schema_for_object, generate_schema_html, 
    autodoc_process_signature, autodoc_process_docstring
)
from jsoncrack_for_sphinx.utils import (
    find_schema_files, get_schema_info, create_schema_index,
    validate_schema_file, schema_to_rst
)
from jsoncrack_for_sphinx.config import parse_config, get_config_values


class TestPerformance:
    """Performance tests for the extension."""
    
    def test_find_schema_for_object_performance(self, temp_dir):
        """Test performance of finding schema for object."""
        # Create many schema files
        num_files = 100
        for i in range(num_files):
            schema_data = {
                "type": "object",
                "title": f"Schema {i}",
                "properties": {
                    f"prop_{j}": {"type": "string"}
                    for j in range(10)
                }
            }
            
            with open(temp_dir / f"schema_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Test performance
        start_time = time.time()
        
        # Find existing schema
        result = find_schema_for_object('module.schema_50', str(temp_dir))
        
        # Find non-existing schema
        result_none = find_schema_for_object('module.non_existent', str(temp_dir))
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 1.0, "Schema finding should be fast"
        assert result is not None
        assert result_none is None
    
    def test_generate_schema_html_performance(self, temp_dir):
        """Test performance of HTML generation."""
        # Create a large schema
        large_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Large Schema",
            "properties": {}
        }
        
        # Add many properties
        for i in range(100):
            large_schema["properties"][f"property_{i}"] = {
                "type": "object",
                "properties": {
                    f"nested_{j}": {"type": "string"}
                    for j in range(10)
                }
            }
        
        schema_file = temp_dir / "large.schema.json"
        with open(schema_file, 'w') as f:
            json.dump(large_schema, f)
        
        # Test performance
        start_time = time.time()
        
        html_content = generate_schema_html(schema_file, 'schema')
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 2.0, "HTML generation should be fast"
        assert 'jsoncrack-container' in html_content
        assert len(html_content) > 0
    
    def test_find_schema_files_performance(self, temp_dir):
        """Test performance of finding schema files."""
        # Create many schema files in subdirectories
        for i in range(10):
            subdir = temp_dir / f"subdir_{i}"
            subdir.mkdir()
            
            for j in range(20):
                schema_file = subdir / f"schema_{j}.schema.json"
                with open(schema_file, 'w') as f:
                    json.dump({"type": "string"}, f)
        
        # Test performance
        start_time = time.time()
        
        files = find_schema_files(temp_dir, pattern="**/*.schema.json")
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 1.0, "File finding should be fast"
        assert len(files) == 200  # 10 * 20
    
    def test_config_parsing_performance(self):
        """Test performance of configuration parsing."""
        from jsoncrack_for_sphinx.config import (
            RenderMode, Directions, Theme, ContainerConfig, RenderConfig
        )
        
        # Create complex configuration
        config_dict = {
            'render': RenderConfig(RenderMode.OnScreen(threshold=0.1, margin='50px')),
            'container': ContainerConfig(
                direction=Directions.RIGHT,
                height='500',
                width='100%'
            ),
            'theme': Theme.AUTO
        }
        
        # Test performance of parsing many times
        start_time = time.time()
        
        for _ in range(1000):
            parsed_config = parse_config(config_dict)
            values = get_config_values(parsed_config)
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 1.0, "Config parsing should be fast"
    
    def test_autodoc_processing_performance(self, temp_dir):
        """Test performance of autodoc processing."""
        # Create schema files
        schema_dir = temp_dir / "schemas"
        schema_dir.mkdir()
        
        for i in range(50):
            schema_data = {
                "type": "object",
                "title": f"Test Schema {i}",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "integer"}
                }
            }
            
            with open(schema_dir / f"test_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Mock Sphinx app
        mock_app = Mock()
        mock_app.config = Mock()
        mock_app.config.json_schema_dir = str(schema_dir)
        mock_app.env = Mock()
        mock_app.env._jsoncrack_schema_paths = {}
        
        # Test performance of signature processing
        start_time = time.time()
        
        for i in range(50):
            autodoc_process_signature(
                mock_app, 'function', f'module.test_{i}', 
                Mock(), {}, 'signature', 'return_annotation'
            )
        
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 2.0, "Autodoc processing should be fast"


class TestStress:
    """Stress tests for the extension."""
    
    def test_many_schema_files_stress(self, temp_dir):
        """Test handling many schema files."""
        # Create many schema files
        num_files = 500
        
        for i in range(num_files):
            schema_data = {
                "type": "object",
                "title": f"Stress Test Schema {i}",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    f"custom_field_{i}": {"type": "string"}
                }
            }
            
            with open(temp_dir / f"stress_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Test finding files
        files = find_schema_files(temp_dir)
        assert len(files) == num_files
        
        # Test creating index
        index = create_schema_index(temp_dir)
        assert "Schema Index" in index
        assert len(index.split('\n')) > num_files  # Should have many lines
    
    def test_large_schema_stress(self, temp_dir):
        """Test handling very large schema."""
        # Create a very large schema
        large_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Stress Test Large Schema",
            "properties": {}
        }
        
        # Add many nested properties
        for i in range(200):
            large_schema["properties"][f"section_{i}"] = {
                "type": "object",
                "properties": {
                    f"field_{j}": {
                        "type": "object",
                        "properties": {
                            f"nested_{k}": {"type": "string"}
                            for k in range(5)
                        }
                    }
                    for j in range(10)
                }
            }
        
        schema_file = temp_dir / "large_stress.schema.json"
        with open(schema_file, 'w') as f:
            json.dump(large_schema, f)
        
        # Test that it can be processed
        assert validate_schema_file(schema_file) is True
        
        info = get_schema_info(schema_file)
        assert info['title'] == "Stress Test Large Schema"
        assert len(info['properties']) == 200
        
        # Test HTML generation
        html = generate_schema_html(schema_file, 'schema')
        assert 'jsoncrack-container' in html
        assert len(html) > 1000  # Should be substantial
    
    def test_deep_nesting_stress(self, temp_dir):
        """Test handling deeply nested schemas."""
        # Create deeply nested schema
        def create_nested_schema(depth):
            if depth == 0:
                return {"type": "string"}
            
            return {
                "type": "object",
                "properties": {
                    "nested": create_nested_schema(depth - 1),
                    "value": {"type": "string"}
                }
            }
        
        deep_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "title": "Deep Nesting Test",
            "properties": {
                "root": create_nested_schema(20)  # 20 levels deep
            }
        }
        
        schema_file = temp_dir / "deep_nest.schema.json"
        with open(schema_file, 'w') as f:
            json.dump(deep_schema, f)
        
        # Test that it can be processed
        assert validate_schema_file(schema_file) is True
        
        info = get_schema_info(schema_file)
        assert info['title'] == "Deep Nesting Test"
        
        # Test HTML generation
        html = generate_schema_html(schema_file, 'schema')
        assert 'jsoncrack-container' in html
    
    def test_concurrent_processing_stress(self, temp_dir):
        """Test concurrent processing of schemas."""
        import threading
        
        # Create schema files
        num_files = 50
        for i in range(num_files):
            schema_data = {
                "type": "object",
                "title": f"Concurrent Test {i}",
                "properties": {
                    "id": {"type": "integer"},
                    "data": {"type": "string"}
                }
            }
            
            with open(temp_dir / f"concurrent_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Function to process schema
        def process_schema(schema_id):
            schema_file = temp_dir / f"concurrent_{schema_id}.schema.json"
            html = generate_schema_html(schema_file, 'schema')
            return 'jsoncrack-container' in html
        
        # Test concurrent processing
        threads = []
        results = []
        
        def worker(schema_id):
            result = process_schema(schema_id)
            results.append(result)
        
        for i in range(num_files):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All should succeed
        assert all(results)
        assert len(results) == num_files
    
    def test_memory_usage_stress(self, temp_dir):
        """Test memory usage with many operations."""
        # Create multiple schema files
        for i in range(100):
            schema_data = {
                "type": "object",
                "title": f"Memory Test {i}",
                "properties": {
                    f"field_{j}": {"type": "string"}
                    for j in range(20)
                }
            }
            
            with open(temp_dir / f"memory_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Perform many operations
        for i in range(100):
            schema_file = temp_dir / f"memory_{i}.schema.json"
            
            # Multiple operations on each file
            validate_schema_file(schema_file)
            get_schema_info(schema_file)
            generate_schema_html(schema_file, 'schema')
            
            # Clean up references (simulate garbage collection)
            del schema_file
        
        # Test should complete without memory issues
        assert True  # If we get here, memory usage was acceptable


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_schema_file(self, temp_dir):
        """Test handling of empty schema file."""
        empty_file = temp_dir / "empty.schema.json"
        empty_file.touch()
        
        assert validate_schema_file(empty_file) is False
        
        with pytest.raises(ValueError):
            get_schema_info(empty_file)
    
    def test_malformed_json_schema(self, temp_dir):
        """Test handling of malformed JSON."""
        malformed_file = temp_dir / "malformed.schema.json"
        with open(malformed_file, 'w') as f:
            f.write('{"type": "object", "properties": {')  # Missing closing braces
        
        assert validate_schema_file(malformed_file) is False
        
        html = generate_schema_html(malformed_file, 'schema')
        assert 'error' in html.lower()
    
    def test_binary_file_as_schema(self, temp_dir):
        """Test handling of binary file as schema."""
        binary_file = temp_dir / "binary.schema.json"
        with open(binary_file, 'wb') as f:
            f.write(b'\x00\x01\x02\x03\x04\x05')
        
        assert validate_schema_file(binary_file) is False
        
        html = generate_schema_html(binary_file, 'schema')
        assert 'error' in html.lower()
    
    def test_very_long_filename(self, temp_dir):
        """Test handling of very long filename."""
        long_name = "a" * 200  # Very long filename
        long_file = temp_dir / f"{long_name}.schema.json"
        
        try:
            schema_data = {"type": "string"}
            with open(long_file, 'w') as f:
                json.dump(schema_data, f)
            
            # Should handle long filename
            assert validate_schema_file(long_file) is True
            
            info = get_schema_info(long_file)
            assert long_name in info['file_name']
        except OSError:
            # Some filesystems may not support very long filenames
            pytest.skip("Filesystem doesn't support long filenames")
    
    def test_unicode_in_schema(self, temp_dir):
        """Test handling of Unicode in schema."""
        unicode_schema = {
            "type": "object",
            "title": "Тест Unicode 测试 🚀",
            "description": "Schema with Unicode characters: café, naïve, 北京",
            "properties": {
                "名前": {"type": "string", "description": "Name in Japanese"},
                "città": {"type": "string", "description": "City in Italian"},
                "🏠": {"type": "string", "description": "House emoji"}
            }
        }
        
        unicode_file = temp_dir / "unicode.schema.json"
        with open(unicode_file, 'w', encoding='utf-8') as f:
            json.dump(unicode_schema, f, ensure_ascii=False, indent=2)
        
        assert validate_schema_file(unicode_file) is True
        
        info = get_schema_info(unicode_file)
        assert "Тест Unicode 测试 🚀" in info['title']
        assert "🏠" in info['properties']
        
        html = generate_schema_html(unicode_file, 'schema')
        assert 'jsoncrack-container' in html
    
    def test_circular_references_in_config(self):
        """Test handling of circular references in configuration."""
        # This would be more relevant for complex configurations
        # For now, test that basic configs don't cause issues
        
        from jsoncrack_for_sphinx.config import JsonCrackConfig
        
        config = JsonCrackConfig()
        
        # Test that we can serialize and deserialize config
        config_dict = {
            'render': config.render,
            'container': config.container,
            'theme': config.theme
        }
        
        # Should not cause infinite recursion
        values = get_config_values(config)
        assert isinstance(values, dict)
        assert len(values) > 0
    
    def test_permission_denied_schema_file(self, temp_dir):
        """Test handling of permission denied on schema file."""
        import os
        import stat
        
        # Create schema file
        schema_file = temp_dir / "permission_test.schema.json"
        with open(schema_file, 'w') as f:
            json.dump({"type": "string"}, f)
        
        try:
            # Remove read permissions
            os.chmod(schema_file, stat.S_IWRITE)
            
            # Should handle permission error gracefully
            try:
                result = validate_schema_file(schema_file)
                assert result is False
            except PermissionError:
                # This is expected - the function should raise PermissionError
                pass
            
            html = generate_schema_html(schema_file, 'schema')
            assert 'error' in html.lower()
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(schema_file, stat.S_IREAD | stat.S_IWRITE)
            except:
                pass
    
    def test_network_path_schema_file(self, temp_dir):
        """Test handling of network path (if applicable)."""
        # This test is more relevant on Windows with UNC paths
        # For Unix systems, we'll test a symlink scenario
        
        # Create schema file
        schema_file = temp_dir / "original.schema.json"
        with open(schema_file, 'w') as f:
            json.dump({"type": "object", "title": "Original"}, f)
        
        # Create symlink
        symlink_file = temp_dir / "symlink.schema.json"
        try:
            symlink_file.symlink_to(schema_file)
            
            # Should handle symlink correctly
            assert validate_schema_file(symlink_file) is True
            
            info = get_schema_info(symlink_file)
            assert info['title'] == "Original"
        except OSError:
            # Symlinks may not be supported on all systems
            pytest.skip("Symlinks not supported on this system")


@pytest.mark.slow
class TestLongRunning:
    """Long-running tests for stability."""
    
    def test_extended_usage_simulation(self, temp_dir):
        """Simulate extended usage of the extension."""
        # Create base schema files
        for i in range(20):
            schema_data = {
                "type": "object",
                "title": f"Extended Test {i}",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
            
            with open(temp_dir / f"extended_{i}.schema.json", 'w') as f:
                json.dump(schema_data, f)
        
        # Simulate many operations over time
        for iteration in range(100):
            # Find schemas
            for i in range(20):
                find_schema_for_object(f'module.extended_{i}', str(temp_dir))
            
            # Generate HTML
            for i in range(0, 20, 2):  # Every other file
                schema_file = temp_dir / f"extended_{i}.schema.json"
                generate_schema_html(schema_file, 'schema')
            
            # Validate files
            for i in range(0, 20, 5):  # Every 5th file
                schema_file = temp_dir / f"extended_{i}.schema.json"
                validate_schema_file(schema_file)
        
        # Should complete without issues
        assert True
